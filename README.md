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

# Usage Instructions
- All required dependencies to run the app are in 'requirements.txt'
- Every time the app runs, the 'initialize_db' script runs to create the database, tables and add the preset cards from a preset file. If the database and preset words already exist, it skips this process. If this preset file does not exist, no cards will be added but the application will still run. It is advised to keep the preset file as is in the 'data' folder for complete functionality
- Currently the code to remove saved sessions on app restart has been implemented by explicitly deleting files in the flask_session directory every time the app boots up. This can be commented out incase that is not desired.


# Acknowledgements
- The API I used for fetching word definitions is from the freeDictionaryAPI github project (https://github.com/meetDeveloper/freeDictionaryAPI).
- The Dataset for preset words I used is from Kaggle (https://www.kaggle.com/datasets/sarthakvajpayee/gre-high-frequency-vocabulary-word-lists/). This has multiple files which can be used but for the purpose of demonstation I have only used one, the file called 'barron_333.csv' (https://www.kaggle.com/datasets/sarthakvajpayee/gre-high-frequency-vocabulary-word-lists/?select=barron_333.csv).
- I took inspiration from CS50's Week 9 material for certain frontend and flask concepts.

# Initial Proposal

I would like to create a web app for a Flashcard / Vocabulary learning application. This could be a dashboard which helps someone improve vocabulary / study for exams like the GRE / learn english from scratch (something like this offered by Manhattan review , but more customizable). This would include
Signup / Login functionality to serve multiple users. Credentials will be stored in a database
A “Learn” page where users can go through flashcards randomly one by one. They would be able to choose any specific sets of flashcards, and there would be logic to determine which ones would appear more based on how the user does (they could select each word after it comes with either “knew it” or “didn’t know it”)
A “Create” page where the user could add a flashcard with any word they want. They can either choose from certain presets of varying difficulty, or they could type in their own words. This would make an API call to a dictionary API and automatically fetch definitions, examples, usage, etc
All saved/added flashcards would be saved in a database which the user can access at any time. They would be able to add and delete, but also mark them as based on their comfort with those words (learnt, partially learnt, no idea what this means, etc)
The preset flashcards will be added either using API calls or web scraping using Beautiful Soup.


# Initial Execution Plan
Execution Plan
- Week 4 - I will have explored web frameworks, dictionary APIs and preset flashcard websites, and hope to finalize the framework and API that I will be using, along with the database schemas.
- Week 5 - I will have login functionality working with a simple homepage, along with databases set up to store user credentials and flashcard data.
- Week 6 - I will have functionality to fetch definitions from the API and display the flashcards, as well as setup the data model for a flashcard. I will also have logic setup to mark flashcards as "learnt" or "not learnt" each time they show up.
- Week 7 - I will have created the basic layout of the entire web app, with ability to create custom flashcards and view/delete saved flashcards, along with the logic to “Learn” (show randomly, with varying frequency)
- Week 8 (tentative, if everything goes according to schedule) - I will add preset flashcards using APIs or using Beautiful Soup to scrape websites. These will be independent from custom flashcards.

