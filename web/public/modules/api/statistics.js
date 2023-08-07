import { API_URL, with_params } from './url.js';

export function fetchVisits(start, end) {
	return fetch(with_params(`${API_URL}/statistics/place/visits`, {start, end}))
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch visits!', error));
}