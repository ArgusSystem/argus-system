import { API_URL } from './url.js'

export function fetchAreaTypes() {
    return fetch(`${API_URL}/area_types`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch area_types!', error));
}