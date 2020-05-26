"""Utility objects and functions"""


import json
import logging
from time import time
from enum import Enum
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class JobStatus(Enum):
    """Represent the status of a job

        - UNKNOWN: Given that a runner can run on a different network,
            a job has an unknown status if the connection between the Scheduler
            and the Runner can't be established'.
        - SLEEPING: Waiting for a scheduled epoch to run
        - WAITING: Ready to run and waiting for a runner
        - RUNNING: Currently running
        - TERMINATED: Terminated by itself or by a runner after an error
        - DONE: Successfully executed
    """
    UNKNOWN = 0
    SLEEPING = 1
    WAITING = 2
    RUNNING = 3
    TERMINATED = 4
    DONE = 5


class Job(Base):
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

    __tablename__ = "jobs"
    identifier = Column(Integer, primary_key=True)
    user = Column(String)
    status = Column(Integer)
    description = Column(Integer)
    epoch_received = Column(Integer)

    @staticmethod
    def from_payload(payload):
        """Create a Job instance given a payload dict

        Args:
            payload (dict): Job info dict

        Returns:
            (broker.utils.Job) instance
        """
        try:
            job = Job(
                user=payload["user"],
                status=JobStatus.WAITING.value,
                description=payload["description"],
                epoch_received=int(time()),
            )
            return job
        except KeyError:
            logging.error("Incorrect payload. Can't create job instance")

    def __repr__(self):
        return f"Job<id={self.identifier}, status={self.status}>"

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
