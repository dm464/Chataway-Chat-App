# app.py
import os, flask, flask_sqlalchemy, flask_socketio, models 
from os.path import join, dirname
from dotenv import load_dotenv

MESSAGES_RECEIVED_CHANNEL = 'messages received'

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

dotenv_path = join(dirname(__file__), 'sql.env')
load_dotenv(dotenv_path)

sql_user = os.environ['SQL_USER']
sql_pwd = os.environ['SQL_PASSWORD']

database_uri = 'postgresql://{}:{}@localhost/postgres'.format(
    sql_user, sql_pwd)

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app

def emit_all_messages(channel):
    # TODO -- Content.jsx is looking for a key called allAddresses
    all_messages = [ \
        db_message.message for db_message in \
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
    
    # TODO
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL)
    

@socketio.on('disconnect')
def on_disconnect():
    print ('Someone disconnected!')
    socketio.emit('disconnected', {
        'test': 'Disconnected'
    })

@socketio.on('new message sent')
def on_new_message(data):
    print("Got an event for new message with data:", data)
    
    db.session.add(models.Message(data["user"], data["message"]));
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