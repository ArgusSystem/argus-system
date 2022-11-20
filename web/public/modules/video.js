import { createNavigationBar, Tab } from '../components/navbar.js'
import { params } from './api/params.js'
import { fetchCamera } from './api/cameras.js'
import { createVideo } from './video/video_source.js'


window.addEventListener('load', async () => {
    await createNavigationBar(Tab.LIVE_FEED);

    const camera = await fetchCamera(params.camera)

    document.getElementById('camera-name').innerText = camera.name;

    createVideo(camera);

    document.getElementById('cover').hidden = false;
});

