import { API_URL, with_params } from './url.js';

const BASE_URL = `${API_URL}/unknown_clusters`;

export function fetchUnknownClusters(count) {
    return fetch(with_params(BASE_URL, {count}))
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch unknown clusters!', error));
}

export function fetchClusterFaces(id) {
    return fetch(`${BASE_URL}/${id}/faces`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch unknown clusters!', error));
}

