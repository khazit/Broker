"""The Web Server Gateway Interface (WSGI).

Serves as the app gateway
"""


import os
import logging

from broker import create_app
from broker import config


if os.environ["FLASK_ENV"] == "development":
    app_config = config.DevConfig
elif os.environ["FLASK_ENV"] == "production":
    app_config = config.ProdConfig

app = create_app(app_config)

logging.basicConfig(
    filename=app_config.LOGFILE,
    filemode="a",
    format="%(asctime)s %(name)s %(levelname)-2s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S"
)

if __name__ == "__main__":
    app.run()