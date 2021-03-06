
# Chataway Chat Application
http://chataway-app.herokuapp.com/
## Description
Chataway is a public chat application! After users sign in by using either Facebook or Google OAuth, they can publicly send text messages, images, and links to other online users.  One can view a live display of the number of users that are currently logged in.  Users also have the ability to interact with a chat bot by sending messages with specified bot commands.  When sending the message "!! help", the bot will respond with details on how to interact with it.

This project uses Flask(in Python), React, PostgreSQL, Facebook and Google OAuth, Socket.io, and several APIs along with Heroku for deployment. This app provides persistence through the PostgreSQL database, manipulated using SQLAlchemy ORM.

![Chataway Chat App](resources/Chataway.JPG?raw=true "Chataway Chat App")

## Potential Improvements & Enhancements
1. Chataway could display a screen with a list of all users that are currently logged in.  This would improve interraction through the app.
2. A big enhancement could be to give the user the ability to create chat rooms/groups through which a select people can send messages to each other.

## Challenges Faced and Troubleshooting
1. I had difficulty understanding how to use sockets.  In particular, I was having a hard time trying to figure out how to prevent users who weren’t logged in yet from sending messages to the chat.  Also, I was having a hard time understanding how to display the messages that were saved on the database to a user only upon logging in.  To solve this problem, I spent a long time reading the flask-socketio documentation.  I realized later that I could make use of the rooms feature on sockets.  In doing this, I can make the main chat in the room, that the user can join only upon successful login. Upon joining the room, the user was then emitted the chat history from the server
2. I had a hard time rendering the messages that the user sent that were meant to be links/images.  The reason for this is because the messages were being passed from the server to the client as strings so tags within the string were not being rendered and were being shown on the webpage.  As I did research, I found there exists a React component called Interweave that parses the string and returns html tags.

## Known Issues
1. The layout of the oauth login screen can be improved. It currently looks very cheap and unaesthetic.
2. There are some security risks with this app since the messages the users types are being rendered by the Interweave component, this could potentially lead to attacks.
3. The structure of the React/JS files could utilize best practices. Several parts of the programs (like messages) could be made into components.  This will not only increase readability but will make the code more modularized.
4. When the user sends a new message, the display doesn't scroll down to the sent message.

## Reason For Chosen Test Code
The reason I chose to test the code that I did is because the bot commands are what determines proper user interaction with
the chat bot.  Also, those functions make up the majority of the python code.

If I had the time, I would have liked to have tested some of the bot commands that use the location API.
I would have also liked to have tested more mocked functionality liked the database and socketio functions.

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
1. Go to <https://console.developers.google.com/> and login using your personal google account (if you don't already have one, just sign up)
2. Click "CREATE PROJECT" or in the dropdown menu called "Select a Project" in the top, click "NEW PROJECT".   
3. Make a new project named ChatApp. "No organization" is fine.  
4. Click "Credentials" in the left hand bar, then click "+ CREATE CREDENTIALS" and then click "OAuth client ID".  
4.5. If you see a warning that says "To create an OAuth client ID, you must first set a 
product name on the consent screen", do the following steps:  
	a. Click the "CONFIGURE CONSENT SCREEN" button.
	b. Choose "External"
	c. For "Application name," specify "ChatApp" or something similar.
	d. Press save.
5. Go back to Credentials -> Create Credentials -> OAuth client ID. Click "web application".  
6. Make name the "ChatApp" and under both Authorized JavaScript origins & Authorized redirect URIs you're going to click "Add URI" and paste the
link for you website (once we deploy on heroku, we will have to add our heroku app link onto here too)
7. Click "Create" and copy your Client ID. This ID will be pasted into your scripts/GoogleButton.jsx file.  Towards the bottom of the file, where
it says `clientId="<some-id>"``, you're going to replace <some-id> with the Client ID you just copied.

#### Facebook OAuth
1. Go to <https://developers.facebook.com/> and login using your personal account (if you don't already have one, just sign up)
2. Create an App. Select “for everything else” and specify Project Name (i.e. "ChatApp")
3. Create App ID
4. Under add a Product select “Facebook Login” Setup
5. Enable Client OAuth login and Web OAuth login
6. Under Valid OAuth Redirect URIs inser the link for your website (same as with the Facebook one).  Keep in mind we will need to add a new URI when
we get our heroku app up.
7. Save Changes
8. Now you have your App ID that you can copy to make this work.  Include this key in your scripts/FacebookButton.jsx file towards the bottom of
the file where if says `appId="<some-id>"``, you're going to replace <some-id> with the AppD you just copied.


### 4. Set up API keys
#### Ipstack API for Location Feature
1. Sign up for ipstack at <https://ipstack.com/>
2. Click the "GET FREE API KEY" button.  When redirected, click on the same button.
3. Sign up and copy your API Access Key
4. Create a file called `ipstack.env` and add `IPSTACK_KEY='<your-api-access-key>'` to it.


