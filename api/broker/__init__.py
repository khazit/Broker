"""Flask's App Factory.

This is where the app is created.

See: https://hackersandslackers.com/flask-application-factory
"""

from flask import Flask
from flask_cors import CORS

from broker.core.scheduling import Scheduler


def create_app(config_class):
    """Initialize the core application"""
    app = Flask(
        __name__,
        instance_relative_config=False
    )
    app.config.from_object(config_class)
    CORS(app)
    schedule = Scheduler(config_class.DATABASE_URI)

    with app.app_context():
        from broker.routes import jobs, runners # pylint: disable=C0415,W0611
        app.schedule = schedule

        return app
