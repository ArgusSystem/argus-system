const configuration = require('./configuration')
const logger = require('./logger')
const amqp = require('amqplib/callback_api');
const schemas = require('./schemas');
const VideoChunk = require('./video_chunk')

const consumerConfiguration = configuration['consumer'];

function onChannel(err, channel, socketServer) {
    if (err) {
        logger.error(err);
    } else {
        channel.consume(consumerConfiguration['video_queue'], function(msg) {
            const metadata = schemas.VIDEO_CHUNK_MESSAGE.fromBuffer(msg.content);
            socketServer.sendVideoChunk(new VideoChunk(metadata));
            channel.ack(msg);
        });
    }
}

function onConnection(err, connection, socketServer) {
    if (err) {
        logger.error(err);
    } else {
        connection.createChannel(function (err, channel) {
            onChannel(err, channel, socketServer);
        });
    }
}

class Consumer {
    constructor (socketServer) {
        this.socketServer = socketServer;
    }

    start() {
        amqp.connect(`${consumerConfiguration['url']}`, function (err, connection) {
            onConnection(err, connection, this.socketServer);
        });
    }
}

module.exports = Consumer;


