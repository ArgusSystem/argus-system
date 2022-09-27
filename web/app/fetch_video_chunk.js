const logger = require('./logger');
const configuration = require('./configuration');

const Minio = require('minio');
const minioClient = new Minio.Client({...configuration['storage']['client'], useSSL: false});
const bucket = configuration['storage']['bucket'];

function fetchVideoChunk (objectName) {
  const chunks = [];

  minioClient.getObject(bucket, objectName, function (err, stream) {
    stream.on('error', function (err) {
      logger.error(err);
    })

    stream.on('data', function (chunk) {
      chunks.push(chunk);
    })

    stream.on('end', function () {
      logger.info(`${objectName} fetched!`);
    })
  })

  return Buffer.concat(chunks);
}

module.exports = fetchVideoChunk;
