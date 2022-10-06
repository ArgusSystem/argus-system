const configuration = require('./configuration')
const logger = require('./logger')
const amqp = require('amqplib/callback_api');
const schemas = require('./schemas');
const buildVideoChunkMessage = require('./build_video_chunk_message')

const consumerConfiguration = configuration['consumer'];

let start_time = new Date();
function debug_video_chunk_time(){
    let end_time = new Date()
    let elapsed_time = (end_time - start_time) / 1000
    start_time = end_time
    return elapsed_time
}

async function processVideoChunk(channel, msg, socketServer) {
    const metadata = schemas.VIDEO_CHUNK_MESSAGE.fromBuffer(msg.content);
    logger.info(`New message from ${metadata['camera_id']} with timestamp ${metadata['timestamp']}`);
    logger.info(`Time since last message received: ${debug_video_chunk_time()}`)
    const videoChunkMessage = await buildVideoChunkMessage(metadata);
    socketServer.sendVideoChunk(videoChunkMessage);
    channel.ack(msg);
}

function onChannel(err, channel, queue, callback, socketServer) {
    if (err) {
        logger.error(err);
    } else {
        channel.consume(queue, function(msg) {
            callback(channel, msg, socketServer);
        });
    }
}

function onConnection(err, connection, socketServer) {
    if (err) {
        logger.error(err);
    } else {
        connection.createChannel(function (err, channel) {
            onChannel(err, channel, consumerConfiguration['video_queue'], processVideoChunk, socketServer);
        });
    }
}

class Consumer {
    constructor (socketServer) {
        this.socketServer = socketServer;
    }

    start() {
        const socketServer = this.socketServer;
        amqp.connect(`${consumerConfiguration['url']}`, function (err, connection) {
            onConnection(err, connection, socketServer);
        });
    }
}

module.exports = Consumer;


