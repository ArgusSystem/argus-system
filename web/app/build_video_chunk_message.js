const fetchVideo = require('./fetch_video_chunk');

async function buildVideoChunkMessage(metadata) {
  return {
    cameraId: metadata['camera_id'],
    timestamp: metadata['timestamp'],
    samplingRate: metadata['sampling_rate'],
    framerate: metadata['framerate'],
    duration: metadata['duration'],
    payload: await fetchVideo(`${metadata['camera_id']}-${metadata['timestamp']}`)
  };
}

module.exports = buildVideoChunkMessage;
