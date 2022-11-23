const logger = require('./logger');
const { Server } = require("socket.io");

function toNamespace(camera_name) {
  return `/video-${camera_name}`;
}

class SocketServer {
  constructor (httpServer, cameras) {
    this.io = new Server(httpServer);

    for (const name of cameras) {
      this.io.of(toNamespace(name)).on('connection', (socket) => {
        logger.debug('New client %s connected to video %s!', socket.id, name);

        socket.on('disconnect', () => logger.debug('Client %s disconnected from %s!', socket.id, name));
      });
    }
  }

  sendVideoChunk (videoChunk) {
    this.io.of(toNamespace(videoChunk.cameraId)).emit('chunk', videoChunk);
    logger.debug(`Sent chunk ${videoChunk.cameraId}-${videoChunk.timestamp} to clients!`);
  }

  sendDetectedFace (face) {
    const [cameraId, _] =  face.videoChunkId.split('-');
    this.io.of(toNamespace(cameraId)).emit('face', face);
    logger.debug(`Sent detected face to clients!`);
  }
}

module.exports = SocketServer;
