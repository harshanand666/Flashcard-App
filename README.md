# Overview
This is a flask based web app for a Flashcard and Vocabulary learning application. This enables you to create custom flashcards for any word you might want by automatically fetching the relevant definition from an API, as well as add a flashcard from preset cards already available. Features - 
- Sign up and Login functionality to allow separate users
- A "Learn" page to view stats about the user's current progress, as well as learn by going through flashcards randomly
- A "Create" page to create custom flashcards or add flashcards from the preset words provided
- A "Manage" page to view all the user's cards in a list view along with the ability to delete any of them

## Tech used
- Python and Flask for backend and routing 
- HTML, CSS, Javascript and Jinja for frontend 
- SQLite for storing data in databases

## Video walkthrough 
https://www.youtube.com/watch?v=hd8jmXESIeY 

# Usage Instructions
- All required dependencies to run the app are in 'requirements.txt'
- Every time the app runs, the 'initialize_db' script runs to create the database, tables and add the preset cards from a preset file. If the database and preset words already exist, it skips this process. If this preset file does not exist, no cards will be added but the application will still run. It is advised to keep the preset file as is in the 'data' folder for complete functionality
- Currently the code to remove saved sessions on app restart has been implemented by explicitly deleting files in the flask_session directory every time the app boots up. This can be commented out incase that is not desired.


# Acknowledgements
- The API I used for fetching word definitions is from the freeDictionaryAPI github project (https://github.com/meetDeveloper/freeDictionaryAPI).
- The Dataset for preset words I used is from Kaggle (https://www.kaggle.com/datasets/sarthakvajpayee/gre-high-frequency-vocabulary-word-lists/). This has multiple files which can be used but for the purpose of demonstation I have only used one, the file called 'barron_333.csv' (https://www.kaggle.com/datasets/sarthakvajpayee/gre-high-frequency-vocabulary-word-lists/?select=barron_333.csv).
- I took inspiration from CS50's Week 9 material for certain frontend and flask concepts.
