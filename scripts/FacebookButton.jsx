import * as React from 'react';
import { Socket } from './Socket';
import FacebookLogin from 'react-facebook-login';

function handleFacebookOAuthLogin(response) {
    console.log(response);
    let name = response.name;
    let email = response.email;
    let picture = response.picture.data.url;
    Socket.emit('new facebook user', {
        'name': name,
        'email': email,
        'picture': picture
    });
        Socket.emit('join', {
        'username': name,
        'room': 'main chat'
    });
    
    console.log('Sent the name ' + name + ' to server!');
}

export function FacebookButton() {
    return (
        <FacebookLogin
        appId="379610306412942"
        autoLoad={false}
        fields="name,email,picture"
        callback={handleFacebookOAuthLogin}  />
    );
}