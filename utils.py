from flask import redirect, session
import requests
from config import API_ENDPOINT


def login_required(f):
    """
    Decorator used for routes to redirect to the login page if user is not logged in.
    """

    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def fetch_definition(word):
    """
    Fetches the definition and POS data of the input word by making an API request
    to the dictionary API endpoint

    PARAMETERS :-
        word: Input word for which definitions are needed

    RETURNS :-
        word_data: Dictionary with POS and Defintions data for the input word
        None: If any error while hitting the API endpoint
    """

    response = requests.get(f"{API_ENDPOINT}/{word}")
    data = response.json()

    try:
        entry = data[0]
        word_data = {}
        word_data["word"] = entry["word"]
        word_data["meanings"] = {}

        for pos, meanings in entry["meaning"].items():
            if meanings:
                word_data["meanings"][pos] = meanings[0]["definition"]

        return word_data

    except:
        return None
