"""
Scheduling module. Controls the order in which the jobs are executed.
"""


import json
import logging
import sqlite3
from enum import Enum
from os.path import isfile
from time import time


class JobStatus(Enum):
    """Represent the status of a job

        - UNKNOWN: Given that a Runner can run on a different network,
            the Scheduler asks for an update on the status of all the jobs
            regularly. A Job has an unknown status if the connection
            between the Scheduler and the Runner is lost.
        - SLEEPING: Waiting for a scheduled epoch to run
        - WAITING: Ready to run and waiting for a broker
        - RUNNING: Currently running
        - TERMINATED: Terminated by itself or by a broker after an error
        - DONE: Successfully executed
    """
    UNKNOWN = 0
    SLEEPING = 1
    WAITING = 2
    RUNNING = 3
    TERMINATED = 4
    DONE = 5


class Job:
    """A unit of work
    Is given by a user to the Scheduler, that will pass it (at the
    right time) to an available Runner to be run.

    Attributes:
        - identifier: Integer, unique id
        - user: String, user id
        - status: JobStatus, represents the status of the job
        - description: String, a description of the job
        - epoch_received: Integer, epoch when the job was received
    """

    def __init__(self, identifier, payload):
        self.identifier = identifier
        if payload is None:
            self.user = None
            self.status = None
            self.description = None
            self.epoch_received = None
        else:
            self.user = payload["user"]
            self.status = JobStatus.WAITING.value
            self.description = payload["description"]
            self.epoch_received = int(time())

    def __str__(self):
        return (
            "---\n"
            f"Job #{self.identifier}\n"
            f"User: {self.user}\n"
            f"Status: {self.status}\n"
            f"Received at {self.epoch_received}\n"
            f"Description: {self.description}\n"
            "---"
        )

    def to_dict(self):
        "Returns a Job in Python dict format"
        return self.__dict__

    def to_json(self):
        "Serializes a Job in JSON format"
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4
        )


class Scheduler:
    """Scheduling agent.

    Manages the order in which the Jobs are executed and is the main interface
    between users and Runners

    Attributes:
    """
    def __init__(self, sqlite_file="data.db"):
        self.jobs = []
        self.sqlite_file = sqlite_file
        self.last_job_id = self.__init_sqlite_db(sqlite_file)

    def add_job(self, payload):
        """Adds a new Job. Called after a POST request from a Client

        Args:
            user: String, user id
            payload: Dict, POST request payload
        """
        job = Job(self.last_job_id+1, payload)
        self.last_job_id += 1
        # Append Job to list
        self.jobs.append(job)
        # Update db
        self.__db_add_job(job)

    def remove_job(self, identifier):
        """Removes an existing Job from Scheduler

        Args:
            identifier: Integer, a unique indentifier
        """
        # Remove Job from list
        idx = 0
        while idx < len(self.jobs):
            if self.jobs[idx].identifier == identifier:
                self.jobs.pop(idx)
                break
            idx += 1
        # Remove job from db
        self.__db_remove_job(identifier)
        self.last_job_id = self.__db_get_last_id()

    def get_jobs(self, user):
        """Returns a list the user's jobs

        Args:
            user: String, unique user identifier

        Returns:
            List of Job instances
        '"""
        if user == "all":
            return self.jobs
        # if not
        res = []
        for job in self.jobs:
            if job.user == user:
                res.append(job)
        return res

    def __init_sqlite_db(self, sqlite_file):
        """Initializes the SQLite database

        If a database is not found, create a new one with an empty table

        Args:
            sqlite_file (str): Path to the .db file
        """
        logging.info("Initializing database")
        db_exist = isfile(sqlite_file)
        conn = sqlite3.connect(sqlite_file, check_same_thread=False)
        self.conn = conn
        if db_exist:
            logging.info("Loading data from %s", sqlite_file)
            self.__db_warm_start()
            #  if db file exists but empty db
            if self.__db_get_last_id() is None:
                return 0
            return self.__db_get_last_id()
        # if not
        logging.info("Can't find existing db at %s", sqlite_file)
        logging.info("Starting one from scratch")
        self.__db_cold_start()
        return 0

    def __db_query(self, query, args=(), one=False):
        """Wrappes a SQLite3 query"""
        cursor = self.conn.cursor().execute(query, args)
        row = cursor.fetchall()
        cursor.close()
        return (row[0] if row else None) if one else row

    def __db_get_last_id(self):
        """Get value of last used id"""
        return self.__db_query("SELECT MAX(id) FROM jobs", one=True)[0]

    def __db_warm_start(self):
        all_rows = self.__db_query("SELECT * from jobs")
        logging.info("Found %i jobs in database", len(all_rows))
        for row in all_rows:
            # Create a Job instance from a tuple
            # Not beautiful, need to find a better way to do it
            job = Job(None, None)
            for i, key in enumerate(vars(job)):
                vars(job)[key] = row[i]
            self.jobs.append(job)

    def __db_cold_start(self):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE jobs ("
            "id INT PRIMARY KEY,"
            "user VARCHAR(30),"
            "status INT,"
            "description MEDIUMTEXT,"
            "epoch_received INT"
            ")"
        )
        conn.commit()

    def __db_add_job(self, job):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO jobs VALUES ("
            f"'{job.identifier}',"
            f"'{job.user}',"
            f"'{job.status}',"
            f"'{job.description}',"
            f"'{job.epoch_received}'"
            ")"
        )
        conn.commit()

    def __db_remove_job(self, identifier):
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM jobs WHERE id = {identifier}")
        conn.commit()

    def __str__(self):
        res = f"Managing {len(self.jobs)} jobs:\n"
        for job in self.jobs:
            res += str(job) + "\n"
        return res
