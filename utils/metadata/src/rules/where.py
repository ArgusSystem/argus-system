from .factory import create


class Camera:

    def __init__(self, cameras):
        self.cameras = cameras

    def match(self, where):
        return where.camera in self.cameras


class Area:

    def __init__(self, areas):
        self.areas = areas

    def match(self, where):
        return where.area in self.areas


class AreaType:

    def __init__(self, area_types):
        self.areas_types = area_types

    def match(self, where):
        return where.area_type in self.areas_types


TYPES = {
    'camera': Camera,
    'area': Area,
    'area_type': AreaType
}


class Where:

    def __init__(self, camera, area, area_type):
        self.camera = camera
        self.area = area
        self.area_type = area_type


class WhereRule:

    def __init__(self, configuration):
        self.rules = [create(TYPES, node) for node in configuration]

    def match(self, where):
        return any(rule.match(where) for rule in self.rules)
