#!/usr/bin/env node

const createServer = require('./app');
const configuration = require('./app/configuration');
const logger = require('./app/logger');

const port = configuration['server']['port'];
const certificatePath = configuration['server']['ssl_cert_path'];
const privateKeyPath = configuration['server']['ssl_key_path'];

// Create server
const server = createServer(certificatePath, privateKeyPath);

// Start server
server.listen(port, function () {
  logger.info(`Listening on port ${port}!`);
});
