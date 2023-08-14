import { API_URL, with_params } from './url.js';

const BASE_URL = `${API_URL}/statistics/place`;

function detail_url(camera) {
	return `${BASE_URL}/${camera}`;
}

export function fetchVisits(start, end) {
	return fetch(with_params(`${BASE_URL}/visits`, {start, end}))
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch visits!', error));
}

export function fetchWeekDayHistogram(camera, start, end) {
	return fetch(with_params(`${detail_url(camera)}/week_histogram`, {start, end}))
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch weekday histogram!', error));
}

export function fetchAvgTimeSpent(camera, start, end) {
		return fetch(with_params(`${detail_url(camera)}/avg_time_spent`, {start, end}))
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch average time spent!', error));
}

export function fetchTrespassers(camera, start, end) {
		return fetch(with_params(`${detail_url(camera)}/trespassers`, {start, end}))
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch trespassers count!', error));
}

export function fetchConcurrentVisits(camera, start, end) {
		return fetch(with_params(`${detail_url(camera)}/concurrent_visits`, {start, end}))
			.then(response => response.json())
			.catch(error => console.error('Failed to fetch concurrent visits count!', error));
}