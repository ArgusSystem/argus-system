import { API_URL } from './url.js'

export async function authorizeUser(username, password) {
    const endpoint = new URL(`${API_URL}/users/${username}`);
    endpoint.search = new URLSearchParams({password}).toString();

    return fetch(endpoint).then(async (response) => {
        const text = await response.text();

        return (response.ok) ? text : new Error(text);
    });
}