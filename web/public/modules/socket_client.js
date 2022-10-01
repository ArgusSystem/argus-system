export class SocketClient {
  constructor () {
    this.client = io.connect('http://localhost:8080/video', { forceNew: true });
    console.log("Connected to web server!");
  }

  onVideoChunk (callback) {
    this.client.on('chunk', callback);
  }
}
