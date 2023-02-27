from utils.orm.src import Area
from flask import jsonify
from peewee import IntegrityError


def _get_areas():
    areas = Area.select().order_by(Area.name).execute()
    result = list(map(lambda area: {
        'id': area.id,
        'name': area.name,
        'type': area.type.name
    }, areas))
    return result


def _update_area(area_id, name, area_type):
    if area_id == "-1":
        area_id = Area.insert(name=name, type=area_type).execute()
    else:
        Area.update(name=name, type=area_type).where(Area.id == area_id).execute()
    # Return OK
    resp = jsonify(area_id=area_id)
    return resp


def _delete_area(area_id):
    try:
        Area.delete().where(Area.id == area_id).execute()
        # Role deleted ok
        return jsonify(success=True)
    except IntegrityError:
        Area._meta.database.rollback()
        # Role is still referenced in other tables
        return jsonify(success=False), 400


class AreasController:

    def __init__(self):
        pass

    def make_routes(self, app):
        app.route('/areas')(_get_areas)
        app.route('/areas/<area_id>/<name>/<area_type>', methods=["POST"])(_update_area)
        app.route('/areas/<area_id>', methods=["DELETE"])(_delete_area)
