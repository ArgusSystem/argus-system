import { API_URL } from './url.js'

export function fetchPeople() {
    return fetch(`${API_URL}/people`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch people!', error));
}
