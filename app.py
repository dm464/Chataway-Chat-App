# app.py
import os, flask, flask_sqlalchemy, flask_socketio, models, bot
from os.path import join, dirname
import dotenv

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

def emit_user_count(channel):
    socketio.emit(channel, {'user_count': user_count})

def emit_all_messages(channel):
    # TODO -- Content.jsx is looking for a key called allAddresses
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
def index():
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
