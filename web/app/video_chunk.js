const fetchVideo = require('./fetch_video_chunk');

class Chunk {
  constructor (metadata) {
    this.metadata = metadata;
    this.payloadPromise = fetchVideo(this.id());
  }

  id() {
    return `${this.metadata['camera_id']}-${this.metadata['timestamp']}`;
  }
}

module.exports = Chunk;
