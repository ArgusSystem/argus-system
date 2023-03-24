from utils.orm.src import Restriction
from flask import jsonify, request
from peewee import IntegrityError


def _get_restrictions():
    return list(map(lambda restriction: {
        'id': restriction.id,
        'offender_role': restriction.offender_role.name,
        'warden_role': restriction.warden_role.name,
        'area': restriction.area_type.name,
        'severity': restriction.severity,
        'start time': str(restriction.time_start),
        'end time': str(restriction.time_end)
    }, Restriction.select().order_by(Restriction.role, Restriction.area_type).execute()))


def _insert_restriction():
    data = request.json

    restriction_id = Restriction.insert(offender_role=data['offender_role'],
                                        warden_role=data['warden_role'],
                                        area_type=data['area'],
                                        severity=data['severity'],
                                        time_start=data['start_time'],
                                        time_end=data['end_time']).execute()

    return str(restriction_id)


def _update_restriction():
    data = request.json

    Restriction.insert(offender_role=data['offender_role'],
                       warden_role=data['warden_role'],
                       area_type=data['area'],
                       severity=data['severity'],
                       time_start=data['start_time'],
                       time_end=data['end_time']) \
        .where(Restriction.id == data['restriction_id']) \
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
