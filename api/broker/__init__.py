from flask import Flask

from broker.core.scheduling import Scheduler


def create_app(config_class):
    """Initialize the core application"""
    app = Flask(
        __name__,
        instance_relative_config=False
    )
    app.config.from_object(config_class)
    schedule = Scheduler(config_class.DATABASE_URI)

    with app.app_context():    
        from broker.routes import jobs, runners
        app.schedule = schedule        

        return app
