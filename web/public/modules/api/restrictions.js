import { API_URL } from './url.js';
import { post, remove } from './utils.js';

const BASE_URL = `${API_URL}/restrictions`;

function restriction_url(id) {
	return `${BASE_URL}/${id}`;
}

export function fetchRestrictions() {
    return fetch(BASE_URL)
		.then(response => response.json())
		.catch(error => console.error('Failed to fetch restriction!', error));
}

export function insertRestriction(role, area_type, severity, time_start, time_end) {
    return post(BASE_URL, {role, area_type, severity, time_start, time_end})
		.catch(error => console.error('Failed to create restrictions!', error));
}

export function updateRestriction(id, role, area_type, severity, time_start, time_end) {
	return post(restriction_url(id), {role, area_type, severity, time_start, time_end})
		.catch(error => console.error('Failed to update restriction!', error));
}

export function deleteRestriction(id) {
	return remove(restriction_url(id))
		.catch(error => console.error('Failed to remove restriction!', error));
}