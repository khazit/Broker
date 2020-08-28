"""SQLAlchemy data models."""

import json
import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from broker.core.utils import JobStatus


Base = declarative_base()


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
    description = Column(String)
    command = Column(String)

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
                command=payload["command"],
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
            f"Command: {self.command}\n"
            f"Description: {self.description}\n"
            "---"
        )

    def to_dict(self):
        "Returns a Job in Python dict format"
        return {
            "identifier": self.identifier,
            "user": self.user,
            "status": self.status,
            "description": self.description,
            "command": self.command
        }

    def to_json(self):
        "Serializes a Job in JSON format"
        return json.dumps(self.to_dict())
