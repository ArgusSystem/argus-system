function buildDetectedFaceMessage(message) {
  return {
    videoChunkId: message['video_chunk_id'],
    offset: message['offset'],
    name: message['name'],
    boundingBox: message['bounding_box'],
    probability: message['probability']
  };
}

module.exports = buildDetectedFaceMessage;
