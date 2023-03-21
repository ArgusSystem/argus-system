import { isSignedIn, signIn } from './session.js'
import { authorizeUser } from './api/users.js'
import { redirectToTab, Tab } from './tab.js'

window.addEventListener('load', () => {
    document.getElementById('log-in').onsubmit = (event) => {
        event.preventDefault();

        const data = event.target;

        // TODO: Validate if it works
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