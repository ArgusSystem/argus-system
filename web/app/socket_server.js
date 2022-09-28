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
    const io = this.io;

    videoChunk.payloadPromise.then(function (payload) {
      io.of('/video').emit('chunk', { ...videoChunk.metadata, payload: payload });
      logger.info(`Sent chunk ${videoChunk.id()} to clients!`);
    });
  }
}

module.exports = SocketServer;
