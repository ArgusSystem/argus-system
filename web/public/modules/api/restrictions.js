import { API_URL } from './url.js'

export function fetchRestrictions() {
    return fetch(`${API_URL}/restrictions`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch restrictions!', error));
}