export class SocketClient {
    constructor (camera) {
        const {protocol, hostname, port} = window.location;
        this.client = io.connect(`${protocol}//${hostname}:${port}/video-${camera}`, { forceNew: true });
    }

    onChunk (callback) {
        this.client.on('chunk', callback);
    }

    onFace (callback) {
        this.client.on('face', callback);
    }
}
