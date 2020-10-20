import * as React from 'react';

import { SendButton } from './SendButton';
import { UserCount } from './UserCount';
import { Socket } from './Socket';

export function ChatLog() {
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
        console.log("Received messages from server: " + data['allMessages']);
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
                        // TODO -- display all addresses
                            messages.map(
                                (message, index) =>
                                <li key={index} class="message"><div class="message_box" id={message['user']}>
                                {message['user']} - {message['message']}</div></li>)
                        }
                    </ul>
                </div>
                <SendButton />
                <UserCount />
            </div>
        </div>
    );
}