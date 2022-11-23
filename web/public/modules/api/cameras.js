import { API_URL } from './url.js'

export async function fetchCameras() {
	return fetch(`${API_URL}/cameras`)
		.then(response => response.json())
		.catch(error => console.error('Failed to fetch cameras!', error));
}

export async function fetchCamera(camera_id) {
	return fetch(`${API_URL}/cameras/${camera_id}`)
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch camera!', error));
}
