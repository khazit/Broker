"""Server side"""


import logging
import json
from flask_cors import CORS
from flask import Flask, request, jsonify
from broker.scheduling import Scheduler


logging.basicConfig(level=logging.INFO)
schedule = Scheduler("data.db")  # pylint: disable=C0103
app = Flask(__name__)  # pylint: disable=C0103
cors = CORS(app)  # pylint: disable=C0103

@app.route("/jobs/add", methods=["POST"])
def append_job():
    """Handles a POST request to append a new job to the scheduler"""
    payload = json.loads(request.data)
    logging.info("Received POST request from %s", payload["user"])
    schedule.add_job(payload)
    response = jsonify(success=True)
    return response


@app.route("/jobs/<user>", methods=["GET"])
def get_job_list(user):
    """Handles a GET request and returns all the user's jobs"""
    logging.info("Received GET request from %s", user)
    res = []
    jobs = schedule.get_jobs(user)
    for job in jobs:
        res.append(job.to_dict())
    response = jsonify(res)
    return response


@app.route("/jobs/remove/<job_id>", methods=["DELETE"])
def remove_job(job_id):
    """Handles a DELETE request to remove a job from the schedule"""
    logging.info("Received DELETE request to remove  %s", job_id)
    schedule.remove_job(int(job_id))
    return "Removed job from schedule\n"
