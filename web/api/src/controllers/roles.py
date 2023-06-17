from utils.orm.src import PersonRole
from flask import jsonify
from peewee import IntegrityError


def _get_roles():
    return [{'id': role.id, 'name': role.name} for role in PersonRole.select().order_by(PersonRole.name)]


def _update_role(role_id, name):
    if role_id == "-1":
        role_id = PersonRole.insert(name=name).execute()
    else:
        PersonRole.update(name=name).where(PersonRole.id == role_id).execute()
    # Return OK
    resp = jsonify(role_id=role_id)
    return resp


def _delete_role(role_id):
    try:
        PersonRole.delete().where(PersonRole.id == role_id).execute()
        # Role deleted ok
        return jsonify(success=True)
    except IntegrityError:
        PersonRole._meta.database.rollback()
        # Role is still referenced in other tables
        return jsonify(success=False), 400


class RolesController:

    def __init__(self):
        pass

    def make_routes(self, app):
        app.route('/roles')(_get_roles)
        app.route('/roles/<role_id>/<name>', methods=["POST"])(_update_role)
        app.route('/roles/<role_id>', methods=["DELETE"])(_delete_role)
