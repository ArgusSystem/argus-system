import { API_URL } from './url.js';

const BASE_URL = `${API_URL}/people`;

export function fetchPeople() {
    return fetch(BASE_URL)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch people!', error));
}

export function getPersonPhotoURL(personId, photoId) {
	return `${BASE_URL}/${personId}/photos/${photoId}`;
}

export function getLastSeenPhotoURL(photoId) {
	return `${BASE_URL}/last_seen/${photoId}`;
}

