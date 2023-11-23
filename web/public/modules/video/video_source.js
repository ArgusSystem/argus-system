import { SocketClient } from './socket_client.js'
import { setUpDisplay } from './video_display.js'
import { VideoBuffer } from './video_buffer.js'
import { FacesIndex } from './faces_index.js';
import { VideoIndex } from "./video_index.js";
import { VideoInterpolator } from './video_interpolator.js'
import { createCanvasElement, createVideoElement } from './utils.js';

const PRE_BUFFERED_THRESHOLD = 5;

export class VideoSource {
    constructor (camera, scalingFactor) {
        this.video = createVideoElement(camera, scalingFactor);
        this.canvas = createCanvasElement(camera, scalingFactor);
        this.socketClient = new SocketClient(camera.name);
        this.scalingFactor = scalingFactor;
    }

    start() {
        const video = this.video;
        const canvas = this.canvas;
        const socketClient = this.socketClient;
        const scalingFactor = this.scalingFactor;

        const mediaSource = new MediaSource;

        video.src = URL.createObjectURL(mediaSource);

        mediaSource.addEventListener('sourceopen', (e) => {
            const videoBuffer = new VideoBuffer(mediaSource);
            const facesIndex = new FacesIndex();
            const videoIndex = new VideoIndex();
            const videoInterpolator = new VideoInterpolator(videoIndex, facesIndex);
            let preBuffered = 0;

            socketClient.onChunk(async chunk => {
                videoBuffer.append(chunk);
                videoIndex.add(chunk);

                preBuffered += chunk.duration;

                if (preBuffered >= PRE_BUFFERED_THRESHOLD && video.paused) {
                    await video.play();
                }
            });

            socketClient.onFace(face => facesIndex.add(face));

            setUpDisplay(video, canvas, scalingFactor, videoInterpolator);
        });
    }
}