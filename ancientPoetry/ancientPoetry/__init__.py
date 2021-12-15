from flask import Flask
from .views import index


def create_app():
    app = Flask(__name__)

    app.register_blueprint(index.ind)
    app.config.from_object("settings.DevelopmentConfig")

    return app