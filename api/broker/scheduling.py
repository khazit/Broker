"""
Scheduling module. Controls the order in which the jobs are executed.
"""


from broker.database import DataBaseManager
from broker.utils import Job, JobStatus


class Scheduler:
    """Scheduling agent.

    Manages the order in which the Jobs are executed and is the main interface
    between users and Runners

    Attributes:
        db_manager: DataBaseManager, wrapper for SQLite3 related methods
        jobs: List, list of Job objects

    NOTE: A list is not a good data structure here. For now, it's a
        placeholder. But in the future, there need to be something that acts
        like a queue, but which could also be accessed in O(1) (using ids)
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

    def get_jobs(self, active=True):
        """Returns a list of all jobs

        Args:
            active: Boolean, if true returns only active jobs

        Returns:
            List of Job instances
        '"""
        if active:
            return self.jobs
        # if not
        return self.db_manager.db_warm_start(active=False)

    def get_next(self):
        """Returns the next job on the queue

        Returns:
            Job object
        """
        if len(self.jobs) == 0:
            return None
        return self.jobs[0]

    def update_job_status(self, identifier, status):
        """Updates a job's status.

        Typically a request coming from a runner
        """
        status = getattr(JobStatus, status).value
        # Update the status in memory
        for job in self.jobs:
            if job.identifier == identifier:
                job.status = status
                break
        self.__refresh_jobs()
        # Update the status on the SQL table
        self.db_manager.db_update_job_status(identifier, status)

    def __refresh_jobs(self):
        """Drops inactive jobs from memory"""
        for idx, job in enumerate(self.jobs):
            if job.status != JobStatus.SLEEPING.value and \
               job.status != JobStatus.WAITING.value:
                self.jobs.pop(idx)

    def __str__(self):
        res = f"Managing {len(self.jobs)} jobs:\n"
        for job in self.jobs:
            res += str(job) + "\n"
        return res
