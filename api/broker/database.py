"""Database module"""


import logging
from os.path import isfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import or_, func
from broker.utils import Job
# pylint: disable=no-member


Session = sessionmaker()


class DataBaseManager():
    """Wrapper for SQL database related operations

    Attributes:
        sqlite_file (string): Path of the SQLite database file
        engine (sqlalchemy.engine.Engine): Database engine
        session (sqlalchemy.orm.session.Session): Session
        last_id (id): Last ID used
    """

    def __init__(self, sqlite_file="data.db"):
        self.sqlite_file = sqlite_file
        self.engine = create_engine(f"sqlite:///{self.sqlite_file}")
        Session.configure(bind=self.engine)  # Bind engine to session
        Job.metadata.create_all(self.engine)  # Create db if needed
        self.session = Session()
        self.last_id = None
        self.init_db()

    def init_db(self):
        """Initializes the database

        If a database is not found, create a new one with an empty table

        Returns:
            List of Jobs from db file (empty list if cold start)
        """
        logging.info("Initializing database")
        db_exist = isfile(self.sqlite_file)
        if db_exist:
            logging.info("Loading data from %s", self.sqlite_file)
            jobs = self.db_warm_start()
            #  if db file exists but empty db
            if self.db_get_last_id() is None:
                self.last_id = 0
            else:
                self.last_id = self.db_get_last_id()
        else:
            logging.info("Can't find existing db at %s", self.sqlite_file)
            logging.info("Starting one from scratch")
            jobs = []
            self.last_id = 0
        return jobs

    def db_get_last_id(self):
        """Gets value of last used id"""
        return self.session.query(func.max(Job.identifier)).scalar()

    def db_get_jobs(self, active=True):
        """Returns jobs from the database

        Args:
            active (bool): If true, returns active jobs only"""
        if active:
            return self.session.query(Job).\
                filter(or_(Job.status == 1, Job.status == 2)).\
                all()
        return self.session.query(Job).all()

    def db_n_jobs(self, active=True):
        """Counts number of jobs in database

        Args:
            active (bool): If true, count active jobs only"""
        if active:
            return self.session.query(Job).\
                filter(or_(Job.status == 1, Job.status == 2)).\
                count()
        return self.session.query(Job).\
            count()

    def db_warm_start(self):
        """Warm start from an existing db file

        Returns:
            (list) Active jobs
        """
        jobs = self.db_get_jobs(active=True)
        logging.info("Found %i active jobs in database", len(jobs))
        return jobs

    def db_add_job(self, job):
        """Adds a job entry to the database given an identifier"""
        job.identifier = self.last_id + 1
        self.session.add(job)
        self.session.commit()
        self.last_id = self.db_get_last_id()

    def db_remove_job(self, identifier):
        """Removes a job entry from the database given an identifier"""
        self.session.query(Job).filter_by(identifier=identifier).delete()
        self.session.commit()
        self.last_id = self.db_get_last_id()

    def db_update_job_status(self, identifier, status):
        """Updates a job's status"""
        job = self.session.query(Job).filter_by(identifier=identifier).first()
        job.status = status
        self.session.commit()
