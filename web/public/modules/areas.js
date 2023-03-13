import { createNavigationBar } from '../components/navbar.js'
import { createAreaTypesList } from './areas/area_types.js'
import { createAreasList } from './areas/areas.js'
import { createCamerasList } from './cameras/cameras.js'
import { isSignedIn } from './session.js'
import { redirectToIndex, Tab } from './tab.js'

window.addEventListener('load', async () => {
    if (!isSignedIn())
        redirectToIndex();

	await createNavigationBar(Tab.AREAS);

    await createAreaTypesList();
    await createAreasList();
    await createCamerasList();

    document.getElementById('cover').hidden = false;
});