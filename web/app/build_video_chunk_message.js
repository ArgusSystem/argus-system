const fetchVideo = require('./fetch_video_chunk');
const cameraPromise = require('./fetch_cameras');

async function buildVideoChunkMessage(metadata) {
  const cameraId = metadata['camera_id'];

  return {
    cameraId,
    timestamp: metadata['timestamp'],
    samples: metadata['samples'],
    duration: metadata['duration'],
    sequenceId: metadata['sequence_id'],
    framerate: (await cameraPromise)[cameraId],
    payload: await fetchVideo(`${cameraId}-${metadata['timestamp']}`)
  };
}

module.exports = buildVideoChunkMessage;
