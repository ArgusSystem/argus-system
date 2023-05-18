from utils.orm.src import Restriction
from flask import jsonify, request
from peewee import IntegrityError


def _get_restrictions():
    # TODO: Add wardens
    return list(map(lambda restriction: {
        'id': restriction.id,
        'role': restriction.role.name,
        'area': restriction.area_type.name,
        'severity': restriction.severity,
        'start time': str(restriction.time_start),
        'end time': str(restriction.time_end)
    }, Restriction.select().order_by(Restriction.role, Restriction.area_type).execute()))


def _insert_restriction():
    return str(Restriction.insert(**request.json).execute())


def _update_restriction(restriction_id):
    Restriction.update(**request.json) \
        .where(Restriction.id == restriction_id) \
        .execute()

    return jsonify(success=True)


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

    @staticmethod
    def make_routes(app):
        app.route('/restrictions', methods=['GET'])(_get_restrictions)
        app.route('/restrictions', methods=['POST'])(_insert_restriction)
        app.route('/restrictions/<restriction_id>', methods=["POST"])(_update_restriction)
        app.route('/restrictions/<restriction_id>', methods=["DELETE"])(_delete_restriction)
