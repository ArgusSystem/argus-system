const fetchVideo = require('./fetch_video_chunk');

class Chunk {
  constructor (metadata) {
    this.metadata = metadata;
    this.payload = fetchVideo(this.id());
  }

  id() {
    return `${this.metadata['camera']}-${this.metadata['timestamp']}`;
  }
}

module.exports = Chunk;
