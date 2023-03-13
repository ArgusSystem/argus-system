import { API_URL, MAIN_URL } from './api/url.js'

window.addEventListener('load', () => {
    document.getElementById('log-in').onsubmit = (event) => {
        event.preventDefault();

        const data = event.target;
        const endpoint = new URL(`${API_URL}/users/${data.username.value}`);
        endpoint.search = new URLSearchParams({password: data.password.value}).toString();

        fetch(endpoint)
            .then(response => response.text())
            .then(username => {
                localStorage.setItem('username', username);
                window.location.replace(MAIN_URL);
            })
            .catch(error => {
                // TODO: Show the error
                console.log(error)
            });
    };
})