from utils.orm.src.database import connect
from utils.video_storage import StorageFactory, StorageType

from .camera import CameraController
from .history import HistoryController
from .people import PeopleController


class ControllersFactory:

    def __init__(self, db_configuration, storage_configuration):
        connect(**db_configuration)
        self.storage_factory = StorageFactory(**storage_configuration)

    def all(self):
        return [
            CameraController(self.storage_factory.new(StorageType.VIDEO_FRAMES)),
            HistoryController,
            PeopleController(self.storage_factory.new(StorageType.PEOPLE))
        ]
