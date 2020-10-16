import * as React from 'react';

import { Socket } from './Socket';

export function UserCount() {
    const [currentUsers, setUsers] = React.useState(0);
    
    function addUser() {
        React.useEffect(() => {
            Socket.on('user added/dropped', updateCount);
            return () => {
                Socket.off('user added/dropped', updateCount);
            }
        });
    }
    function updateCount(data) {
        console.log("There are " + data['user_count'] + " users in server");
        setUsers(data['user_count']);
    }
    
    addUser();

    return (
        <div>
            <div>Users Online: {currentUsers}</div>
        </div>
    );
}