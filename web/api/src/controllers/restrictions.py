from utils.orm.src import Restriction
from flask import jsonify
from peewee import IntegrityError


def _get_restrictions():
    restrictions = Restriction.select().order_by(Restriction.role, Restriction.area_type).execute()
    result = list(map(lambda restriction: {
        'id': restriction.id,
        'role': restriction.role.name,
        'area': restriction.area_type.name,
        'start time': str(restriction.time_start),
        'end time': str(restriction.time_end)
    }, restrictions))
    return result


def _update_restriction(restriction_id, role, area, start_time, end_time):
    if restriction_id == "-1":
        restriction_id = Restriction.insert(role=role, area_type=area, time_start=start_time, time_end=end_time).execute()
    else:
        Restriction.update(role=role, area=area, time_start=start_time, time_end=end_time)\
            .where(Restriction.id == restriction_id).execute()
    # Return OK
    resp = jsonify(restriction_id=restriction_id)
    return resp


def _delete_restriction(restriction_id):
    try:
        Restriction.delete().where(Restriction.id == restriction_id).execute()
        # Role deleted ok
        return jsonify(success=True)
    except IntegrityError:
        Restriction._meta.database.rollback()
        # Role is still referenced in other tables
        return jsonify(success=False), 400


class RestrictionsController:

    def __init__(self):
        pass

    def make_routes(self, app):
        app.route('/restrictions')(_get_restrictions)
        app.route('/restrictions/<restriction_id>/<role>/<area>/<start_time>/<end_time>', methods=["POST"])(_update_restriction)
        app.route('/restrictions/<restriction_id>', methods=["DELETE"])(_delete_restriction)
