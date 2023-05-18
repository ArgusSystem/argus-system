import { createNavigationBar } from '../components/navbar.js'
import { createCameras } from './cameras/camera_list.js'
import { createFooter } from '../components/footer.js'
import { isSignedIn } from './session.js'
import { Tab } from './tab.js'
import { redirectToIndex } from './routing.js';

window.addEventListener('load', async () => {
    if (!isSignedIn())
        redirectToIndex();

    await createNavigationBar(Tab.LIVE_FEED);

    await createCameras();

    await createFooter();

    document.getElementById('cover').hidden = false;
});