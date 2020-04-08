"""Server side"""


import logging

from bottle import Bottle, request, run

from broker.scheduling import Scheduler


def append_job(user):
    """Receives a POST request to append a new job to the scheduler"""
    logging.info("Received POST request from %s", user)
    schedule.add_job(user, request.POST)


def setup_rooting(app):
    """Configures explicit rooting"""
    app.route("/<user>", "POST", append_job)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    schedule = Scheduler("data.db")  # pylint: disable=C0103
    print(schedule)
    web_app = Bottle()  # pylint: disable=C0103
    setup_rooting(web_app)
    run(web_app, host="localhost", port=8080)
