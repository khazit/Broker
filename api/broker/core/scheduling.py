"""Scheduling module.

Controls the order in which the jobs are executed.
"""


from broker.core.database import DataBaseManager
from broker.core.utils import JobStatus


class Scheduler:
    """Scheduling agent.

    Manages the order in which the jobs are executed and is the main interface
    between users and runners

    Attributes:
        db_manager: DataBaseManager, wrapper for SQLite3 related methods
    """
    def __init__(self, sqlite_file="data.db"):
        self.db_manager = DataBaseManager(sqlite_file)

    def add_job(self, job):
        """Adds a new job to the schedule."""
        self.db_manager.add_job(job)

    def get_jobs(self):
        """Gets all jobs in schedule."""
        return self.db_manager.get_jobs()

    def get_job_by_id(self, identifier):
        """Gets a job given an identifier"""
        return self.db_manager.get_job_by_id(identifier)

    def update_job_status(self, identifier, status):
        """Updates a job's status."""
        status = getattr(JobStatus, status).value
        self.db_manager.update_job(identifier, status=status)

    def remove_job(self, identifier):
        """Removes an existing job from the schedule."""
        self.db_manager.remove_job(identifier)

    @property
    def n_jobs(self):
        """Returns number of jobs in the schedule."""
        return self.db_manager.get_n_jobs()

    def get_job_status(self, identifier):
        """Returns a job's current status."""
        return self.db_manager.get_job_status(identifier)

    def get_next(self):
        """Returns the next job on the queue."""
        queue = self.db_manager.select_jobs_by(status=2)
        if len(queue) != 0:
            return queue[0]
        return None
