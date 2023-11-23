import { params } from './api/params.js'
import { fetchCamera } from './api/cameras.js'
import { VideoSource } from './video/video_source.js';
import { Tab } from './tab.js'
import { loadPage } from './page.js';
import { calculateScalingFactor } from './video/utils.js';

loadPage(Tab.LIVE_FEED, async () => {
    let cameras = [];

    if (params.camera)
        cameras.push(await fetchCamera(params.camera));
    else
        for (const camera of params.cameras.split(','))
            cameras.push(await fetchCamera(camera));

    document.getElementById('camera-name').innerText = cameras.map(camera => camera.name).join(' - ');

    const videosContainer = document.getElementById('videos-container');

    const scalingFactor = calculateScalingFactor(cameras.length);

    for (const camera of cameras) {
        const videoSource = new VideoSource(camera, scalingFactor);

        videosContainer.appendChild(videoSource.video);
        videosContainer.appendChild(videoSource.canvas);

        videoSource.start();
    }
});
