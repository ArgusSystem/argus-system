import { Queue } from './queue.js'


export class VideoIndex {
    constructor () {
        this.chunks = new Queue();
        this.totalTime = 0;
    }

    add(chunk) {
        this.chunks.append({
            id: `${chunk.cameraId}-${chunk.timestamp}`,
            samples: chunk.samples,
            framerate: chunk.framerate,
            startTime: this.totalTime,
            duration: chunk.duration
        });

        this.totalTime += chunk.duration;
    }

    element() {
        return this.chunks.peek();
    }

    remove() {
        return this.chunks.poll();
    }
}