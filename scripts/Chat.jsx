import * as React from 'react';

import { SendButton } from './SendButton';
import { UserCount } from './UserCount';
import { Login } from './Login';
import { Socket } from './Socket';
import { Markup } from 'interweave';

var user_id = 0;
Socket.on("current user info", getUserId);
function getUserId(data) {
    user_id = data["user_id"];
}

export function Chat() {
    const [messages, setMessages] = React.useState([]);

    function getNewMessages() {
        React.useEffect(() => {
            Socket.on('messages received', updateMessages);
            return () => {
                Socket.off('messages received', updateMessages);
            }
        });
    }
    
    function updateMessages(data) {
        console.log("Received all messages from server");
        setMessages(data['allMessages']);
    }
    
    getNewMessages();

    return (
        <div>
            <h1>CHATAWAY</h1>
            <div class="chat_box">
                <div class="chat_log">
                    <ul>
                    {
                        messages.map(
                            (message, index) => 
                            <li key={index} class="message">
                            <div class="message_box" id={"id_"+(message['user_id'] == user_id? "me":message['user_id'])}>
                                <div class="message_user">
                                    <img src={message['user_pic']} class="sender_pic"></img>
                                    {message['user']}
                                </div>
                                <Markup content={message['message']} />
                            </div>
                            <div class={`timestamp id_${(message['user_id'] == user_id? "me":message['user_id'])}`}>{message['timestamp']}</div>
                            </li>)
                    }
                    </ul>
                </div>
                <SendButton />
                <UserCount />
                <Login />
            </div>
        </div>
    );
}