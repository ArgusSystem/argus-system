const logger = require('./logger');
const { Server } = require("socket.io");

class SocketServer {
  constructor (httpServer) {
    this.io = new Server(httpServer);

    this.io.of('/video').on('connection', (socket) => {
      logger.debug('New client %s connected!', socket.id)

      socket.on('disconnect', () => logger.debug('Client %s disconnected!', socket.id))
    });
  }

  sendVideoChunk (videoChunk) {
    this.io.of('/video').emit('chunk', videoChunk);
    logger.debug(`Sent chunk ${videoChunk.cameraId}-${videoChunk.timestamp} to clients!`);
  }

  sendDetectedFace (face) {
    this.io.of('/video').emit('face', face);
    logger.debug(`Sent detected face to clients!`);
  }
}

module.exports = SocketServer;
