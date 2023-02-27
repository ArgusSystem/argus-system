import { createNavigationBar, Tab } from '../components/navbar.js'
import { createCameras } from './cameras/camera_list.js'
import { createFooter } from '../components/footer.js'

window.addEventListener('load', async () => {
    await createNavigationBar(Tab.LIVE_FEED);

    await createCameras();

    await createFooter();

    document.getElementById('cover').hidden = false;
});