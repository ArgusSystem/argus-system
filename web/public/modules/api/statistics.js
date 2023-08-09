import { API_URL, with_params } from './url.js';

const BASE_URL = `${API_URL}/statistics/place`;

export function fetchVisits(start, end) {
	return fetch(with_params(`${BASE_URL}/visits`, {start, end}))
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch visits!', error));
}

export function fetchWeekDayHistogram(camera, start, end) {
	return fetch(with_params(`${BASE_URL}/${camera}/week_histogram`, {start, end}))
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch weekday histogram!', error));
}