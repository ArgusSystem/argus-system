const express = require('express');
const http = require('http');

const SocketServer = require('./socket_server');
const Consumer = require('./consumer');

// Create app and server
const app = express();
const server = http.createServer(app);

// Expose public
app.use(express.static('public'));

// Create SocketServer
const socketServer = new SocketServer(server);

// Create RabbitMQ consumer
const consumer = new Consumer(socketServer);
consumer.start();

module.exports = server;
