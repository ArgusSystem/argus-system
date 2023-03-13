from flask import request
from peewee import DoesNotExist

from utils.orm.src.models.user import User


def _log_in(username):
    password = request.args.get('password')

    if password is None:
        return 'No password', 400

    try:
        user = User.get(User.username == username)

        if user.is_authorized(password):
            return user.alias
    except DoesNotExist:
        pass

    return 'Invalid username or password', 401


class UsersControllers:

    @staticmethod
    def make_routes(app):
        app.route('/users/<username>')(_log_in)
