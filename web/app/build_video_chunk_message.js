const fetchVideo = require('./fetch_video_chunk');

async function buildVideoChunkMessage(metadata) {
  const payload = await fetchVideo(`${metadata['camera_id']}-${metadata['timestamp']}`);
  return {...metadata, payload};
}

module.exports = buildVideoChunkMessage;
