"""Database module"""


from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session

from broker.core.models import Base, Job, Event, LogFile
from broker.core.utils import JobStatus


# pylint: disable=no-member


class DataBaseManager():
    """Wrapper for SQL database related operations

    Attributes:
        sqlite_file (string): Path of the SQLite database file
        engine (sqlalchemy.engine.Engine): Database engine
        session (sqlalchemy.orm.session.Session): Session
    """

    def __init__(self, sqlite_file="data.db"):
        self.sqlite_file = sqlite_file
        self.engine = create_engine(f"sqlite:///{self.sqlite_file}")
        Session = scoped_session(sessionmaker(bind=self.engine))
        self.session = Session()
        Base.metadata.create_all(self.engine)  # Create db if needed


    # ------------------------------ Jobs ------------------------------ #

    def add_job(self, job):
        """Adds a job to the database."""
        self.session.add(job)
        job.events.append(Event(status=JobStatus.WAITING.value))
        self.session.commit()

    def get_jobs(self):
        """Returns all jobs from the database"""
        return self.session.query(Job).all()

    def get_job_by_id(self, identifier):
        """Returns a job given an id."""
        if self._job_exists(identifier):
            return self.session.query(Job).filter_by(identifier=identifier).first()
        return None

    def update_job(self, identifier, **kwargs):
        """Updates a job."""
        if self._job_exists(identifier):
            job = self.get_job_by_id(identifier)
            for key, value in kwargs.items():
                if key == "status":
                    job.events.append(Event(status=value))
                else:
                    setattr(job, key, value)
            self.session.commit()
        else:
            raise IndexError(f"Job #{identifier} not found")

    def remove_job(self, identifier):
        """Removes a job the database given an identifier"""
        if self._job_exists(identifier):
            job = self.session.query(Job).filter(Job.identifier == identifier).first()
            self.session.delete(job)
            self.session.commit()
        else:
            raise IndexError(f"Job #{identifier} not found")

    def get_n_jobs(self):
        """Counts number of jobs in database"""
        return self.session.query(Job).count()

    def select_jobs_by(self, **kwargs):
        """Selects jobs based on given args."""
        if len(kwargs) > 1:
            raise NotImplementedError("Can't select based on 2 args.")
        if "status" in kwargs:
            sub = (self.session)\
                .query(
                    Event.job_id,
                    Event.status,
                    func.max(Event.timestamp)
                )\
                .group_by(Event.job_id)\
                .subquery()
            return (self.session)\
                    .query(Job)\
                    .join((sub, sub.c.job_id == Job.identifier))\
                    .filter(sub.c.status == kwargs["status"])\
                    .all()
        return self.session.query(Job).filter_by(**kwargs).all()

    def get_job_status(self, identifier):
        """Returns a job's current status"""
        if self._job_exists(identifier):
            return (self.session)\
                .query(
                    Event.job_id,
                    Event.status,
                    func.max(Event.timestamp)
                )\
                .filter(Event.job_id == identifier)\
                .first()\
                .status
        raise IndexError(f"Job #{identifier} not found")

    # --------------------------- Log files ---------------------------- #

    def add_logfile(self, job_id):
        """Assign a log file to a job given its identifier.

        Returns:
            (str) logfile name in the server's file system
        """
        job = self.get_job_by_id(job_id)
        if job is not None:
            job.logfile = LogFile(job_id=job_id)
            return job.logfile.filename
        raise IndexError(f"Job #{job_id} not found.")

    def get_logfile(self, job_id):
        """Returns a logfile given its job identifier."""
        if self._job_exists(job_id):
            return self.session.query(LogFile).filter_by(job_id=job_id).first()
        raise IndexError(f"Job #{job_id} not found.")


    # --------------------------- Utilities ---------------------------- #

    def _job_exists(self, identifier):
        return (self.session)\
            .query(Job.identifier)\
            .filter_by(identifier=identifier)\
            .scalar() is not None
