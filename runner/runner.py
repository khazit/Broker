"""
Runner that, once installed on a remote host, can receive jobs to execute
from the Scheduler

Manages 3 types of interactions  with the Scheduler:
    1. Sends a GET request when the Runner is available to receive a new job
    2. Receives via a POST request info about the job to execute
    3. Sends a POST request when the job is done to update the status

This runner is written using no objects from the Broker API backend. This was
done on purpose to minimize the dependancy on the Scheduler, and make the
whole architecture as compartmentalized as possible.
"""


import logging
import tempfile
import argparse
import requests
import subprocess


logging.basicConfig(level=logging.INFO)


def get_job():
    """Sends a GET request to the scheduler for a new job to execute

    Returns:
        Dict, job parameters
    """
    try:
        response = requests.get(
            f"http://{SCHEDULER_IP}:{SCHEDULER_PORT}/runners/available-job"
        )
        response.raise_for_status()
        if response.status_code == 200:
            response = response.json()
            logging.info(
                "Successfully received JOB #%d from scheduler",
                response["identifier"]
            )
            return response
        if response.status_code == 204:
            return None
        logging.error("Weird response status code %s", response.status_code)
        return None
    except requests.exceptions.RequestException as err:
        logging.info("Request module raised an exception.\n%s", err)
        return None


def execute_job(identifier, command):
    """Execute a job"""
    send_update(identifier, "RUNNING")
    logfile = tempfile.NamedTemporaryFile(mode="w+b")
    logging.info("Executing JOB #%d: %s", identifier, command)
    result = subprocess.run(
        command,
        shell=True,
        stdout=logfile,
        stderr=subprocess.STDOUT
    )
    requests.post(
        f"http://{SCHEDULER_IP}:{SCHEDULER_PORT}/jobs/{identifier}/logs",
        files={"logfile": open(logfile.name, mode="rb")} 
    )
    if result.returncode == 0:
        send_update(identifier, "DONE")
    else:
        send_update(identifier, "TERMINATED")


def send_update(identifier, status):
    """Sends a job status update to the scheduler

    3 types of status are possible:
        * RUNNING: Job is running
        * TERMINATED: Job terminated itself or was terminated by the runner
        * DONE: Successfully executed

    Args:
        identifier: Integer, job's id
        status: String, job's status
    """
    logging.info("Setting JOB #%d status to %s", identifier, status)
    try:
        requests.put(
            f"http://{SCHEDULER_IP}:{SCHEDULER_PORT}/runners/update-job",
            json={"identifier": identifier, "status": status}
        )
    except requests.exceptions.RequestException as err:
        logging.info("Couldn't send request to scheduler.\n%s", err)


PARSER = argparse.ArgumentParser()
PARSER.add_argument(
    "--scheduler_ip",
    default="localhost",
    help="IP address of the scheduler"
)
PARSER.add_argument(
    "--scheduler_port",
    default="5000",
    help="Port on which the scheduler is listening"
)
ARGS = PARSER.parse_args()
SCHEDULER_IP = ARGS.scheduler_ip
SCHEDULER_PORT = ARGS.scheduler_port


if __name__ == "__main__":
    JOB = get_job()
    while JOB is not None:
        execute_job(JOB["identifier"], JOB["command"])
        JOB = get_job()
    logging.info("No jobs available, shutting down this runner. Box.")
