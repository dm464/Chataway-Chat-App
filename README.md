
# Chataway Chat Application

## Description
This project uses Flask(in Python), React, PostgreSQL, Facebook and Google OAuth, Socket.io, and several APIs along with Heroku to deploy a web
chat application that allows users to sign in and chat publically with other online users.  This app provides persistence with the 

## Setup
To use this repository, you must follow these steps:
### 0. Clone this repo
1. Run `git clone https://github.com/NJIT-CS490/project2-m2-dm464`
2. Go to github and make a new personal repository.
3. To make your own personal repository and have your git point to it, run the following:
    - `git remote rm origin`
    - `git remote add origin http://www.github.com/<your-username>/<your-repo-name>`
4. Run `git remote -v` and make sure this points to your newly created Github repo
5. Now run `git push origin master`

### 1. Upgrade Node version to 7

`$ nvm install 7`

### 2. Install Required Python Modules & Libraries
- `pip install flask`  
- `pip install flask-socketio`  
- `pip install eventlet`
- `pip install python-dotenv`
- `pip install validators`

### 3. Setup OAuths
#### Google OAuth
1. Go to https://console.developers.google.com/ and login using your personal google account (if you don't already have one, just sign up)
2. Click "CREATE PROJECT" or in the dropdown menu called "Select a Project" in the top, click "NEW PROJECT".   
3. Make a new project named ChatApp. "No organization" is fine.  
4. Click "Credentials" in the left hand bar, then click "+ CREATE CREDENTIALS" and then click "OAuth client ID".  
4.5. If you see a warning that says "To create an OAuth client ID, you must first set a 
    product name on the consent screen", do the following steps:  
			1. Click the "CONFIGURE CONSENT SCREEN" button.
			2. Choose "External"
			3. For "Application name," specify "ChatApp" or something similar.
			4. Press save.
5. Go back to Credentials -> Create Credentials -> OAuth client ID. Click "web application".  
6. Make name the "ChatApp" and under both Authorized JavaScript origins & Authorized redirect URIs you're going to click "Add URI" and paste the
link for you website (once we deploy on heroku, we will have to add our heroku app link onto here too)
7. Click "Create" and copy your Client ID. This ID will be pasted into your scripts/GoogleButton.jsx file.  Towards the bottom of the file, where
it says clientId="<some-id>", you're going to replace <some-id> with the Client ID you just copied.

#### Facebook OAuth
1. Go to https://developers.facebook.com/ and login using your personal account (if you don't already have one, just sign up)
2. Create an App. Select “for everything else” and specify Project Name (i.e. "ChatApp")
3. Create App ID
4. Under add a Product select “Facebook Login” Setup
5. Enable Client OAuth login and Web OAuth login
6. Under Valid OAuth Redirect URIs inser the link for your website (same as with the Facebook one).  Keep in mind we will need to add a new URI when
we get our heroku app up.
7. Save Changes
8. Now you have your App ID that you can copy to make this work.  Include this key in your scripts/FacebookButton.jsx file towards the bottom of
the file where if says appId="<some-id>", you're going to replace <some-id> with the AppD you just copied.


### 4. Set up API keys
#### ipstack API for location feature
1. Sign up for ipstack at <https://ipstack.com/>
2. Click the "GET FREE API KEY" button.  When redirected, click on the same button.
3. Sign up and copy your API Access Key
4. Create a file called `ipstack.env` and add `IPSTACK_KEY='<your-api-access-key>'` to it.


