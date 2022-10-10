const fetchVideo = require('./fetch_video_chunk');

async function buildVideoChunkMessage(metadata) {
  const video_chunk_id = `${metadata['camera_id']}-${metadata['timestamp']}`;
  const payload = await fetchVideo(video_chunk_id);
  return {video_chunk_id, ...metadata, payload};
}

module.exports = buildVideoChunkMessage;
