import { createCameras } from './cameras/camera_list.js'
import { Tab } from './tab.js'
import { loadPage, Page } from './page.js';
import { fetchCameras } from './api/cameras.js';
import { redirect } from './routing.js';


loadPage(Tab.LIVE_FEED, async () => {
    const cameras = await fetchCameras();

    await createCameras(cameras);

    document.getElementById('all-cameras').onclick = () => {
      redirect(Page.VIDEO, {cameras: cameras.map(camera => camera.id)});
    };
});