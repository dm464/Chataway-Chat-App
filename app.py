# app.py
import os, flask, flask_sqlalchemy, flask_socketio, models, bot
from datetime import datetime
from os.path import join, dirname
import dotenv

MESSAGES_RECEIVED_CHANNEL = 'messages received'
USER_COUNT_CHANNEL = 'user added/dropped'
USER_INFO_CHANNEL = 'current user info'

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
    if models.AuthUser.query.filter_by(email=email).first() is None:
        db.session.add(models.AuthUser(auth_type, name, email, picture));
        db.session.commit();
        print("Added {} to database".format(name))
    else:
        print("{} is already in database".format(name))

def emit_user_count(channel):
    socketio.emit(channel, {'user_count': user_count})

def emit_user_info(channel, email, room):
    user_id = models.AuthUser.query.filter_by(email=email).first().id
    picture = models.AuthUser.query.filter_by(email=email).first().picture
    socketio.emit(channel, {'user_id': user_id, "picture": picture}, room=room)
    print("Sent user_id={} to room={}".format(user_id, room))

def emit_all_messages(channel, room):
    all_messages = [ \
        {'user': db_message.user, \
        'message': db_message.message, \
        'timestamp': str(db_message.timestamp), \
        'user_id': db_message.user_id, \
        'user_pic': db_message.user_pic} \
        for db_message in db.session.query(models.Message).all()
    ]
    
    socketio.emit(channel, {'allMessages': all_messages}, room=room)


@socketio.on('connect')
def on_connect():
    print('Someone connected!')
    socketio.emit('connected', {
        'test': 'Connected'
    })
    global user_count
    user_count+=1


@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')
    socketio.emit('disconnected', {
        'test': 'Disconnected'
    })
    global user_count
    user_count-=1

    emit_user_count(USER_COUNT_CHANNEL)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    flask_socketio.join_room(room)
    flask_socketio.send(username + ' has entered the room.', room=room)
    emit_user_count(USER_COUNT_CHANNEL)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL, room)

@socketio.on('new facebook user')
def on_new_facebook_user(data):
    print("Got an event for new facebook user input with data:", data)
    push_new_user_to_db(models.AuthUserType.FACEBOOK, data["name"], data["email"], data["picture"])
    emit_user_info(USER_INFO_CHANNEL, data["email"], flask.request.sid)

@socketio.on('new google user')
def on_new_google_user(data):
    print("Got an event for new google user input with data:", data)
    push_new_user_to_db(models.AuthUserType.GOOGLE, data["name"], data["email"], data["picture"])
    emit_user_info(USER_INFO_CHANNEL, data["email"], flask.request.sid)

@socketio.on('new message sent')
def on_new_message(data):
    if "main chat" in flask_socketio.rooms():
        print("Got an event for new message with data:", data)
        message = bot.render(data["message"])
        db.session.add(models.Message(data["user"], message, data["timestamp"], data["user_id"], data["user_pic"]));
        db.session.commit();
        
        if bot.is_bot_command(data["message"]):
            reply = bot.bot_reply(data["message"])
            bot_timestamp = datetime.now()
            db.session.add(models.Message("bot", reply, bot_timestamp, 0, bot.BOT_PIC));
            db.session.commit();
        
        emit_all_messages(MESSAGES_RECEIVED_CHANNEL, "main chat")

@app.route('/')
def chat():
    models.db.create_all()
    db.session.commit()

    return flask.render_template("index.html")
    

if __name__ == '__main__': 
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080)),
        debug=True
    )
