import * as React from 'react';
import { Socket } from './Socket';
import GoogleLogin from 'react-google-login';

function handleGoogleOAuthLogin(response) {
    console.log(response.profileObj.name + ' logged in successfully');
    let name = response.profileObj.name;
    let email = response.profileObj.email;
    let picture = response.profileObj.imageUrl;
    Socket.emit('new google user', {
        'name': name,
        'email': email,
        'picture': picture
    });
    Socket.emit('join', {
        'username': name,
        'room': 'main chat'
    });
    document.getElementById("modal").style.display = "none";
    document.getElementById("input_log").style.display = "block";
    document.getElementById("online_user_count").style.display = "block";
    document.getElementById("user").value = name;

    console.log('Sent the name ' + name + ' to server!');
}

function GoogleOAuthFailed(response) {
    console.log("failed" + response);
}

export function GoogleButton() {
    return (
        <GoogleLogin
        clientId="1087078822501-d1a06225qo91k5skea3m4698eu4r4jv3.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={handleGoogleOAuthLogin}
        onFailure={GoogleOAuthFailed}
        cookiePolicy={'single_host_origin'}
        isSignedIn={false} />
    );
}