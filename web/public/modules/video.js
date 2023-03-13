import { createNavigationBar } from '../components/navbar.js'
import { params } from './api/params.js'
import { fetchCamera } from './api/cameras.js'
import { createVideo } from './video/video_source.js'
import { createFooter } from '../components/footer.js'
import { isSignedIn } from './session.js'
import { redirectToIndex, Tab } from './tab.js'


window.addEventListener('load', async () => {
    if (!isSignedIn())
        redirectToIndex();

    await createNavigationBar(Tab.LIVE_FEED);

    const camera = await fetchCamera(params.camera)

    document.getElementById('camera-name').innerText = camera.name;

    createVideo(camera);

    await createFooter();

    document.getElementById('cover').hidden = false;
});

