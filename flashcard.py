import random


class Flashcard:
    """
    Data model for storing a flashcard object along with utility functions
    """

    def __init__(self, word, data, flashcard_type, status="new"):
        self.word = word
        self.data = data
        self.definitions = []
        self.pos = []
        self.flashcard_type = flashcard_type
        self.status = status
        self.parse_data()

    def parse_data(self):
        """
        Parses input "data" dictionary and populates the definitions and pos lists
        """

        for pos in self.data["meanings"].keys():
            self.definitions.append(self.data["meanings"][pos])
            self.pos.append(pos)

    def add_to_db(self, db, user_id):
        """
        Adds a flashcard object into the database

        PARAMETERS :-
            db: Database connection object
            user_id: User ID of the current user

        RETURNS :-
            exists_in_mapping: None if mapping does not exist, else an sqlite object
        """

        # If card already exists in database.flashcards, then only add mapping to existing flashcard
        exists = db.select("SELECT card_id FROM flashcards WHERE word = ?", self.word)
        exists_in_mapping = None
        if exists:
            card_id = exists[0]["card_id"]
            # If mapping already exists from a previous add, then do nothing
            exists_in_mapping = db.select(
                "SELECT * FROM mapping WHERE user_id = ? AND card_id = ?",
                user_id,
                card_id,
            )
            if not exists_in_mapping:
                db.insert(
                    "INSERT INTO mapping (user_id, card_id, status) VALUES (?,?,?)",
                    user_id,
                    card_id,
                    self.status,
                )
        else:
            # Add card to flashcards and the corresponding mapping for the user
            db.insert(
                "INSERT INTO flashcards (word, definitions, pos, type) VALUES (?,?,?,?)",
                self.word,
                ",".join(self.definitions),
                ",".join(self.pos),
                self.flashcard_type,
            )
            card_id = db.cur.lastrowid
            db.insert(
                "INSERT INTO mapping (user_id, card_id, status) VALUES (?,?,?)",
                user_id,
                card_id,
                self.status,
            )

        return exists_in_mapping

    @staticmethod
    def load_from_db(db, card_id, user_id):
        """
        Loads a flashcard from the database

        PARAMETERS :-
            db: Database connection object
            card_id: ID of the flashcard that needs to be loaded
            user_id: User ID of the current user

        RETURNS :-
            A new Flashcard object with data loaded in from the database
        """

        card_data = db.select("SELECT * FROM flashcards WHERE card_id = ?", card_id)

        # If card does not exist
        if not card_data:
            return None

        else:
            # Convert card_data into the correct format to pass into the Flashcard class
            card_data = card_data[0]
            data_dict = {}
            data_dict["meanings"] = dict()
            word = card_data["word"]
            defs = card_data["definitions"].split(",")
            pos = card_data["pos"].split(",")
            card_type = card_data["type"]
            status = db.select(
                "SELECT status FROM mapping WHERE card_id = ? AND user_id = ?",
                card_id,
                user_id,
            )[0]["status"]

            for i, p in enumerate(pos):
                data_dict["meanings"][p] = defs[i]

            return Flashcard(word, data_dict, card_type, status)

    @staticmethod
    def delete_from_db(db, card_id, user_id):
        """
        Deletes the flashcard and/or relevant mapping from the database

        PARAMETERS :-
            db: Database connection object
            card_id: ID of the flashcard that needs to be loaded
            user_id: User ID of the current user

        RETURNS :-
            None
        """

        # Delete mapping
        num_users = len(db.select("SELECT * FROM mapping WHERE card_id = ?", card_id))
        db.delete(
            "DELETE FROM mapping WHERE card_id = ? AND user_id = ?", card_id, user_id
        )
        type_of_card = db.select(
            "SELECT type FROM flashcards WHERE card_id = ?", card_id
        )[0]["type"]

        # Only delete flashcard if no other user is mapped to it and not a preset flashcard
        if num_users == 1 and type_of_card == "custom":
            db.delete("DELETE FROM flashcards WHERE card_id = ?", card_id)

    @staticmethod
    def update_status(db, word, user_id, new_status):
        """
        Updates the current "status" of a flashcard-user mapping in the database

        PARAMETERS :-
            db: Database connection object
            word: Word for which status needs to be changed
            user_id: User ID of the current user
            new_status: New status to be updated

        RETURNS :-
            None
        """

        card_id = db.select("SELECT card_id FROM flashcards WHERE word = ?", word)[0][
            "card_id"
        ]

        db.update(
            "UPDATE mapping SET status = ? WHERE card_id = ? AND user_id = ?",
            new_status,
            card_id,
            user_id,
        )

    @staticmethod
    def get_random_flashcard(db, user_id):
        """
        Returns a random flashcard from the current user's list of cards.
        "unknown" and "new" cards are twice as likely as "known" cards to show up.

        PARAMETERS :-
            db: Database connection object
            user_id: User ID of the current user

        RETURNS :-
            A new Flashcard object created from a random card from the user's list of cards
        """

        cards = db.select(
            "SELECT card_id, status FROM mapping WHERE user_id = ?", user_id
        )

        weighted_ids = []
        for card in cards:
            card_id = card["card_id"]
            weighted_ids.append(card_id)

            if card["status"] != "known":
                # If card status is "unknown" or "new" add an additional entry to double the weight
                weighted_ids.append(card_id)

        rand_id = random.choice(weighted_ids)
        return Flashcard.load_from_db(db, int(rand_id), user_id)
