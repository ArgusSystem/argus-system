const logger = require('./logger');
const { Server } = require('socket.io');
const ChunkIterator = require('./chunk_iterator')

function toNamespace(camera_name) {
  return `/video-${camera_name}`;
}

class SocketServer {
  constructor (httpServer, cameras) {
    this.chunkIterators = {};
    this.io = new Server(httpServer);

    for (const name of cameras) {
      this.chunkIterators[name] = new ChunkIterator();

      this.io.of(toNamespace(name)).on('connection', (socket) => {
        logger.debug('New client %s connected to video %s!', socket.id, name);

        socket.on('disconnect', () => logger.debug('Client %s disconnected from %s!', socket.id, name));
      });
    }
  }

  sendVideoChunk (videoChunk) {
    const namespace = toNamespace(videoChunk.cameraId);
    const chunkIterator = this.chunkIterators[videoChunk.cameraId];

    chunkIterator.add(videoChunk);

    let nextVideoChunk = null;

    while ((nextVideoChunk = chunkIterator.next()) !== null) {
      this.io.of(namespace).emit('chunk', nextVideoChunk);
      logger.debug(`Sent chunk ${nextVideoChunk.cameraId}-${nextVideoChunk.timestamp} to clients!`);
    }

  }

  sendDetectedFace (face) {
    const [cameraId, _] =  face.videoChunkId.split('-');
    this.io.of(toNamespace(cameraId)).emit('face', face);
    logger.debug(`Sent detected face to clients!`);
  }
}

module.exports = SocketServer;
