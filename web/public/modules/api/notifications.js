import { API_URL } from './url.js';

const BASE_URL = `${API_URL}/notifications`

function notifications_url(username) {
	return `${BASE_URL}/${username}`;
}
export function fetchNotifications(username) {
    return fetch(notifications_url(username))
		.then(response => response.json())
		.catch(error => console.error('Failed to fetch notifications!', error));
}