### 5. Setting up PSQL
1. Install PostGreSQL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`  
    Enter yes to all prompts.
2. Initialize PSQL database: `sudo service postgresql initdb`
3. Start PSQL: `sudo service postgresql start`
4. Make a new superuser: `sudo -u postgres createuser --superuser $USER`
    If you get an error saying "could not change directory", that's okay! It worked!
5. Make a new database: `sudo -u postgres createdb $USER`
        If you get an error saying "could not change directory", that's okay! It worked!
6. Make sure your user shows up:  
    a) `psql`  
    b) `\du` look for ec2-user as a user  
    c) `\l` look for ec2-user as a database  
7. Make a new user:  
    a) `psql` (if you already quit out of psql)  
    b) Type this with a new unique password:  
    `create user some_username_here superuser password 'some_unique_new_password_here';`  
    c) `\q` to quit out of sql

#### Getting PSQL to work with Python
1. Update yum: `sudo yum update`, and enter yes to all prompts  
2. Get psycopg2: `pip install psycopg2-binary`  
3. Get SQLAlchemy: `pip install Flask-SQLAlchemy==2.1`  
4. Make a new file called `sql.env` and add `DATABASE_URL='postgresql://<your-psql-username>:<your-password>@localhost/postgres'`in it
5. to enable read/write from SQLAlchemy, there's a special file that you need to enable your db admin password to work for:  
    a. Open the file in vim: `sudo vim /var/lib/pgsql9/data/pg_hba.conf`  
    :warning: :warning: :warning: If that doesn't work: `sudo vim $(psql -c "show hba_file;" | grep pg_hba.conf)`  :warning: :warning: :warning:  
    b. Replace all values of `ident` with `md5` in Vim: `:%s/ident/md5/g`
    c. Save and exit by pressing ESC + : + x + Enter
    d. After changing those lines, run `sudo service postgresql restart`  

#### Set up DB  
0. `sudo service postgresql start`
1. In the python interactive shell, run:  
	- `import models`  
	- `models.db.create_all()`  
	- `models.db.session.commit()`  

### 6. Install initial `npm` dependencies from `package.json`

This command runs `npm`, which looks inside our `package.json` file, 
retrieves a list of packages, and installs them to the `node_modules` folder
inside your repository. `node_modules` folder **does not** need to be pushed
to Heroku or GitHub.

- `npm install` 
- `npm install -g webpack`  
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
  
### 7. Compile Javascript using Webpack

This line starts up Webpack, which looks inside `webpack.config.js`, loads
configuration options, and starts transpiling your JS code into 
`static/script.js`. You may be asked to also install webpack-cli. Type **yes**.

```$ npm run watch```

***The program should not stop running. Leave it running!***

If this step fails for whatever reason, please close your terminal and restart it,
and re-run the command.

### 8. Run the web app

Simultaneously, while the Webpack is running, open a new terminal and run with `python app.py` 
(from the same folder, but new terminal), then preview the running application,
and verify that the React renders. You should the chat app.

**Do not manually edit `static/script.js`! It will update when you make changes.**
**You do need to push this file to Heroku and GitHub, which is why we put it in**
**our .gitignore files**

### 9. Deploying onto Heroku
1. Sign up for heroku at <https://www.heroku.com/> 
2. Install heroku by running `npm install -g heroku`

#### Pushing Database into Heroku
1. Log in to Heroku
`heroku login -i`
2. Create new Heroku app
`heroku create <app-name>`
3. Create postregresql database on Heroku:
    - `heroku addons:create heroku-postgresql:hobby-dev`
        ***You can copy database using pg:copy***
    - `heroku pg:wait`
4. Make sure you are the owner of your database
    a. Open psql
    b. Check list of users and roles `\du`
    c. Check list of databases `\l` (owner of postgres should be your username)
    d. Change owner of postgres database and add roles:
        - `ALTER DATABASE postgres OWNER to <your-psql-username>;`
        - `ALTER ROLE <your-psql-username> WITH CREATEDB;`
        - `ALTER ROLE <your-psql-username> WITH CREATEROLE;`
        - `ALTER ROLE <your-psql-username> WITH REPLICATION;`
    e. Leave psql
    f. `PGUSER=username heroku pg:push postgres DATABASE_URL`
        - If this doesn’t work, remove `PGUSER=[]` command
        - When it works, ignore “pg_restore errored with 1” message
5. Connect to heroku psql
    a. heroku `pg:psql`
    b. Here, you can run the same commands as in local psql

#### Pushing files into Heroku
1. On Heroku console, configure variables by adding your secret keys (from ipstack.env). Go to <https://dashboard.heroku.com/apps>
    and click into your app. Click on Settings, then scroll to "Config Vars." Click
    "Reveal Config Vars" and add the key value pairs for each variable used.
    Your config var key names should be:
    DATABASE_URL ***This is automatically configured***
    IPSTACK_KEY
2. Create and push heroku files
    a. Configure Procfile with the command needed to run your app:
    `web: python app.py`
    b. Configure requirements.txt with all requirements needed to run your app:
        i. Automatically load all requirements onto requirements.txt with `pip freeze > requirements.txt` command
3.	Commit and push changes to git
4.	Push onto heroku with `git push heroku master`
5.	After the app builds, navigate to your newly-created heroku site!
6.	If the app is not working then restart all dynos from heroku app console
7. If you are still having issues, you may use heroku logs --tail to see what's wrong.

## Author
Denisse Mendoza
