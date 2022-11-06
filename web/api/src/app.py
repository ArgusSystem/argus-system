from flask import Flask
from flask_cors import CORS


def make_app(name, controllers):
    app = Flask(name)

    for controller in controllers:
        controller.make_routes(app)

    CORS(app)

    return app
