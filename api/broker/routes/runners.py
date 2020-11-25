"""Routes that are used by runners."""

import logging

from flask import current_app as app
from flask import request, jsonify

from broker.core.utils import is_status_valid


logger = logging.getLogger(__name__)


@app.route("/runners/available-job", methods=["GET"])
def get_available_job():
    """Gets an available job"""
    logger.info("REQUEST: Runner asked for an available job")
    job = app.schedule.get_next()
    if job is None:
        logger.info("RESPONSE: No more jobs available.")
        return jsonify(None), 204
    logger.info("RESPONSE: Job %i sent to runner", job.identifier)
    return jsonify(job.to_dict()), 200


@app.route("/runners/update-job", methods=["PUT"])
def update_job_status():
    """Updates a job's status"""
    payload = request.json
    logger.info(
        "REQUEST: Runner want to update job %i to status %s",
        payload["identifier"], payload["status"])
    if not is_status_valid(payload["status"]):
        logger.error("Status is not valid")
        return jsonify(
            error=f"Invalid value for status {payload['status']}"
        ), 400
    try:
        app.schedule.update_job_status(payload["identifier"], payload["status"])
        logger.info("RESPONSE: Updated job status")
        return jsonify(), 204
    except IndexError as err:
        logger.error(err)
        return jsonify(
            error=f"Resource Job #{payload['identifier']} not found"
        ), 404
