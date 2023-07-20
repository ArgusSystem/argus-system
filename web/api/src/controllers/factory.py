from utils.orm.src.database import connect
from utils.video_storage import StorageFactory, StorageType

from .camera import CameraController
from .history import HistoryController
from .notifications import NotificationsController
from .people import PeopleController
from .roles import RolesController
from .area_types import AreaTypesController
from .areas import AreasController
from .restrictions import RestrictionsController
from .restriction_severity import RestrictionSeveritiesController
from .users import UsersController
from .unknown_clusters import UnknownClustersController
from .faces import FacesController


class ControllersFactory:

    def __init__(self, db_configuration, publisher_configuration, storage_configuration, tracer):
        connect(**db_configuration)
        self.publisher_configuration = publisher_configuration
        self.storage_factory = StorageFactory(**storage_configuration)
        self.tracer = tracer

    def all(self):
        return [
            CameraController(self.storage_factory.new(StorageType.VIDEO_FRAMES)),
            HistoryController,
            PeopleController(self.storage_factory.new(StorageType.PEOPLE),
                             self.storage_factory.new(StorageType.VIDEO_FRAMES)),
            RolesController(),
            AreaTypesController(),
            AreasController(),
            NotificationsController,
            RestrictionsController,
            RestrictionSeveritiesController,
            UsersController,
            UnknownClustersController(self.publisher_configuration, self.tracer),
            FacesController(self.storage_factory.new(StorageType.FRAME_FACES))
        ]
