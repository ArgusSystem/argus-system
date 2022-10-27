import {SocketClient} from './modules/socket_client.js'
import {setUpDisplay} from './modules/video_display.js'
import {VideoBuffer} from './modules/video_buffer.js'
import {FacesIndex} from './modules/faces_index.js';
import {VideoIndex} from "./modules/video_index.js";
import { VideoInterpolator } from './modules/video_interpolator.js'


const PRE_BUFFERED_THRESHOLD = 10;

window.addEventListener('load', () => {
    const socketClient = new SocketClient();
    const mediaSource = new MediaSource;


    const video = document.getElementById('auxiliary-video');
    video.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', (e) => {
        const videoBuffer = new VideoBuffer(mediaSource);
        const facesIndex = new FacesIndex();
        const videoIndex = new VideoIndex();
        const videoInterpolator = new VideoInterpolator(videoIndex, facesIndex);
        let preBuffered = 0;

        socketClient.onChunk(chunk => {
            videoBuffer.append(chunk);
            videoIndex.add(chunk);

            console.log('Total processing time of %s-%d: %d ms', chunk.cameraId, chunk.timestamp, Date.now() - chunk.timestamp);

            if (preBuffered >= PRE_BUFFERED_THRESHOLD && video.paused) {
                video.play();
            }

            preBuffered += chunk.duration;
        });

        socketClient.onFace(face => facesIndex.add(face));

        setUpDisplay(videoInterpolator);
    })
});

