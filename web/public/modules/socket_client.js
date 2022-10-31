export class SocketClient {
  constructor () {
    const {protocol, hostname, port} = window.location;
    this.client = io.connect(`${protocol}//${hostname}:${port}/video`, { forceNew: true });
    console.log("Connected to web server!");
  }

  onChunk (callback) {
    this.client.on('chunk', callback);
  }

  onFace (callback) {
    this.client.on('face', callback);
  }
}
