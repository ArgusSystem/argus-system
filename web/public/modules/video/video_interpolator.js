class Sample {
    constructor (chunkId, sampleOffset, frameOffset) {
        this.chunkId = chunkId;
        this.sampleOffset = sampleOffset;
        this.frameOffset = frameOffset;
    }
}

export class VideoInterpolator {
    constructor (videoIndex, facesIndex) {
        this.videoIndex = videoIndex;
        this.facesIndex = facesIndex;

        this.lastSample = null;
        this.staleChunkId = null;
    }


    getFaces(time) {
        const [chunkId, frameOffset] = this.#locateLastSample(time);
        const faces = this.lastSample !== null ?
            this.facesIndex.get(this.lastSample.chunkId, this.lastSample.frameOffset) :
            [];

        if (faces.length > 0)
            console.log('Found %d faces for {chunk: %s, offset: %d}', faces.length, chunkId, frameOffset);

        return faces;
    }

    #locateLastSample (time) {
        // The chunk that is currently being displayed
        let currentChunk = null;
        // The relative time to the chunk in display
        let relativeTime = null;

        do {
            // Remove last chunk and store last sample
            if (currentChunk !== null) {
                this.videoIndex.remove();
                this.#markStaleChunk(currentChunk.id);
                const lastSampleOffset = currentChunk.samples.length - 1;
                this.lastSample = new Sample(currentChunk.id, lastSampleOffset, currentChunk.samples[lastSampleOffset]);
            }

            currentChunk = this.videoIndex.element();
            relativeTime = time - currentChunk.startTime;
        } while (relativeTime >= currentChunk.duration);

        // Current frame in the chunk
        const frameOffset = Math.floor(relativeTime * currentChunk.framerate);

        let sampleOffset = this.lastSample !== null && this.lastSample.chunkId === currentChunk.id ?
            this.lastSample.sampleOffset :
            0;

        // Iterate through samples to find the nearest sample offset for the frame
        while (sampleOffset < currentChunk.samples.length && frameOffset >= currentChunk.samples[sampleOffset]) {
            this.lastSample = new Sample(currentChunk.id, sampleOffset, currentChunk.samples[sampleOffset]);
            sampleOffset++;
        }

        return [currentChunk.id, frameOffset];
    }

    #markStaleChunk(chunkId) {
        if (this.staleChunkId !== null)
            this.facesIndex.remove(this.staleChunkId);

        this.staleChunkId = chunkId;
    }
}