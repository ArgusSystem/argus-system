import { Queue } from './queue.js'

const MIME = 'video/mp4; codecs="avc1.f4001f"';
const INTERVAL = 100; // ms

export class VideoBuffer {
    constructor(mediaSource) {
        this.sourceBuffer = mediaSource.addSourceBuffer(MIME);
        this.sourceBuffer.mode = 'sequence';
        this.sourceBuffer.addEventListener('error', function (e) {
            console.log(e);
        });

        /**
         * Need a pre buffer queue to avoid writing when the new chunk event is triggered.
         * Event callbacks should be fast and writes to video buffer aren't always as fast as new events are
         * received.
         *
         * Logic uses a busy waiting loop to check for new chunks to append.
         */
        this.preBufferQueue = new Queue();
        const that = this;

        setInterval(() => {
            let chunk = that.preBufferQueue.poll();

            if (chunk !== null) {
                that.sourceBuffer.appendBuffer(chunk.payload);
                console.log('Total processing time of %s-%d: %d ms', chunk.cameraId, chunk.timestamp, Date.now() - chunk.timestamp);
            }
        }, INTERVAL);
    }

    append(chunk) {
        this.preBufferQueue.append(chunk);
    }
}
