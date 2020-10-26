import * as React from 'react';
import { Socket } from './Socket';

var user_id = 0;
Socket.on("current user info", getUserId);
function getUserId(data) {
    user_id = data["user_id"];
}

function handleSubmit(event) {
    let user = document.getElementById("user");
    let newMessage = document.getElementById("typed_message");
    var date = new Date();

    console.log('User sent new message: ', newMessage, ' at ', date);
    Socket.emit("new message sent", {"user": user.value, "message": newMessage.value, "timestamp": date, "user_id": user_id});
    
    console.log('Sent the message \'' + newMessage.value + '\' to server!');
    newMessage.value = '';
    event.preventDefault();
}

export function SendButton() {
    return (
        <form onSubmit={handleSubmit} id="input_log">
            <input id="user" placeholder="Username" readonly="true" ></input><br></br>
            <input id="typed_message" placeholder="Type a message..."></input><br></br>
            <button id="send-button"><i class="material-icons">send</i>Send</button>
        </form>
    );
}