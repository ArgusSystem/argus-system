import { onSightings } from './sightings.js'

const {protocol, hostname} = window.location;

const DATE_FORMAT = 'DD/MM/YYYY';

function buildURL() {
    const endpoint = new URL(`${protocol}//${hostname}:5000/history`);

    const dateRange = $('#history-range').data('daterangepicker');

    const params = {
        'person_id': $('#select-person').select2('data')[0].id,
        'from_date': dateRange.startDate.format(DATE_FORMAT),
        'to_date': dateRange.endDate.format(DATE_FORMAT)
    }

    endpoint.search = new URLSearchParams(params).toString();

    return endpoint;
}

function search(endpoint) {
    return fetch(endpoint)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch people!', error));
}

export function loadFilterSubmit(cameras) {
    $("#filter-form").submit(function(e) {
        e.preventDefault();

        const endpoint = buildURL();
        search(endpoint).then(data => {
            onSightings(cameras, data);
        });
    });
}