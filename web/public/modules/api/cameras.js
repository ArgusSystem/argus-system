import { API_URL } from './url.js'

export function fetchCameras() {
	return fetch(`${API_URL}/cameras`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch people!', error));
}
