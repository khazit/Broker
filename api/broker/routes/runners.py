"""Routes that are used by runners."""

import logging

from flask import current_app as app
from flask import request, jsonify

from broker.core.utils import is_status_valid


@app.route("/runners/available-job", methods=["GET"])
def get_available_job():
    """Gets an available job"""
    logging.info("GET - r %s", None)
    job = app.schedule.get_next()
    if job is None:
        return jsonify(None), 204
    return jsonify(app.schedule.get_next().to_dict()), 200


@app.route("/runners/update-job", methods=["PUT"])
def update_job_status():
    """Updates a job's status"""
    payload = request.json
    logging.info("POST - r %s - id %s", None, payload["identifier"])
    if not is_status_valid(payload["status"]):
        return jsonify(
            error=f"Invalid value for status {payload['status']}"
        ), 400
    try:
        app.schedule.update_job_status(payload["identifier"], payload["status"])
        return jsonify(), 204
    except IndexError as err:
        logging.error(err)
        return jsonify(
            error=f"Resource Job #{payload['identifier']} not found"
        ), 404
