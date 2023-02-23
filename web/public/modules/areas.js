import { createNavigationBar, Tab } from '../components/navbar.js'
import { createAreaTypesList } from './areas/area_types.js'
import { createAreasList } from './areas/areas.js'
import { createCamerasList } from './cameras/cameras.js'

window.addEventListener('load', async () => {
	await createNavigationBar(Tab.AREAS);

    await createAreaTypesList();
    await createAreasList();
    await createCamerasList();

    document.getElementById('cover').hidden = false;
});