"""
Scheduling module. Controls the order in which the jobs are executed.
"""


import json
from enum import Enum
from time import time
from broker.database import DataBaseManager


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
        self.db_manager = DataBaseManager(sqlite_file)
        self.jobs = self.db_manager.init_sqlite_db()

    def add_job(self, payload):
        """Adds a new Job. Called after a POST request from a Client

        Args:
            user: String, user id
            payload: Dict, POST request payload
        """
        job = Job(self.db_manager.last_id+1, payload)
        # Append Job to list
        self.jobs.append(job)
        # Update db
        self.db_manager.db_add_job(job)

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
        self.db_manager.db_remove_job(identifier)

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


    def __str__(self):
        res = f"Managing {len(self.jobs)} jobs:\n"
        for job in self.jobs:
            res += str(job) + "\n"
        return res
