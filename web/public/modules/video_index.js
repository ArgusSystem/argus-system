import { Queue } from './queue'

class Sample {
  constructor (chunkId, sampleOffset, frameOffset) {
    this.chunkId = chunkId;
    this.sampleOffset = sampleOffset;
    this.frameOffset = frameOffset;
  }
}

export class VideoIndex {
  constructor (faceIndex) {
    this.chunks = new Queue();
    this.totalTime = 0;

    this.faceIndex = faceIndex;
    this.lastSample = null;

    this.staleChunkId = null;
  }

  addChunk(chunk) {
    this.chunks.append({
      id: `${chunk.cameraId}-${chunk.timestamp}`,
      samples: chunk.samples,
      framerate: chunk.framerate,
      startTime: this.totalTime,
      duration: chunk.duration
    });

    this.totalTime += chunk.duration;
  }

  getFaces(time) {
    [chunkId, frameOffset] = this.#locateLastSample(time);
    const faces = this.faceIndex.get(this.lastSample.chunkId, this.lastSample.frameOffset);
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
        const lastChunk = this.chunks.poll();
        this.#markStaleChunk(lastChunk.id);
        const lastSampleOffset = lastChunk.samples.length - 1;
        this.lastSample = new Sample(lastChunk.id, lastSampleOffset, lastChunk.samples[lastSampleOffset]);
      }

      currentChunk = this.chunks.peek();
      relativeTime = time - currentChunk.startTime;
    } while (relativeTime >= currentChunk.duration);

    // Current frame in the chunk
    const frameOffset = Math.floor(relativeTime * currentChunk.framerate);

    let sampleOffset = this.lastSample.chunkId === currentChunk.id ? this.lastSample.sampleOffset : 0;

    // Iterate through samples to find the nearest sample offset for the frame
    while (sampleOffset < currentChunk.samples.length && frameOffset >= currentChunk.samples[sampleOffset]) {
      this.lastSample = new Sample(currentChunk.id, sampleOffset, currentChunk.samples[sampleOffset]);
      sampleOffset++;
    }

    return [currentChunk.id, frameOffset];
  }

  #markStaleChunk(chunkId) {
    if (this.staleChunkId !== null)
      this.faceIndex.remove(chunkId);

    this.staleChunkId = chunkId;
  }
}