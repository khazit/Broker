"""Routes related to job resources"""

# pylint: disable=W0703

import os
import logging

from flask import current_app as app
from flask import request, jsonify, send_from_directory

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


@app.route("/jobs/<job_id>/logs", methods=["POST"])
def add_logfile(job_id):
    """Adds a logfile to its corresponding job."""
    if "logfile" not in request.files:
        return jsonify(error="Missing file in request"), 400
    logfile = request.files["logfile"]
    try:
        filename = app.schedule.db_manager.add_logfile(job_id)
        logfile.save(os.path.join(app.config["STORAGE_URI"], filename))
        return jsonify(), 204
    except IndexError as err:
        logging.error(err)
        return jsonify(error=f"Resource Job #{job_id} not found"), 404


@app.route("/jobs/<job_id>/logs", methods=["GET"])
def get_logfile(job_id):
    """Returns a log file given a job id."""
    try:
        logfile = app.schedule.db_manager.get_logfile(job_id)
        if logfile is None:
            return jsonify(error="Log file not found"), 404
        return send_from_directory(
            directory=app.config["STORAGE_URI"],
            filename=logfile.filename
        ), 200
    except IndexError as err:
        logging.error(err)
        return jsonify(error=f"Resource Job #{job_id} not found"), 404
