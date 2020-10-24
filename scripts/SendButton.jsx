import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let user = document.getElementById("user");
    let newMessage = document.getElementById("typed_message");
    var date = new Date();

    console.log('User sent new message: ', newMessage, ' at ', date);
    Socket.emit("new message sent", {"user": user.value, "message": newMessage.value, "timestamp": date});
    
    console.log('Sent the message \'' + newMessage.value + '\' to server!');
    newMessage.value = ''
    user.value = ''
    event.preventDefault();
}

export function SendButton() {
    return (
        <form onSubmit={handleSubmit}>
            <input id="user" placeholder="Username"></input><br></br>
            <input id="typed_message" placeholder="Type a message..."></input><br></br>
            <button id="send-button"><i class="material-icons">send</i>Send</button>
        </form>
    );
}