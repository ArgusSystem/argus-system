import { API_URL } from './url.js';

const BASE_URL = `${API_URL}/restriction_severities`;

export function fetchRestrictionSeverities() {
    return fetch(BASE_URL)
		.then(response => response.json())
		.catch(error => console.error('Failed to fetch restriction severities!', error));
}