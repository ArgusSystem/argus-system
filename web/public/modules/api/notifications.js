import { API_URL, with_params } from './url.js';

const BASE_URL = `${API_URL}/notifications`

function id_url(id) {
	return `${BASE_URL}/id/${id}`;
}

function username_url(username) {
	return `${BASE_URL}/user/${username}`;
}

export function fetchNotification(id) {
	return fetch(`${id_url(id)}`)
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch notification!', error));
}

export function markNotificationRead(id) {
	return fetch(`${id_url(id)}/read`, {method:'POST'})
			.catch(error => console.error('Failed to mark notification as read!', error));
}

export function fetchNotifications(username, count) {
    return fetch(with_params(username_url(username), {count}))
		.then(response => response.json())
		.catch(error => console.error('Failed to fetch notifications!', error));
}

export function fetchNotificationsCount(username) {
    return fetch(`${username_url(username)}/count`,)
		.then(response => response.text())
		.catch(error => console.error('Failed to fetch notifications count!', error));
}

