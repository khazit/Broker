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


###############################################################################
# Web client requests
###############################################################################


@app.route("/jobs/add", methods=["POST"])
def append_job():
    """Handles a POST request to append a new job to the scheduler"""
    payload = json.loads(request.data)
    logging.info("Received POST request from %s", payload["user"])
    schedule.add_job(payload)
    response = jsonify(success=True)
    return response


@app.route("/jobs/remove/<job_id>", methods=["DELETE"])
def remove_job(job_id):
    """Handles a DELETE request to remove a job from the schedule"""
    logging.info("Received DELETE request to remove  %s", job_id)
    schedule.remove_job(int(job_id))
    return "Removed job from schedule\n"


@app.route("/jobs", methods=["GET"])
def get_job_list():
    """Handles a GET request and returns all the jobs"""
    logging.info("Received GET request")
    res = []
    jobs = schedule.get_jobs(active=False)
    for job in jobs:
        res.append(job.to_dict())
    response = jsonify(res)
    return response


###############################################################################
# Runner requests
###############################################################################


@app.route("/jobs/runner/get_next", methods=["GET"])
def get_next_job():
    """Handles a GET request from a runner and returns a job to run"""
    job = schedule.get_next()
    if job is None:
        logging.info("Queue empty")
        return jsonify(None)
    return schedule.get_next().to_json()


@app.route("/jobs/runner/update", methods=["POST"])
def update_job_status():
    """Handles a POST request to update a job's status"""
    payload = json.loads(request.data)
    logging.info(
        "Received status update for %d : %s",
        payload["identifier"],
        payload["status"]
    )
    schedule.update_job_status(payload["identifier"], payload["status"])
    response = jsonify(success=True)
    return response
