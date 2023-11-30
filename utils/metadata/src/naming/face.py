def to_object_storage_key(camera, timestamp, offset, face_num):
    return f'{camera}-{timestamp}-{offset}-{face_num}'
