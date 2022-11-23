import { createNavigationBar, Tab } from '../components/navbar.js'
import { createCameras } from './cameras/camera_list.js'

window.addEventListener('load', async () => {
    await createNavigationBar(Tab.LIVE_FEED);

    await createCameras();

    document.getElementById('cover').hidden = false;
});