function buildDetectedFaceMessage(message) {
  return {
    videoChunkId: message['video_chunk_id'],
    offset: message['offset'],
    name: message['name'],
    role: message['role'],
    boundingBox: message['bounding_box'],
    probability: message['probability'],
    is_match: message['is_match'],
  };
}

module.exports = buildDetectedFaceMessage;
