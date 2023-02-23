from utils.orm.src import AreaType
from flask import jsonify
from peewee import IntegrityError


def _get_area_types():
    area_types = AreaType.select().order_by(AreaType.name).execute()
    result = list(map(lambda area_type: {
        'id': area_type.id,
        'name': area_type.name
    }, area_types))
    return result


def _update_area_type(area_type_id, name):
    if area_type_id == "-1":
        area_type_id = AreaType.insert(name=name).execute()
    else:
        AreaType.update(name=name).where(AreaType.id == area_type_id).execute()
    # Return OK
    resp = jsonify(area_type_id=area_type_id)
    return resp


def _delete_area_type(area_type_id):
    try:
        AreaType.delete().where(AreaType.id == area_type_id).execute()
        # Role deleted ok
        return jsonify(success=True)
    except IntegrityError:
        AreaType._meta.database.rollback()
        # Role is still referenced in other tables
        return jsonify(success=False), 400


class AreaTypesController:

    def __init__(self):
        pass

    def make_routes(self, app):
        app.route('/area_types')(_get_area_types)
        app.route('/area_types/<area_type_id>/<name>', methods=["POST"])(_update_area_type)
        app.route('/area_types/<area_type_id>', methods=["DELETE"])(_delete_area_type)
