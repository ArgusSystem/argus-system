import { API_URL, MAIN_URL } from './api/url.js'

function redirect() {
    window.location.replace(`${MAIN_URL}/home.html`);
}

window.addEventListener('load', () => {
    document.getElementById('log-in').onsubmit = (event) => {
        event.preventDefault();

        const data = event.target;
        const endpoint = new URL(`${API_URL}/users/${data.username.value}`);
        endpoint.search = new URLSearchParams({password: data.password.value}).toString();

        fetch(endpoint)
            .then(response => {
                response.text().then(text => {
                    if (response.ok) {
                        localStorage.setItem('username', text);
                        redirect();
                    } else {
                        console.log(text);
                    }
                })
            });
    };

    if (localStorage.getItem('username'))
        redirect();
})