import {SocketClient} from './modules/socket_client.js'
import {setUpDisplay} from './modules/video_display.js'
import {VideoBuffer} from './modules/video_buffer.js'
import {FaceData} from "./modules/face_data.js";


window.addEventListener('load', () => {
    const socketClient = new SocketClient();
    const mediaSource = new MediaSource;
    const faceData = new FaceData();

    const video = document.getElementById('auxiliary-video');
    video.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', (e) => {
        const videoBuffer = new VideoBuffer(mediaSource);
        let hasPreBuffer = false;

        socketClient.onVideoChunk((chunk) => {
            videoBuffer.append(chunk);

            if (hasPreBuffer && video.paused) {
                video.play();
            }

            hasPreBuffer = true
        });

        socketClient.onFace((face) => {
            faceData.update(face);
        });

        setUpDisplay(videoBuffer, faceData);
    })
});

