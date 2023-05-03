import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import './index.css';
import {getAccessToken} from './utils';

// Kicks off the app after the user "logs in":
async function renderApp() {
    const token = await getAccessToken('webdev', 'password');
    
    ReactDOM.render(
        <App token={token} />,
        document.getElementById('root')
    );
}

renderApp();