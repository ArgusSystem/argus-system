import { onSightings } from './sightings.js'
import { toTimestamp } from '../format.js';

const {protocol, hostname} = window.location;

function buildURL() {
    const endpoint = new URL(`${protocol}//${hostname}:5000/history`);

    const dateRange = $('#history-range').data('daterangepicker');

    const params = {
        'person_id': $('#select-person').select2('data')[0].id,
        'from_date': toTimestamp(dateRange.startDate),
        'to_date': toTimestamp(dateRange.endDate) + 999 // Add milliseconds to complete day
    }

    endpoint.search = new URLSearchParams(params).toString();

    return endpoint;
}

function search(endpoint) {
    return fetch(endpoint)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch people!', error));
}

export function loadSearchSubmit(cameras) {
    document.getElementById('submit-filter').onclick = () => {
        const endpoint = buildURL();
        search(endpoint).then(data => {
            onSightings(cameras, data);
        });
    };
}