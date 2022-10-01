// S3 Client
const Minio = require('minio');
const minioClient = new Minio.Client( {
  endPoint: 'localhost',
  port: 9500,
  useSSL: false,
  accessKey: 'argus',
  secretKey: 'panoptes'
});

videoChunk = {
  camera_id: 'camera-1',
  timestamp: 0,
  encoding: 'mp4',
  framerate: 30,
  width: 1920,
  height: 1080,
  sampling_rate: 6
};

// UPLOAD VIDEO CHUNK TO S3
const filepath = 'resources/camera-1-1664381744029976668.mp4';

minioClient.fPutObject('video-chunks', `${videoChunk.camera_id}-${videoChunk.timestamp}` , filepath, {}, function(err, etag) {
  return console.log(err, etag);
});

// SEND RABBITMQ EVENT
const fs = require('fs')
const avro = require('avsc')
const data = fs.readFileSync('../../utils/events/resources/VideoChunkMessage.json', {encoding: 'utf8'});
const VIDEO_CHUNK_SCHEMA = avro.Type.forSchema(JSON.parse(data));

const amqp = require('amqplib');
const queue = 'published_video_chunks';

(async () => {
  const conn = await amqp.connect('amqp://argus:panoptes@localhost:5672');

  const ch = await conn.createConfirmChannel();
  ch.sendToQueue(queue, VIDEO_CHUNK_SCHEMA.toBuffer(videoChunk), {}, (err, ok) => {
    if (err) {
      console.warn(err);
    } else {
      console.log('Sent video chunk!');
      ch.close();
      conn.close();
    }
  });
})();

const { io } = require('socket.io-client');
const assert = require('assert')

const socketClient = io.connect('http://localhost:8080/video', { forceNew: true });

socketClient.on('chunk', (chunk) => {
  console.log(`Message received!`);
  assert(chunk.camera_id === 'camera-1');
  assert(chunk.timestamp === 0);
  assert(chunk.framerate === 30);
  assert(chunk.encoding === 'mp4');
  assert(chunk.width === 1920);
  assert(chunk.height === 1080);
  assert(chunk.sampling_rate === 6);
  assert(chunk.payload.length > 0);
  console.log(`Assertions successful!`);
  socketClient.close();
});
