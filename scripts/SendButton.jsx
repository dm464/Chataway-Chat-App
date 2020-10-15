import * as React from 'react';
import { Socket } from './Socket';

function handleSubmit(event) {
    let user = document.getElementById("user");
    let newMessage = document.getElementById("typedMessage");

    console.log('User sent new message: ', newMessage);
    
    Socket.emit("new message sent", {"user": user.value, "message": newMessage.value});
    
    console.log('Sent the message \'' + newMessage.value + '\' to server!');
    newMessage.value = ''
    user.value = ''
    
    event.preventDefault();
}

export function SendButton() {
    return (
        <form onSubmit={handleSubmit}>
            <input id="user"></input>
            <input id="typedMessage" placeholder="Type a message..."></input>
            <button>Send</button>
        </form>
    );
}