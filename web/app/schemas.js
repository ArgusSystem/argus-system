const fs = require('fs');
const path = require('path');
const avro = require('avsc');
const configuration = require('./configuration')

function readSchema(fileName) {
  const data = fs.readFileSync(path.join(configuration.schemas, fileName), {encoding: 'utf8'});
  return avro.Type.forSchema(JSON.parse(data));
}

module.exports = {
  VIDEO_CHUNK_MESSAGE: readSchema('VideoChunkMessage.json')
};