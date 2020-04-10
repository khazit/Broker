"""Server side"""


import logging
from flask import Flask, request
from broker.scheduling import Scheduler


logging.basicConfig(level=logging.INFO)
schedule = Scheduler("data.db")  # pylint: disable=C0103
app = Flask(__name__)  # pylint: disable=C0103


@app.route("/<user>", methods=["POST"])
def append_job(user):
    """Handles a POST request to append a new job to the scheduler"""
    logging.info("Received POST request from %s", user)
    schedule.add_job(user, request.form)
    return "Added job to schedule\n"


@app.route("/<user>", methods=["GET"])
def get_job_list(user):
    """Handles a GET request and returns all the user's jobs"""
    logging.info("Received GET request from %s", user)
    res = ""
    jobs = schedule.get_jobs(user)
    for job in jobs:
        res += job.to_json()
        res += "\n"
    return res


@app.route("/<user>/<job_id>", methods=["DELETE"])
def remove_job(user, job_id):
    """Handles a DELETE request to remove a job from the schedule"""
    logging.info("Received DELETE request from %s", user)
    schedule.remove_job(int(job_id))
    return "Removed job from schedule\n"
