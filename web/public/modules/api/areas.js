import { API_URL } from './url.js'

export function fetchAreas() {
    return fetch(`${API_URL}/areas`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch areas!', error));
}