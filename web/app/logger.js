const { createLogger, format, transports } = require('winston');
const { combine, timestamp, simple } = format;

module.exports = createLogger({
  level: 'info',
  format: combine(timestamp(), simple()),
  transports: [new transports.Console()],
});
