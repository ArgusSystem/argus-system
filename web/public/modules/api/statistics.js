import { API_URL } from './url.js';

export function fetchVisits() {
	return fetch(`${API_URL}/statistics/place/visits`)
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch visits!', error));
}