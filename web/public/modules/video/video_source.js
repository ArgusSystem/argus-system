import { SocketClient } from './socket_client.js'
import { setUpDisplay } from './video_display.js'
import { VideoBuffer } from './video_buffer.js'
import { FacesIndex } from './faces_index.js';
import { VideoIndex } from "./video_index.js";
import { VideoInterpolator } from './video_interpolator.js'

const PRE_BUFFERED_THRESHOLD = 5;

export function createVideo(camera) {
    const socketClient = new SocketClient(camera.name);
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

        setUpDisplay(camera, videoInterpolator);
    });
}