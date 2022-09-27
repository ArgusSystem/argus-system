const logger = require('./logger');
const { Server } = require("socket.io");

class SocketServer {
  constructor (httpServer) {
    this.io = new Server(httpServer);

    this.io.of('/video').on('connection', function (socket) {
      logger.info('New client connected!');
    });
  }

  sendVideoChunk (videoChunk) {
    logger.info(`Starting to send chunk ${videoChunk.id()} to clients!`);
    this.io.of('/video')
      .emit('chunk', { ...videoChunk.metadata, payload: videoChunk.payload });
  }
}

module.exports = SocketServer;
