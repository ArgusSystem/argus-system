from utils.orm.src.models import Restriction, RestrictionSeverity
from flask import jsonify, request
from peewee import IntegrityError


def _get_restrictions():
    return [{
                'id': restriction.id,
                'rule': restriction.rule,
                'severity': {
                    'name': restriction.severity.name,
                    'value': restriction.severity.value
                },
                'last_update': str(restriction.last_update)
            } for restriction in Restriction.select().join(RestrictionSeverity).order_by(Restriction.last_update.desc())]


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
