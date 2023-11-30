def to_object_storage_key(camera, timestamp, offset):
    return f'{camera}-{timestamp}-{offset}'
