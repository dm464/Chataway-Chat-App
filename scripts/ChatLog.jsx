import * as React from 'react';

import { SendButton } from './SendButton';
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
            <h1>Chat Bot!</h1>
                <ul>
                    {
                    // TODO -- display all addresses
                        messages.map(
                            (message, index) => <li key={index}>{message}</li>)
                    }
                </ul>
            <SendButton />
        </div>
    );
}