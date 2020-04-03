"""Server side"""


import json
import sqlite3
import logging
from time import time
from enum import Enum
from os.path import isfile
from bottle import Bottle, request, run


class JobStatus(Enum):
    """Represent the status of a job

        - UNKNOWN: Given that a Runner can run on a different network,
            the Scheduler asks for an update on the status of all the jobs
            regularly. A Job has an unknown status if the connection
            between the Scheduler and the Runner is lost.
        - SLEEPING: Waiting for a scheduled epoch to run
        - WAITING: Ready to run and waiting for a broker
        - RUNNING: Currently running
        - TERMINATED: Terminated by a broker
        - STOPPED: Job stopped itself
    """
    UNKNOWN = 0
    SLEEPING = 1
    WAITING = 2
    RUNNING = 3
    TERMINATED = 4
    STOPPED = 5


class Job:
    """A unit of work
    Is given by a user to the Scheduler, that will pass it (at the
    right time) to an available Runner to be run.

    Attributes:
        - identifier: Integer, unique id
        - user: Integer, user id
        - status: JobStatus, represents the status of the job
        - description: String, a description of the job
        - epoch_sent: Integer, epoch when the job was sent
        - epoch_received: Integer, epoch when the job was received
    """

    def __init__(self, user, payload):
        self.identifier = 0
        self.user = user
        self.status = JobStatus.WAITING.value
        self.description = payload["description"]
        self.epoch_sent = None
        self.epoch_received = int(time())

    def __str__(self):
        return (
            f"Job #{self.identifier}\n"
            f"User: {self.user}\n"
            f"Status: {self.status}\n"
            f"Received at {self.epoch_received}\n"
            f"Description: {self.description}"
        )

    def to_json(self):
        "Serialize a Job in JSON format"
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )


class Scheduler:
    """

    Attributes:
    """
    def __init__(self, sqlite_file="data.db"):
        self.queue = []
        self.sqlite_file = sqlite_file
        self.__init_sqlite_db(sqlite_file)

    def __init_sqlite_db(self, sqlite_file):
        """Initialize the SQLite database

        If a database is not found, create a new one with an empty table

        Args:
            sqlite_file (str): Path to the .db file
        """
        logging.info("Initializing database")
        db_exist = isfile(sqlite_file)
        conn = sqlite3.connect(sqlite_file)
        self.conn = conn
        if db_exist:
            logging.info("Loading data from %s", sqlite_file)
            self.__db_warm_start()
        else:
            logging.info("Can't find existing db at %s", sqlite_file)
            logging.info("Starting one from scratch")
            self.__db_cold_start()

    def __db_warm_start(self):
        conn = self.conn
        cursor = conn.cursor()

    def __db_cold_start(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE jobs ("
            "id INT PRIMARY KEY,"
            "user INT,"
            "status INT,"
            "description MEDIUMTEXT,"
            "epoch_sent INT,"
            "epoch_received INT"
            ")"
        )
        conn.commit()


def append_job(user):
    """Receives a POST request to append a new job to the scheduler"""
    logging.info("Received POST request from %s", user)
    job = Job(user, request.POST)
    print(job)


def setup_rooting(app):
    """Configures explicit rooting"""
    app.route("/<user>", "POST", append_job)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    schedule = Scheduler("data.db")  # pylint: disable=C0103
    web_app = Bottle()  # pylint: disable=C0103
    setup_rooting(web_app)
    run(web_app, host="localhost", port=8080)
