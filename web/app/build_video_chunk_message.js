const fetchVideo = require('./fetch_video_chunk');

async function buildVideoChunkMessage(metadata) {
  return {
    cameraId: metadata['camera_id'],
    timestamp: metadata['timestamp'],
    samples: metadata['samples'],
    duration: metadata['duration'],
    payload: await fetchVideo(`${metadata['camera_id']}-${metadata['timestamp']}`)
  };
}

module.exports = buildVideoChunkMessage;
