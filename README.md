
# Chataway Chat Application

## Description
This project uses Flask(in Python) and the Twitter and Spoonacular API's along with Heroku to deploy a simple web
application that shows information about my favourite recipes and related quotes/tweets.  These resources are
dynamically generated.

## Setup
To use this repository, you must follow these steps:
###1. Run `git clone https://github.com/NJIT-CS490/project2-m2-dm464`
###2. Go to github and make a new personal repository.
3. To make your own personal repository and have your git point to it, run the following:
    `git remote rm origin` &&
    `git remote add origin http://www.github.com/<your-username>/<your-repo-name>`.
4. Run `git remote -v` and make sure this points to your newly created Github repo
5. Now run `git push origin master`
6. 


0. Sign up for the twitter developer portal at https://developer.twitter.com. Sign up for spoonacular at https://spoonacular.com/food-api/console.
1. Navigate to https://developer.twitter.com/en/portal/projects-and-apps and make a new app.
2. Click on the key symbol after creating your project, and it will take you to your keys and tokens.
    If needed, you can regenerate your access token and secret.
3. Sign up for spoonacular at https://spoonacular.com/food-api/console.
4. Navigate and find spoonacular keys.
5. Clone this repository by using git clone https://github.com/NJIT-CS490/project1-dm464
6. Run the following in your terminal:
    sudo pip install tweepy
    (or) sudo pip3 install tweepy
    (or) pip install tweepy
    (or) pip3 install tweepy
7. Install spoonacular using the same process as above ([sudo] pip[3] install spoonacular)
8. Install flask using the same process as above ([sudo] pip[3] install flask)
9. Install python-dotenv using the same process as above ([sudo] pip[3] install python-dotenv)
10. Add your secret keys (from step 2) by making a new root-level file called tweepy.env and populating it as follows.
    **** MAKE SURE THE FILE AND VARIABLES ARE NAMED THE EXACT SAME WAY AS DESCRIBED!!!***
    KEY=''
    KEY_SECRET=''
    TOKEN=''
    TOKEN_SECRET=''
11. Also in your local copy of this repository, create a another new root-level file called spoonacular.env adding the following line in spoonacular.env:
    **** MAKE SURE THE FILE AND VARIABLES ARE NAMED THE EXACT SAME WAY AS DESCRIBED!!!***
    SPOONACULAR_KEY=''
12. Save your files and run `python project1.py`
13. If on Cloud9, preview templates/index.html. This should successfully render the HTML!
14. Sign up for heroku at heroku.com
15. Install heroku by running npm install -g heroku
16. Add your secret keys (from tweepy.env and spoonacular.env) by going to https://dashboard.heroku.com/apps
    and clicking into your app. Click on Settings, then scroll to "Config Vars." Click
    "Reveal Config Vars" and add the key value pairs for each variable in project1.py
    Your config var key names should be:
    KEY
    KEY_SECRET
    TOKEN
    TOKEN_SECRET
    SPOONACULAR_KEY
17. Configure requirements.txt with all requirements needed to run your app:
    Flask
    tweepy
    python-dotenv
    spoonacular
18. Configure Procfile with the command needed to run your app:
    web: python project1.py
19. Go through the following steps:
    heroku login -i
    heroku create
    git push heroku master
20. Navigate to your newly-created heroku site!


## Troubleshoot
1. When working on the html, the style from the css stylsheet wasn't being reflected.  The way to make the changes appear
on the page is to have press `Ctrl + Shift + R`
2. When getting the recipe info from spoonacular, the 'total_results' attribute didn't match the actual number of searches I could
parse through, causing some index errors.  I solved this by not referring to the 'total_results' attribute and relying only on the size
of the results dictionary parsed from JSON.
3. Some of the pages wouldn't load properly given my original list of food items until I later realized that some
good items were simply not available on spoonacular.  I ended up changing my list to have less exotic items.

## Known Issues
1. This app currently displays the 2 most recent relevant twitter quote.  To make this better and more randomized, it should
choose randomly from a collection of several search results.
2. To make the app look nicer, there could be a way found around the tweet including a link when it's too long.
3. Some of the recipes from spoonacular have the steps separated by different parameters.  Some are separated by newline characters,
others by HTML tags, and some by the word "Step n".  For better display, the instructions could be parsed so as to have the recipes
displayed by steps, making it look more organized.

## Author
Denisse Mendoza
