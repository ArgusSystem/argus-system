const express = require('express');
const http = require('http');
const https = require('https');
const fs = require('fs');

const SocketServer = require('./socket_server');
const camerasPromise = require('./fetch_cameras');
const Consumer = require('./consumer');


function createServer(certificatePath, privateKeyPath) {
    // Create app
    const app = express();

    // Create HTTP or HTTPS server
    let server = null;
    if (certificatePath && privateKeyPath) {
        // Load SSL certificate and key
        const options = {
            key: fs.readFileSync(privateKeyPath),
            cert: fs.readFileSync(certificatePath)
        };

        // Crete HTTPS server
        server = https.createServer(options, app);
    }
    else {
        server = http.createServer(app);
    }

    // Expose public
    app.use(express.static('public'));

    camerasPromise.then(cameras => {
        // Create SocketServer
        const socketServer = new SocketServer(server, Object.keys(cameras));

        // Create RabbitMQ consumer
        const consumer = new Consumer(socketServer);
        consumer.start();
    });

    return server;
}


module.exports = createServer;
