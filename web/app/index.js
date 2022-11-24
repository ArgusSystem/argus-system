const express = require('express');
const http = require('http');

const SocketServer = require('./socket_server');
const camerasPromise = require('./fetch_cameras');
const Consumer = require('./consumer');

// Create app and server
const app = express();
const server = http.createServer(app);

// Expose public
app.use(express.static('public'));


camerasPromise.then(cameras => {
    // Create SocketServer
    const socketServer = new SocketServer(server, Object.keys(cameras));

    // Create RabbitMQ consumer
    const consumer = new Consumer(socketServer);
    consumer.start();
})


module.exports = server;
