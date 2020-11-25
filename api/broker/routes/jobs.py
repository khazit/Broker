"""Routes related to job resources"""

# pylint: disable=W0703

import os
import logging

from flask import current_app as app
from flask import request, jsonify, send_from_directory

from broker.core.models import Job


logger = logging.getLogger(__name__)


@app.route("/jobs", methods=["POST"])
def append_job():
    """Appends a new job to the schedule."""
    payload = request.json
    logger.info("REQUEST: Add job to schedule")
    try:
        job = Job.from_payload(payload)
        app.schedule.add_job(job)
        logger.info("RESPONSE: Job %i added to schedule", job.identifier)
        return jsonify(job.to_dict()), 201
    except Exception as err:
        logger.error(err)
        return jsonify(error="Internal Server Error"), 500


@app.route("/jobs/<job_id>", methods=["DELETE"])
def remove_job(job_id):
    """Removes a job from the schedule."""
    job_id = int(job_id)
    logger.info("REQUEST: Remove job %i from schedule", job_id)
    try:
        app.schedule.remove_job(job_id)
        logger.info("RESPONSE: Job %i removed from schedule", job_id)
        return jsonify(), 204
    except IndexError as err:
        logger.error(err)
        return jsonify(error=f"Resource Job #{job_id} not found"), 404


@app.route("/jobs", methods=["GET"])
def get_jobs():
    """Fetchs all jobs."""
    logger.info("REQUEST: Fetch all jobs")
    jobs = app.schedule.get_jobs()
    res = []
    for job in jobs:
        res.append(job.to_dict())
    logger.info("RESPONSE: Found %i jobs", len(jobs))
    return jsonify(res), 200


@app.route("/jobs/<job_id>/logs", methods=["POST"])
def add_logfile(job_id):
    """Adds a logfile to its corresponding job."""
    if "logfile" not in request.files:
        logger.error("Runner wanted to add a logfile, but file is missing in request")
        return jsonify(error="Missing file in request"), 400
    logger.info("REQUEST: Add logfile to job %i", job_id)
    logfile = request.files["logfile"]
    try:
        filename = app.schedule.db_manager.add_logfile(job_id)
        logfile.save(os.path.join(app.config["STORAGE_URI"], filename))
        logger.info("RESPONSE: Added logfile to job %i", job_id)
        return jsonify(), 204
    except IndexError as err:
        logger.error(err)
        return jsonify(error=f"Resource Job #{job_id} not found"), 404


@app.route("/jobs/<job_id>/logs", methods=["GET"])
def get_logfile(job_id):
    """Returns a log file given a job id."""
    try:
        logfile = app.schedule.db_manager.get_logfile(job_id)
        logger.info("REQUEST: Get logfile for %i", job_id)
        if logfile is None:
            return jsonify(error="Log file not found"), 404
        logger.info("RESPONSE: Logfile sent")
        return send_from_directory(
            directory=app.config["STORAGE_URI"],
            filename=logfile.filename
        ), 200
    except IndexError as err:
        logger.error(err)
        return jsonify(error=f"Resource Job #{job_id} not found"), 404
