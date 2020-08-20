"""The Web Server Gateway Interface (WSGI).

Serves as the app gateway
"""


import os

from broker import create_app
from broker import config


if os.environ["FLASK_ENV"] == "development":
    app = create_app(config.DevConfig)
elif os.environ["FLASK_ENV"] == "production":
    app = create_app(config.ProdConfig)


if __name__ == "__main__":
    app.run()
