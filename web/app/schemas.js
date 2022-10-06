const fs = require('fs');
const path = require('path');
const avro = require('avsc');
const configuration = require('./configuration')
const Long = require('long');

const longType = avro.types.LongType.__with({
  fromBuffer: (buf) => {
    return new Long(buf.readInt32LE(), buf.readInt32LE(4));
  },
  toBuffer: (n) => {
    const buf = Buffer.alloc(8);
    buf.writeInt32LE(n.getLowBits());
    buf.writeInt32LE(n.getHighBits(), 4);
    return buf;
  },
  fromJSON: Long.fromValue,
  toJSON: (n) => +n,
  isValid: Long.isLong,
  compare: (n1, n2) => n1.compare(n2)
});

function readSchema(fileName) {
  const data = fs.readFileSync(path.join(configuration['schemas'], fileName), {encoding: 'utf8'});
  return avro.Type.forSchema(JSON.parse(data), {registry: {'long': longType}});
}

module.exports = {
  VIDEO_CHUNK_MESSAGE: readSchema('VideoChunkMessage.json')
};