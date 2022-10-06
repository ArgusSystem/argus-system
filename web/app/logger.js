const { createLogger, format, transports } = require('winston');
const { combine, timestamp, simple } = format;
const configuration = require('./configuration');

module.exports = createLogger({
  level: configuration['logger']['level'],
  format: combine(timestamp(), simple()),
  transports: [new transports.Console()],
});
