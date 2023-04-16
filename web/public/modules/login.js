import { isSignedIn, signIn } from './session.js'
import { authorizeUser } from './api/users.js'
import { Tab } from './tab.js'
import { redirectToTab } from './routing.js';

window.addEventListener('load', () => {
    document.getElementById('log-in').onsubmit = (event) => {
        event.preventDefault();

        const data = event.target;

        authorizeUser(data.username.value, data.password.value)
            .then(username => {
                signIn(username);
                redirectToTab(Tab.HOME);
            })
            .catch(console.log);
    };

    if (isSignedIn())
        redirectToTab(Tab.HOME);
})