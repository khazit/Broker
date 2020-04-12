import pytest

import os
from shutil import copyfile
from os.path import isfile
from broker.scheduling import Job, Scheduler

@pytest.fixture
def warm_scheduler():
    """Creates a Scheduler instance from an existing db file"""
    return Scheduler("tests/test_data/data.db")

@pytest.fixture
def cold_scheduler():
    """Creates a Scheduler instance from scratch"""
    return Scheduler("tests/test_data/no_data.db")

def test_warm_init_sqlite_db(warm_scheduler):
    assert warm_scheduler.last_job_id == 2
    assert len(warm_scheduler.jobs) == 2
   
def test_cold_init_sqlite_db(cold_scheduler):
    assert isfile("tests/test_data/no_data.db")
    assert cold_scheduler.last_job_id == 0 
    assert len(cold_scheduler.jobs) == 0
    if isfile("tests/test_data/no_data.db"):
        os.remove("tests/test_data/no_data.db")

def test_add_remove_job(warm_scheduler):
    # Copy file to recover it later
    copyfile("tests/test_data/data.db", "tests/test_data/recovery.db")
    payload = {
        "description": "Ceci est temporaire"
    }
    warm_scheduler.add_job("RyanTheTemp", payload)
    assert len(warm_scheduler.jobs) == 3
    assert warm_scheduler.last_job_id == 3
    warm_scheduler.remove_job(3)
    assert len(warm_scheduler.jobs) == 2
    assert warm_scheduler.last_job_id == 2
    # Recover original db file
    os.remove("tests/test_data/data.db")
    os.rename("tests/test_data/recovery.db", "tests/test_data/data.db")

def test_get_jobs(warm_scheduler):
    assert len(warm_scheduler.get_jobs(user="ali")) == 1
    assert len(warm_scheduler.get_jobs(user="all")) == 2
    assert warm_scheduler.get_jobs(user="ben")[0].user == "ben"
