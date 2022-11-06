import {fetchCameras} from './history/cameras.js';
import { fetchPeople } from './history/people.js';
import { loadTimeRange } from './history/timeRange.js';
import { loadSearchSubmit } from './history/search.js';


$(document).ready(async () => {
	const cameras = {};
	await fetchCameras()
		.then(data => data.forEach(camera => cameras[camera.id] = camera));

	await fetchPeople()
		.then(data => $('.select-person').select2({placeholder: "Person's name", data: data}));

	loadTimeRange();

	loadSearchSubmit(cameras);
});

