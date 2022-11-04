import {fetchCameras} from './history/cameras.js'
import { fetchPeople } from './history/people.js'
import { loadTimeRange } from './history/timeRange.js'
import { loadFilterSubmit } from './history/search.js'


$(document).ready(async () => {
	const cameras = {};
	await fetchCameras()
		.then(data => data.forEach(camera => cameras[camera.id] = camera));

	await fetchPeople()
		.then(data => $('.select-person').select2({placeholder: "Person's name", data: data}));

	loadTimeRange();

	loadFilterSubmit(cameras);

	const map = L.map('map').setView([51.505, -0.09], 13);

	const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	}).addTo(map);
});

