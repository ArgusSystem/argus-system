const logger = require('./logger');
const configuration = require('./configuration');

const Minio = require('minio');
const minioClient = new Minio.Client({...configuration['storage']['client'], useSSL: false});
const bucket = configuration['storage']['bucket'];

async function fetchVideoChunk (objectName) {
  return new Promise((resolve, reject) => {
    const chunks = [];

    minioClient.getObject(bucket, objectName).then(function(dataStream) {
      dataStream.on('error', function (err) {
        logger.error(err);
        reject(err);
      });

      dataStream.on('data', async function (chunk) {
        chunks.push(chunk);
      });

      dataStream.on('end', function () {
        logger.debug(`${objectName} fetched!`);
        resolve(Buffer.concat(chunks));
      });
    }).catch(reject);
  });
}

module.exports = fetchVideoChunk;
