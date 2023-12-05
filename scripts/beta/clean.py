from utils.orm.src.database import connect
from utils.orm.src.models import BrokenRestriction, Face, Notification, UnknownCluster, UnknownFace, VideoChunk
from utils.video_storage import StorageFactory, StorageType


def clean_database():
    connect('argus', 'argus', 5432, 'argus', 'panoptes')

    UnknownFace.truncate_table(restart_identity=True)
    UnknownCluster.truncate_table(restart_identity=True, cascade=True)

    Notification.truncate_table(restart_identity=True)
    BrokenRestriction.truncate_table(restart_identity=True, cascade=True)

    Face.truncate_table(restart_identity=True, cascade=True)
    VideoChunk.truncate_table(restart_identity=True, cascade=True)


def clean_bucket(bucket):
    for obj_name in map(lambda x: x.object_name, bucket.list()):
        bucket.remove(obj_name)


def clean_storage():
    storage_factory = StorageFactory('argus', 9500, 'argus', 'panoptes')

    clean_bucket(storage_factory.new(StorageType.VIDEO_CHUNKS))
    clean_bucket(storage_factory.new(StorageType.VIDEO_FRAMES))
    clean_bucket(storage_factory.new(StorageType.FRAME_FACES))


if __name__ == "__main__":
    clean_database()
    clean_storage()
