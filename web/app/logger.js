const { createLogger, format, transports } = require('winston');
const { combine, timestamp, simple, splat } = format;
const configuration = require('./configuration');

module.exports = createLogger({
  level: configuration['logger']['level'],
  format: combine(timestamp(), splat(), simple()),
  transports: [new transports.Console()],
});
