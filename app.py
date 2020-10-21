# app.py
import os, flask, flask_sqlalchemy, flask_socketio, models, bot
from os.path import join, dirname
import dotenv

USERS_UPDATED_CHANNEL = 'users updated'
MESSAGES_RECEIVED_CHANNEL = 'messages received'
USER_COUNT_CHANNEL = 'user added/dropped'

user_count = 0

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

try:
    dotenv_path = join(dirname(__file__), 'sql.env')
    dotenv.load_dotenv(dotenv_path)
except AttributeError:
    pass

database_uri = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

def push_new_user_to_db(auth_type, name, email, picture):
    # TODO remove this check after the logic works correctly
    db.session.add(models.AuthUser(auth_type, name, email, picture));
    db.session.commit();
    print("Added {} to database".format(name))

def emit_user_count(channel):
    socketio.emit(channel, {'user_count': user_count})

def emit_all_messages(channel):
    all_messages = [ \
        {'user': db_message.user, 'message': db_message.message} for db_message in \
        db.session.query(models.Message).all()
    ]
    
    socketio.emit(channel, {
        'allMessages': all_messages
    })


@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    global user_count
    user_count+=1

    emit_user_count(USER_COUNT_CHANNEL)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')
    socketio.emit('disconnected', {
        'test': 'Disconnected'
    })
    global user_count
    user_count-=1

    emit_user_count(USER_COUNT_CHANNEL)

@socketio.on('new facebook user')
def on_new_facebook_user(data):
    print("Got an event for new facebook user input with data:", data)
    push_new_user_to_db(models.AuthUserType.FACEBOOK, data["name"], data["email"], data["picture"])

@socketio.on('new google user')
def on_new_google_user(data):
    print("Got an event for new google user input with data:", data)
    push_new_user_to_db(models.AuthUserType.GOOGLE, data["name"], data["email"], data["picture"])

@socketio.on('new message sent')
def on_new_message(data):
    print("Got an event for new message with data:", data)
    
    db.session.add(models.Message(data["user"], data["message"]));
    db.session.commit();
    
    if bot.is_bot_command(data["message"]):
        reply = bot.bot_reply(data["message"])
        db.session.add(models.Message("bot", reply));
        db.session.commit();
    
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

@app.route('/')
def chat():
    models.db.create_all()
    db.session.commit()
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)

    return flask.render_template("index.html")
    

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
