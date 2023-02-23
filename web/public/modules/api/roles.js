import { API_URL } from './url.js'

export function fetchRoles() {
    return fetch(`${API_URL}/roles`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch roles!', error));
}