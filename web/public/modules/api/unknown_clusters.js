import { API_URL } from './url.js'

export function fetchUnknownClusters() {
    return fetch(`${API_URL}/unknown_clusters`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch unknown clusters!', error));
}
