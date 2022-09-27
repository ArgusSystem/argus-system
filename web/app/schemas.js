const fs = require('fs');
const path = require('path');
const avro = require('avsc');

const rootPath = path.join('$ARGUS_HOME', 'utils', 'events', 'resources');

function readSchema(fileName) {
  const data = fs.readFileSync(path.join(rootPath, fileName), {encoding: 'utf8'});
  return avro.Type.forSchema(JSON.parse(data));
}

module.exports = {
  VIDEO_CHUNK_MESSAGE: readSchema('VideoChunkMessage.json')
};