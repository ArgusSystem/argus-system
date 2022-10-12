import {SocketClient} from './modules/socket_client.js'
import {setUpDisplay} from './modules/video_display.js'
import {VideoBuffer} from './modules/video_buffer.js'
import {FaceData} from "./modules/face_data.js";


const PRE_BUFFERED_THRESHOLD = 10;

window.addEventListener('load', () => {
    const socketClient = new SocketClient();
    const mediaSource = new MediaSource;
    const faceData = new FaceData();

    const video = document.getElementById('auxiliary-video');
    video.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', (e) => {
        const videoBuffer = new VideoBuffer(mediaSource);
        let preBuffered = 0;

        socketClient.onVideoChunk((chunk) => {
            videoBuffer.append(chunk);

            if (preBuffered >= PRE_BUFFERED_THRESHOLD && video.paused) {
                video.play();
            }

            preBuffered += chunk.duration;
        });

        socketClient.onFace((face) => {
            faceData.update(face);
        });

        setUpDisplay(videoBuffer, faceData);
    })
});

