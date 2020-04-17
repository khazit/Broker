"""Database module"""


import logging
import sqlite3
from os.path import isfile
from broker.utils import Job


class DataBaseManager():
    """Wrapper for SQLite3 related operations

    Attributes:
        sqlite_file: String, path of the SQLite database file
        conn: SQLite connexion object
        last_id: Integer, last id used in the jobs table
    """

    def __init__(self, sqlite_file="data.db"):
        self.sqlite_file = sqlite_file
        self.conn = None
        self.last_id = None
        self.init_sqlite_db()

    def init_sqlite_db(self):
        """Initializes the SQLite database

        If a database is not found, create a new one with an empty table

        Returns:
            List of Jobs from db file (empty list if cold start)
        """
        logging.info("Initializing database")
        db_exist = isfile(self.sqlite_file)
        conn = sqlite3.connect(self.sqlite_file, check_same_thread=False)
        self.conn = conn
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
            jobs = self.db_cold_start()
            self.last_id = 0
        return jobs

    def db_query(self, query, args=(), one=False):
        """Wrappes a SQLite3 query"""
        cursor = self.conn.cursor().execute(query, args)
        row = cursor.fetchall()
        cursor.close()
        return (row[0] if row else None) if one else row

    def db_get_last_id(self):
        """Get value of last used id"""
        return self.db_query("SELECT MAX(id) FROM jobs", one=True)[0]

    def db_warm_start(self):
        """Warm start from an existing db file

        Returns:
            List of Jobs (could be empty if db file empty)
        """
        jobs = []
        all_rows = self.db_query("SELECT * from jobs")
        logging.info("Found %i jobs in database", len(all_rows))
        for row in all_rows:
            # Create a Job instance from a tuple
            # Not beautiful, need to find a better way to do it
            job = Job(None, None)
            for i, key in enumerate(vars(job)):
                vars(job)[key] = row[i]
            jobs.append(job)
        return jobs

    def db_cold_start(self):
        """Cold start: creates a database file with an empty table

        Returns:
            Empty list
        """
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE jobs ("
            "id INT PRIMARY KEY,"
            "user VARCHAR(30),"
            "status INT,"
            "description MEDIUMTEXT,"
            "epoch_received INT"
            ")"
        )
        conn.commit()
        return []

    def db_add_job(self, job):
        """Add a job entry to the database given an identifier"""
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO jobs VALUES ("
            f"'{job.identifier}',"
            f"'{job.user}',"
            f"'{job.status}',"
            f"'{job.description}',"
            f"'{job.epoch_received}'"
            ")"
        )
        conn.commit()
        self.last_id += 1

    def db_remove_job(self, identifier):
        """Remove a job entry from the database given an identifier"""
        conn = self.conn
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM jobs WHERE id = {identifier}")
        conn.commit()
        self.last_id -= 1
