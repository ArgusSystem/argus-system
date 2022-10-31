
def get_camera_id(video_chunk_id):
    return video_chunk_id.split("-")[0]


def get_timestamp(video_chunk_id):
    return video_chunk_id.split("-")[1]
