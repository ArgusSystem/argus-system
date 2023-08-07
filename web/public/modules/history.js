import {fetchCameras} from './api/cameras.js';
import { fetchPeople } from './api/people.js';
import { loadTimeRange } from './history/time-range.js';
import { loadSearchSubmit } from './history/search.js';
import { Tab } from './tab.js'
import { toSelect } from '../components/select2.js';
import { loadPage } from './page.js';


loadPage(Tab.HISTORY, async () => {
	const cameras = await fetchCameras().then(data => data.reduce((accumulator, camera) => {
		accumulator[camera.id] = camera;
		return accumulator;
	}, {}));

	await fetchPeople()
		.then(data => $('.select-person').select2({placeholder: "Person's name", data: toSelect(data)}));

	loadTimeRange('history-range');
	loadSearchSubmit(cameras);
});

