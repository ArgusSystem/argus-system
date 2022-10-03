const logger = require('./logger');
const { Server } = require("socket.io");

class SocketServer {
  constructor (httpServer) {
    this.io = new Server(httpServer);

    this.io.of('/video').on('connection', function (socket) {
      logger.debug('New client connected!');
    });
  }

  sendVideoChunk (videoChunk) {
    this.io.of('/video').emit('chunk', videoChunk);
    logger.debug(`Sent chunk ${videoChunk.camera_id}-${videoChunk.timestamp} to clients!`);
  }
}

module.exports = SocketServer;
