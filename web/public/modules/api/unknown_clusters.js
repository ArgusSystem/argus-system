import { API_URL, with_params } from './url.js';

export function fetchUnknownClusters(count) {
    return fetch(with_params(`${API_URL}/unknown_clusters`, {count}))
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch unknown clusters!', error));
}
