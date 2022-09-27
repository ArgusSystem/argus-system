const server = require('./app');
const configuration = require('./app/configuration');

const port = configuration['server']['port'];

// Start server
server.listen(port, function () {
  console.log(`Listening on port ${port}!`);
});
