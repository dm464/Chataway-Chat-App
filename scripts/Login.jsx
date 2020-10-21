import * as React from 'react';

import { GoogleButton } from './GoogleButton';
import { FacebookButton } from './FacebookButton';
//import { InstagramButton } from './InstagramButton';
//import { TwitterButton } from './TwitterButton';
import { Socket } from './Socket';


/*function handleSubmit(event) {
    let user = document.getElementById("user");
    let newMessage = document.getElementById("typed_message");

    console.log('User sent new message: ', newMessage);
    
    Socket.emit("new message sent", {"user": user.value, "message": newMessage.value});
    
    console.log('Sent the message \'' + newMessage.value + '\' to server!');
    newMessage.value = ''
    user.value = ''
    event.preventDefault();
}*/

export function Login() {
    const [accounts, setAccounts] = React.useState([]);
    
    function getAllAccounts() {
        React.useEffect(() => {
            Socket.on('accounts received', (data) => {
                let allAccounts = data['allAccounts'];
                console.log("Received accounts from server: " + allAccounts);
                setAccounts(allAccounts);
            })
        });
    }
    
    //getAllAccounts();
    
    // TODO use these accounts for something
    
    return (
        <div class="form-popup" id="login-form">
        <FacebookButton />
        <GoogleButton />
        </div>
    );
}