import * as React from 'react';
import { Socket } from './Socket';
import GoogleLogin from 'react-google-login';

function handleGoogleOAuthLogin(response) {
    console.log(response);
    let name = response.profileObj.name;
    let email = response.profileObj.email;
    let picture = response.profileObj.imageUrl;
    Socket.emit('new google user', {
        'name': name,
        'email': email,
        'picture': picture
    });
    
    console.log('Sent the name ' + name + ' to server!');
}

function GoogleOAuthFailed(response) {
    console.log("failed" + response);
}

export function GoogleButton() {
    return (
        <GoogleLogin
        clientId="387589797855-drpmn0itocbndb0e1bab8ihqr4isbhd2.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={handleGoogleOAuthLogin}
        onFailure={GoogleOAuthFailed}
        cookiePolicy={'single_host_origin'}
        isSignedIn={false} />
    );
}