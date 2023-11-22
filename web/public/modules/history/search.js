import { onSightings } from './sightings.js'
import { toTimestamp } from '../format.js';
import { API_URL } from '../api/url.js'

const {protocol, hostname} = window.location;

function buildURL() {
    const endpoint = new URL(`${API_URL}/history`);

    const dateRange = $('#history-range').data('daterangepicker');

    const params = {
        'person_id': $('#select-person').select2('data')[0].id,
        'from_date': toTimestamp(dateRange.startDate),
        'to_date': toTimestamp(dateRange.endDate) + 999 // Add milliseconds to complete day
    };

    endpoint.search = new URLSearchParams(params).toString();

    return endpoint;
}

function search(endpoint) {
    return fetch(endpoint)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch people!', error));
}

export async function loadSearchSubmit(cameras) {
    document.getElementById('submit-filter').onclick = async () => {
        const endpoint = buildURL();
        const data = await search(endpoint);
        await onSightings(cameras, data);
    };
}