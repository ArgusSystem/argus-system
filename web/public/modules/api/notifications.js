import { API_URL, with_params } from './url.js';

const BASE_URL = `${API_URL}/notifications`

function notifications_url(username) {
	return `${BASE_URL}/${username}`;
}
export function fetchNotifications(username, count) {
    return fetch(with_params(notifications_url(username), {count}))
		.then(response => response.json())
		.catch(error => console.error('Failed to fetch notifications!', error));
}

export function fetchNotificationsCount(username) {
    return fetch(`${notifications_url(username)}/count`,)
		.then(response => response.text())
		.catch(error => console.error('Failed to fetch notifications count!', error));
}

