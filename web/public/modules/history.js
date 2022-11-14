import {fetchCameras} from './api/cameras.js';
import { fetchPeople } from './api/people.js';
import { loadTimeRange } from './history/timeRange.js';
import { loadSearchSubmit } from './history/search.js';
import { createNavigationBar, Tab } from '../components/navbar.js'


window.addEventListener('load', async () => {
	await createNavigationBar(Tab.HISTORY);

	const cameras = {};
	await fetchCameras()
		.then(data => data.forEach(camera => cameras[camera.id] = camera));

	await fetchPeople()
		.then(data => $('.select-person').select2({placeholder: "Person's name", data: data}));

	loadTimeRange();

	loadSearchSubmit(cameras);

	document.getElementById('cover').hidden = false;
});

