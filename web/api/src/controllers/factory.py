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
from .statistics import StatisticsController
from .users import UsersController
from .unknown_clusters import UnknownClustersController
from .faces import FacesController
from .known_faces import KnownFacesController


class ControllersFactory:

    def __init__(self, db_configuration, publisher_to_warden_configuration, publisher_to_clusterer_configuration,
                 storage_configuration, tracer):
        connect(**db_configuration)
        self.publisher_to_warden_configuration = publisher_to_warden_configuration
        self.publisher_to_clusterer_configuration = publisher_to_clusterer_configuration
        self.storage_factory = StorageFactory(**storage_configuration)
        self.tracer = tracer

    def all(self):
        return [
            CameraController(self.storage_factory.new(StorageType.VIDEO_FRAMES)),
            HistoryController,
            PeopleController(self.storage_factory.new(StorageType.PEOPLE),
                             self.storage_factory.new(StorageType.VIDEO_FRAMES)),
            RolesController,
            AreaTypesController(),
            AreasController(),
            NotificationsController,
            RestrictionsController,
            RestrictionSeveritiesController,
            UsersController,
            UnknownClustersController(self.publisher_to_warden_configuration, self.publisher_to_clusterer_configuration,
                                      self.tracer),
            FacesController(self.storage_factory.new(StorageType.FRAME_FACES)),
            StatisticsController,
            KnownFacesController(self.publisher_to_warden_configuration, self.publisher_to_clusterer_configuration,
                                      self.tracer)
        ]
