"""SQLAlchemy data models."""


import json
import logging
from time import time
from uuid import uuid4

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


# pylint: disable=R0903
Base = declarative_base()


class Job(Base):
    """A unit of work
    Is given by a user to the Scheduler, that will pass it (at the
    right time) to an available Runner to be run.

    Attributes:
        identifier: Integer, unique id
        user: String, user id
        events: List of updates to the job's status
        description: String, a description of the job
        epoch_received: Integer, epoch when the job was received
    """

    __tablename__ = "jobs"
    identifier = Column(Integer, primary_key=True)
    user = Column(String)
    events = relationship("Event", cascade="all, delete-orphan")
    description = Column(String)
    command = Column(String)
    logfile = relationship("LogFile", uselist=False, cascade="all, delete-orphan")

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
                description=payload["description"],
                command=payload["command"],
            )
            return job
        except KeyError:
            logging.error("Incorrect payload. Can't create job instance")

    def __repr__(self):
        return f"Job<id={self.identifier}, status={self.events[-1].status}>"

    def __str__(self):
        return (
            "---\n"
            f"Job #{self.identifier}\n"
            f"User: {self.user}\n"
            f"Status: {self.events[-1].status}\n"
            f"Command: {self.command}\n"
            f"Description: {self.description}\n"
            "---"
        )

    def to_dict(self):
        "Returns a Job in Python dict format"
        return {
            "identifier": self.identifier,
            "user": self.user,
            "events": [e.to_dict() for e in self.events],
            "description": self.description,
            "command": self.command
        }

    def to_json(self):
        "Serializes a Job in JSON format"
        return json.dumps(self.to_dict())


class Event(Base):
    """An event is when a job's status is updated.

    See `broker.core.utils.JobStatus` for a list possible states.

    Attributes:
        identifier: Unique id.
        job_id: Foreign key. Id of the job that was updated.
        timestamp: Float, epoch when the status was updated.
        status: Integer, status after update.

    """

    __tablename__ = "events"
    identifier = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.identifier"))
    timestamp = Column(Float)
    status = Column(Integer)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timestamp = time()

    def __repr__(self):
        return f"Event<id={self.identifier}, job={self.job_id}>"

    def to_dict(self):
        """Returns an Even in a Python dict format."""
        return {
            "identifier": self.identifier,
            "timestamp": self.timestamp,
            "status": self.status,
        }


class LogFile(Base):
    """A job's logging file.

    Attribute:
        identifier: Unique id.
        job_id: Foreign key. Id of the job.
        filename: Filename.
    """

    __tablename__ = "logfiles"
    identifier = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.identifier"))
    filename = Column(String)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filename = str(uuid4()).replace("-", "")

    def __repr__(self):
        return f"LogFile<id={self.identifier}, job={self.job_id}>"
