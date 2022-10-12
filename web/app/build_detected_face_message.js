function buildDetectedFaceMessage(metadata) {
  const video_chunk_id = metadata['video_chunk_id'];
  const offset = metadata['offset'];
  const face_num = metadata['face_num'];
  const name = metadata['name'];
  const bounding_box = metadata['bounding_box'];
  const probability = metadata['probability'];
  return {video_chunk_id, offset, face_num, name, bounding_box, probability};
}

module.exports = buildDetectedFaceMessage;
