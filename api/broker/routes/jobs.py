"""Routes related to job resources"""

# pylint: disable=W0703

import logging

from flask import current_app as app
from flask import request, jsonify

from broker.core.models import Job


@app.route("/jobs", methods=["POST"])
def append_job():
    """Appends a new job to the schedule."""
    payload = request.json
    logging.info("POST - u %s", payload["user"])
    try:
        job = Job.from_payload(payload)
        app.schedule.add_job(job)
        return jsonify(job.to_dict()), 201
    except Exception as err:
        logging.error(err)
        return jsonify(error="Internal Server Error"), 500


@app.route("/jobs/<job_id>", methods=["DELETE"])
def remove_job(job_id):
    """Removes a job from the schedule."""
    logging.info("DELETE - u %s - id %s", None, job_id)
    try:
        app.schedule.remove_job(int(job_id))
        return jsonify(), 204
    except IndexError as err:
        logging.error(err)
        return jsonify(error=f"Resource Job #{job_id} not found"), 404


@app.route("/jobs", methods=["GET"])
def get_jobs():
    """Fetchs all jobs."""
    logging.info("GET - u %s - id %s", None, "all")
    jobs = app.schedule.get_jobs()
    res = []
    for job in jobs:
        res.append(job.to_dict())
    return jsonify(res), 200
