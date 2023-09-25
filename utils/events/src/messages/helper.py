def unwrap_video_chunk_id(video_chunk_id):
    return video_chunk_id.split('-')


def get_camera_id(video_chunk_id):
    return unwrap_video_chunk_id(video_chunk_id)[0]


def get_timestamp(video_chunk_id):
    return unwrap_video_chunk_id(video_chunk_id)[1]
