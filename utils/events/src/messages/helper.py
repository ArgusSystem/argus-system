def unwrap_video_chunk_id(video_chunk_id):
    camera_name, timestamp = video_chunk_id.split('-')
    return camera_name, int(timestamp)
