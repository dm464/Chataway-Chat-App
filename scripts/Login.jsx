import * as React from 'react';

import { GoogleButton } from './GoogleButton';
import { FacebookButton } from './FacebookButton';
//import { InstagramButton } from './InstagramButton';
//import { TwitterButton } from './TwitterButton';
import { Socket } from './Socket';


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
    
    function openForm(event) {
        document.getElementById("modal").style.display = "block";
        console.log("Open form");
    }
    
    function closeModal(event) {
        document.getElementById("modal").style.display = "none";
    }
    
    return (
        <div id="login-section">
            <button id="login-button" onClick={openForm}>Sign In</button>
            <div id="modal">
                <div id="popup-signin" >
                    <span id="close" onClick={closeModal}>&times;</span>
                    <FacebookButton />
                    <GoogleButton />
                </div>
            </div>
        </div>
    );
}