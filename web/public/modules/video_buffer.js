const MIME = 'video/mp4; codecs="avc1.f4001f"';

export class VideoBuffer {
  constructor (mediaSource) {
    this.sourceBuffer = mediaSource.addSourceBuffer(MIME);
    this.sourceBuffer.mode = 'sequence';

    this.sourceBuffer.addEventListener('error', function (e) {
      console.log(e);
    });
  }

  append(chunk) {
    this.sourceBuffer.appendBuffer(chunk.payload);
  }
}
