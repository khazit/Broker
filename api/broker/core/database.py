"""Database module"""


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from broker.core.models import Job


# pylint: disable=no-member

Session = sessionmaker()


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
        Session.configure(bind=self.engine)  # Bind engine to session
        Job.metadata.create_all(self.engine)  # Create db if needed
        self.session = Session()

    def add_job(self, job):
        """Adds a job to the database."""
        self.session.add(job)
        self.session.commit()

    def get_jobs(self):
        """Returns all jobs from the database"""
        return self.session.query(Job).all()

    def get_job_by_id(self, identifier):
        """Returns a job given an id."""
        if not self._job_exists(identifier):
            raise IndexError(f"Job #{identifier} not found")
        return self.session.query(Job).filter_by(identifier=identifier).first()

    def update_job(self, identifier, **kwargs):
        """Updates a job."""
        if self._job_exists(identifier):
            job = self.get_job_by_id(identifier)
            for key, value in kwargs.items():
                setattr(job, key, value)
            self.session.commit()
        else:
            raise IndexError(f"Job #{identifier} not found")

    def remove_job(self, identifier):
        """Removes a job the database given an identifier"""
        if self._job_exists(identifier):
            self.session.query(Job.identifier).filter_by(identifier=identifier).delete()
            self.session.commit()
        else:
            raise IndexError(f"Job #{identifier} not found")

    def get_n_jobs(self):
        """Counts number of jobs in database"""
        return self.session.query(Job).count()

    def select_jobs_by(self, **kwargs):
        """Selects jobs based on given args."""
        return self.session.query(Job).filter_by(**kwargs).all()

    def _job_exists(self, identifier):
        return (self.session)\
            .query(Job.identifier)\
            .filter_by(identifier=identifier)\
            .scalar() is not None
