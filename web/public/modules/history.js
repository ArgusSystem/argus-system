import {fetchCameras} from './api/cameras.js';
import { fetchPeople } from './api/people.js';
import { loadTimeRange } from './history/time-range.js';
import { loadSearchSubmit } from './history/search.js';
import { createNavigationBar } from '../components/navbar.js'
import { createFooter } from '../components/footer.js'
import { isSignedIn } from './session.js'
import { Tab } from './tab.js'
import { redirectToIndex } from './routing.js';
import { toSelect } from '../components/select2.js';



window.addEventListener('load', async () => {
	if (!isSignedIn())
        redirectToIndex();

	await createNavigationBar(Tab.HISTORY);

	const cameras = {};
	await fetchCameras()
		.then(data => data.forEach(camera => cameras[camera.id] = camera));

	await fetchPeople()
		.then(data => $('.select-person').select2({placeholder: "Person's name", data: toSelect(data)}));

	loadTimeRange();

	loadSearchSubmit(cameras);

	await createFooter();

	document.getElementById('cover').hidden = false;
});

