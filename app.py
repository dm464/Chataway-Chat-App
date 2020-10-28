"""
app.py

This module runs the server for the chat app
"""
import os
from datetime import datetime
from os.path import join, dirname
import flask
import flask_sqlalchemy
import flask_socketio
import dotenv
import models
import bot

MESSAGES_RECEIVED_CHANNEL = "messages received"
USER_COUNT_CHANNEL = "user added/dropped"
USER_INFO_CHANNEL = "current user info"

USER_COUNT = 0

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

try:
    dotenv_path = join(dirname(__file__), "sql.env")
    dotenv.load_dotenv(dotenv_path)
except AttributeError:
    pass

database_uri = os.environ["DATABASE_URL"]

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = flask_sqlalchemy.SQLAlchemy(app)
db.init_app(app)
db.app = app


def push_new_user_to_db(auth_type, name, email, picture):
    """Pushes user into database if not already inside"""
    if models.AuthUser.query.filter_by(email=email).first() is None:
        db.session.add(models.AuthUser(auth_type, name, email, picture))
        db.session.commit()
        print("Added {} to database".format(name))
    else:
        print("{} is already in database".format(name))


def emit_user_count(channel, room):
    """Sends user count to clients in chat room"""
    socketio.emit(channel, {"user_count": USER_COUNT}, room=room)


def emit_user_info(channel, email, room):
    """Sends user info to the client which the user is on"""
    user_id = models.AuthUser.query.filter_by(email=email).first().id
    picture = models.AuthUser.query.filter_by(email=email).first().picture
    socketio.emit(channel, {"user_id": user_id, "picture": picture}, room=room)
    print("Sent user_id={} to room={}".format(user_id, room))


def emit_all_messages(channel, room):
    """Emits all messages in the database to the clients in the chat room"""
    all_messages = [
        {
            "user": db_message.user,
            "message": db_message.message,
            "timestamp": str(db_message.timestamp),
            "user_id": db_message.user_id,
            "user_pic": db_message.user_pic,
        }
        for db_message in db.session.query(models.Message).all()
    ]

    socketio.emit(channel, {"allMessages": all_messages}, room=room)


@socketio.on("connect")
def on_connect():
    """Client connects to server"""
    print("Someone connected!")
    socketio.emit("connected", {"test": "Connected"})


@socketio.on("disconnect")
def on_disconnect():
    """Client disconnects from server"""
    print("Someone disconnected!")
    socketio.emit("disconnected", {"test": "Disconnected"})
    if "main chat" in flask_socketio.rooms():
        global USER_COUNT
        USER_COUNT -= 1
        print("User count is {}".format(USER_COUNT))
    emit_user_count(USER_COUNT_CHANNEL, "main chat")


@socketio.on("join")
def on_join(data):
    """Adds client to chat room"""
    username = data["username"]
    room = data["room"]
    flask_socketio.join_room(room)
    flask_socketio.send(username + " has entered the room.", room=room)
    global USER_COUNT
    USER_COUNT += 1
    print("user count is {}".format(USER_COUNT))
    emit_user_count(USER_COUNT_CHANNEL, room)
    emit_all_messages(MESSAGES_RECEIVED_CHANNEL, room)


@socketio.on("new facebook user")
def on_new_facebook_user(data):
    """Push facebook user info to database when logging in with Facebook OAuth"""
    print("Got an event for new facebook user input with data:", data)
    push_new_user_to_db(
        models.AuthUserType.FACEBOOK, data["name"], data["email"], data["picture"]
    )
    emit_user_info(USER_INFO_CHANNEL, data["email"], flask.request.sid)


@socketio.on("new google user")
def on_new_google_user(data):
    """Push google user info to database when logging in with Google OAuth"""
    print("Got an event for new google user input with data:", data)
    push_new_user_to_db(
        models.AuthUserType.GOOGLE, data["name"], data["email"], data["picture"]
    )
    emit_user_info(USER_INFO_CHANNEL, data["email"], flask.request.sid)


@socketio.on("new message sent")
def on_new_message(data):
    """When a client sends a new message, add to database, have bot parse message,
    emit all messages"""
    if "main chat" in flask_socketio.rooms():
        print("Got an event for new message with data:", data)
        message = bot.render(data["message"])
        db.session.add(
            models.Message(
                data["user"],
                message,
                data["timestamp"],
                data["user_id"],
                data["user_pic"],
            )
        )
        db.session.commit()

        if bot.is_bot_command(data["message"]):
            reply = bot.bot_reply(data["message"])
            bot_timestamp = datetime.now()
            db.session.add(models.Message("bot", reply, bot_timestamp, 0, bot.BOT_PIC))
            db.session.commit()

        emit_all_messages(MESSAGES_RECEIVED_CHANNEL, "main chat")


@app.route("/")
def chat():
    """Flask renders index"""
    models.db.create_all()
    db.session.commit()

    return flask.render_template("index.html")


if __name__ == "__main__":
    socketio.run(
        app,
        host=os.getenv("IP", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        debug=True,
    )
