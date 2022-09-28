#!/usr/bin/env node

const server = require('./app');
const configuration = require('./app/configuration');
const logger = require('./app/logger')

const port = configuration['server']['port'];

// Start server
server.listen(port, function () {
  logger.info(`Listening on port ${port}!`);
});
