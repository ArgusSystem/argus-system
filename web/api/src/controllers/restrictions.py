from utils.orm.src.database import db
from utils.orm.src.models import Person, Restriction, RestrictionSeverity, RestrictionWarden, User, UserPerson
from flask import jsonify, request
from peewee import IntegrityError


def map_restriction(restriction):
    return {
        'id': restriction.id,
        'rule': restriction.rule,
        'severity': {
            'name': restriction.severity.name,
            'value': restriction.severity.value
        },
        'last_update': str(restriction.last_update)
    }


def _get_restriction(restriction_id):
    return map_restriction(Restriction.select(Restriction, RestrictionSeverity)
                           .join(RestrictionSeverity)
                           .where(Restriction.id == restriction_id)
                           .get())


def _get_restrictions():
    restrictions = Restriction.select(Restriction, RestrictionSeverity) \
        .where(~Restriction.deleted) \
        .join(RestrictionSeverity) \
        .order_by(Restriction.last_update.desc())

    return [map_restriction(restriction) for restriction in restrictions]


def _insert_restriction():
    data = request.json

    with db.atomic():
        restriction_id = Restriction.insert(**data['restriction']).execute()
        user_people = UserPerson.select(UserPerson, Person) \
            .join(Person).switch(UserPerson).join(User) \
            .where(User.username == data['warden']) \
            .execute()

        for user_person in user_people:
            RestrictionWarden.insert(restriction_id=restriction_id, role_id=user_person.person.role_id)

    return str(restriction_id)


def _update_restriction(restriction_id):
    Restriction.update(**request.json).where(Restriction.id == restriction_id).execute()
    return jsonify(success=True)


def _delete_restriction(restriction_id):
    with db.atomic() as txn:
        try:
            RestrictionWarden.delete().where(RestrictionWarden.restriction_id == restriction_id).execute()
            Restriction.delete().where(Restriction.id == restriction_id).execute()
            txn.commit()
        except IntegrityError:
            # Referenced by another record, soft deleting
            txn.rollback()
            Restriction.update(deleted=True).where(Restriction.id == restriction_id).execute()

    return jsonify(success=True)


class RestrictionsController:

    @staticmethod
    def make_routes(app):
        app.route('/restrictions', methods=['GET'])(_get_restrictions)
        app.route('/restrictions', methods=['POST'])(_insert_restriction)
        app.route('/restrictions/<restriction_id>', methods=['GET'])(_get_restriction)
        app.route('/restrictions/<restriction_id>', methods=['POST'])(_update_restriction)
        app.route('/restrictions/<restriction_id>', methods=['DELETE'])(_delete_restriction)
