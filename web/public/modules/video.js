import {SocketClient} from './video/socket_client.js'
import {setUpDisplay} from './video/video_display.js'
import {VideoBuffer} from './video/video_buffer.js'
import {FacesIndex} from './video/faces_index.js';
import {VideoIndex} from "./video/video_index.js";
import { VideoInterpolator } from './video/video_interpolator.js'


const PRE_BUFFERED_THRESHOLD = 2;

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

            preBuffered += chunk.duration;

            if (preBuffered >= PRE_BUFFERED_THRESHOLD && video.paused) {
                video.play();
            }
        });

        socketClient.onFace(face => facesIndex.add(face));

        setUpDisplay(videoInterpolator);
    });
});
