"""
Script used to initialize the database tables and add any preset words to the 
database. Currently being called whenever the app is started up, but can be 
called initially only once and removed from app.py as per preference and 
performance requirements.
"""

from utils import fetch_definition
import pandas as pd
from config import PRESET_FILE
from flashcard import Flashcard


def create_tables(db):
    """
    Creates tables in the database if they don't exist

    PARAMETERS :-
        db: Database connection object

    RETURNS :-
        None
    """

    db.create(
        """CREATE TABLE IF NOT EXISTS users 
              (user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
              username TEXT NOT NULL, 
              password TEXT NOT NULL)
              ;"""
    )

    db.create(
        """CREATE TABLE IF NOT EXISTS flashcards 
              (card_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
              word TEXT NOT NULL, 
              definitions TEXT NOT NULL, 
              pos TEXT NOT NULL, 
              type TEXT NOT NULL);"""
    )

    db.create(
        """CREATE TABLE IF NOT EXISTS mapping 
              (mapping_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
              user_id INTEGER NOT NULL, 
              card_id INTEGER NOT NULL, 
              status TEXT NOT NULL, 
              FOREIGN KEY (user_id) REFERENCES users(user_id), 
              FOREIGN KEY (card_id) REFERENCES flashcards(card_id))
              ;"""
    )


def initialize_flashcards(db, preset_file):
    """
    Reads preset words from the given file and adds them to the database
    if the file exists.

    PARAMETERS :-
        db: Database connection object
        preset_file: String containing path to CSV file with preset words,
            any CSV file containing a column called "word" will work

    RETURNS :-
        None
    """

    try:
        # Try reading CSV from specified path
        preset_df = pd.read_csv(preset_file)
        preset_words = preset_df["word"]
        db_preset = db.select("SELECT word FROM flashcards WHERE type = ?", "preset")
        db_preset = [word[0] for word in db_preset]
        for word in preset_words:
            # Check if word already exists in database
            if word not in db_preset:
                word_data = fetch_definition(word)
                if word_data:
                    added_flashcard = Flashcard(word, word_data, "preset")
                    add_preset(db, added_flashcard)

    except:
        # CSV file not found, no preset cards are added
        pass


def add_preset(db, card):
    """
    Adds the input card in the database as a preset card

    PARAMETERS :-
        db: Database connection object
        card: Flashcard to be added

    RETURNS :-
        None
    """

    exists = db.select("SELECT card_id FROM flashcards WHERE word = ?", card.word)
    if not exists:
        print(f"ADDING {card.word}")
        db.insert(
            "INSERT INTO flashcards (word, definitions, pos, type) VALUES (?,?,?,?)",
            card.word,
            ",".join(card.definitions),
            ",".join(card.pos),
            card.flashcard_type,
        )


def init(db):
    """
    Driver function to initialize the database

    PARAMETERS :-
        db: Database connection object

    RETURNS :-
        None
    """

    create_tables(db)
    initialize_flashcards(db, PRESET_FILE)