### 2. Setting up PSQL
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`  
    Enter yes to all prompts.
2. Initialize PSQL database: `sudo service postgresql initdb`
3. Start PSQL: `sudo service postgresql start`
2. Make a new superuser: `sudo -u postgres createuser --superuser $USER`
    If you get an error saying "could not change directory", that's okay! It worked!
3. Make a new database: `sudo -u postgres createdb $USER`
        If you get an error saying "could not change directory", that's okay! It worked!
4. Make sure your user shows up:  
    a) `psql`  
    b) `\du` look for ec2-user as a user  
    c) `\l` look for ec2-user as a database  
5. Make a new user:  
    a) `psql` (if you already quit out of psql)  
    b) Type this with a new unique password:  
    `create user some_username_here superuser password 'some_unique_new_password_here';`  
    c) `\q` to quit out of sql

#### Getting PSQL to work with Python
1. Update yum: `sudo yum update`, and enter yes to all prompts  
2. Get psycopg2: `pip install psycopg2-binary`  
3. Get SQLAlchemy: `pip install Flask-SQLAlchemy==2.1`  
5. Make a new file called `sql.env` and add `DATABASE_URL='postgresql://<your-psql-username>:<your-password>@localhost/postgres'`in it
6. to enable read/write from SQLAlchemy, there's a special file that you need to enable your db admin password to work for:  
    1. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`  
    :warning: :warning: :warning: If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  :warning: :warning: :warning:  
    2. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`
    3. Save and exit by pressing ESC + : + x + Enter
    3. After changing those lines, run `sudo service postgresql restart`  

#### Set up DB  
0. `sudo service postgresql start`
1. In the python interactive shell, run:  
	`import models`  
	`models.db.create_all()`  
	`models.db.session.commit()`  

## 3. Install initial `npm` dependencies from `package.json`

This command runs `npm`, which looks inside our `package.json` file, 
retrieves a list of packages, and installs them to the `node_modules` folder
inside your repository. `node_modules` folder **does not** need to be pushed
to Heroku or GitHub.

- `npm install` 
- - `npm install -g webpack`  
- `npm install --save-dev webpack`  
    **Note: This command MUST be run from the folder that contains package.json!**
    **You will get an error if you are in a different folder!**
- `npm install socket.io-client --save` 
- `npm install html-react-parser` 
- `npm install interweave react` 
- `npm install react-facebook-login`
- `npm install react-google-login` 
  :warning: :warning: :warning: If you see any error messages, make sure you use `sudo pip` or `sudo npm`.
  If it says "pip cannot be found", run `which pip` and use `sudo [path to pip from which pip] install` :warning: :warning: :warning:
  
## 4. Compile Javascript using Webpack

This line starts up Webpack, which looks inside `webpack.config.js`, loads
configuration options, and starts transpiling your JS code into 
`static/script.js`. You may be asked to also install webpack-cli. Type **yes**.

```$ npm run watch```

(The program should not stop running. Leave it running.)

If this step fails for whatever reason, please close your terminal and restart it,
and re-run the command.

## 6. Run the web app

Open a new terminal in your AWS Cloud9 environment (click the little green + 
button near your current terminal and choose 'New Terminal'). Run `app.py` 
(from the same folder, but new terminal), then preview the running application,
and verify that the React renders. You should see "Hello World from React!" in
the preview.

**Do not manually edit `static/script.js`! It will update when you make changes.**
**You do need to push this file to Heroku and GitHub, which is why we put it in**
**our .gitignore files**


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
21. 

8. Run `python user_tweets.py`
9. If on Cloud9, preview templates/index.html. This should successfully render the HTML!
10. Sign up for heroku at heroku.com 
11. Install heroku by running npm install -g heroku
13. Go through the following steps:
    heroku login -i
    heroku create
    git push heroku master
14. Navigate to your newly-created heroku site!
14.5. Add your secret keys (from tweepy.env) by going to https://dashboard.heroku.com/apps
    and clicking into your app. Click on Settings, then scroll to "Config Vars." Click
    "Reveal Config Vars" and add the key value pairs for each variable in user_tweets.py
    Your config var key names should be:
    KEY
    KEY_SECRET
    TOKEN
    TOKEN_SECRET
15. Configure requirements.txt with all requirements needed to run your app.
16. Configure Procfile with the command needed to run your app.
17. If you are still having issues, you may use heroku logs --tail to see what's wrong.


## Troubleshoot
1. I had difficulty understanding how to use sockets.  In particular, I was having a hard time trying to figure out how to
prevent users who weren’t logged in yet from sending messages to the chat.  Also, I was having a hard time understanding
how to display the messages that were saved on the database to a user only upon logging in.  To solve this problem, I 
spent a long time reading the flask-socketio documentation.  I realized later that I could make use of the rooms feature 
on sockets.  In doing this, I can make the main chat in the room, that the user can join only upon successful login.  
Upon joining the room, the user was then emitted the chat history from the server
2. I had a hard time rendering the messages that the user sent that were meant to be links/images.  The reason for this is 
because the messages were being passed from the server to the client as strings so tags within the string were not being
rendered and were being shown on the webpage.  As I did research, I found there exists a React component called Interweave 
that parses the string and returns html tags.


## Known Issues & Further Improvements
1. The overall layout of the app can be improved.  I currently don’t have the username remaining constant on the page.
Also, the user’s photo doesn’t display next to the message.
2. There are some security risks with this app since the messages the users types are being rendered by the Interweave
component, this could potentially lead to attacks.

## Author
Denisse Mendoza
