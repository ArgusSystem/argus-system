from flask import Flask


def make_app(name, controllers):
    app = Flask(name)

    for controller in controllers:
        controller.make_routes(app)

    return app
