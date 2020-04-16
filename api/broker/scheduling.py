"""
Scheduling module. Controls the order in which the jobs are executed.
"""


from broker.database import DataBaseManager
from broker.utils import Job


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
