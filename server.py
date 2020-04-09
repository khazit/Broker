"""Server side"""

import logging

from flask import Flask, request
from broker.scheduling import Scheduler

app = Flask(__name__)  # pylint: disable=C0103


@app.route("/<user>", methods=["POST"])
def append_job(user):
    """Receives a POST request to append a new job to the scheduler"""
    logging.info("Received POST request from %s", user)
    schedule.add_job(user, request.form)
    return "Added job to schedule\n"


@app.route("/<user>", methods=["GET"])
def get_job_list(user):
    """Receives a GET request and returns all the user's jobs"""
    res = ""
    jobs = schedule.get_jobs(user)
    for job in jobs:
        res += job.to_json()
        res += "\n"
    return res


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    schedule = Scheduler("data.db")  # pylint: disable=C0103
    app.run()
