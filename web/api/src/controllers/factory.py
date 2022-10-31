from utils.orm.src.database import connect

from .camera import CameraController
from .people import PeopleController


class ControllersFactory:

    def __init__(self, db_configuration):
        connect(**db_configuration)

    @staticmethod
    def all():
        return [
            CameraController,
            PeopleController
        ]
