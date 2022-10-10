from .local_video_chunk import LocalVideoChunk, LOCAL_DIR
import os.path as path


def fetch(video_chunk_message, remote_storage):
    name = str(video_chunk_message)
    filepath = path.join(LOCAL_DIR, f'{name}.{video_chunk_message.encoding}')
    remote_storage.fetch(name, filepath)

    local_video_chunk = LocalVideoChunk(camera_id=video_chunk_message.camera_id,
                                        timestamp=video_chunk_message.timestamp,
                                        encoding=video_chunk_message.encoding,
                                        framerate=video_chunk_message.framerate,
                                        width=video_chunk_message.width,
                                        height=video_chunk_message.height,
                                        filepath=filepath,
                                        duration=video_chunk_message.duration)

    return local_video_chunk
