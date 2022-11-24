class ChunkIterator {
    constructor () {
       this.buffer = {};
       this.#reset();
    }

    #reset() {
        this.sequence = 0;
        this.lastTimestamp = Number.NEGATIVE_INFINITY;
    }

    add(videoChunk) {
        const sequenceId = videoChunk.sequenceId;

        // The first sequence id means that the system may have been reset, so we do the same
        if (sequenceId === 0)
            this.#reset();

        // Either the video chunk with the same sequence id is not buffered
        // or
        // the timestamp of the video chunk buffered is less than the new chunk
        if (!(sequenceId in this.buffer) || videoChunk.timestamp > this.buffer[sequenceId].timestamp)
            this.buffer[sequenceId] = videoChunk;
    }

    next() {
        let videoChunk = null;

        // Make sure that the sequence is in the buffer and that the timestamp is greater that the last one
        if (this.sequence in this.buffer && this.buffer[this.sequence].timestamp > this.lastTimestamp) {
            videoChunk = this.buffer[this.sequence];
            delete this.buffer[this.sequence];

            this.sequence++;
            this.lastTimestamp = videoChunk.timestamp;
        }

        return videoChunk;
    }
}

module.exports = ChunkIterator;