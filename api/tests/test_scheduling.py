import pytest

import os
from shutil import copyfile
from os.path import isfile
from broker.scheduling import Scheduler
from broker.utils import Job

@pytest.fixture
def warm_scheduler():
    """Creates a Scheduler instance from an existing db file"""
    return Scheduler("tests/test_data/data.db")

@pytest.fixture
def cold_scheduler():
    """Creates a Scheduler instance from scratch"""
    return Scheduler("tests/test_data/no_data.db")

def test_warm_init_sqlite_db(warm_scheduler):
    assert warm_scheduler.db_manager.last_id == 8
    assert len(warm_scheduler.jobs) == 3
   
def test_cold_init_sqlite_db(cold_scheduler):
    assert isfile("tests/test_data/no_data.db")
    assert cold_scheduler.db_manager.last_id == 0 
    assert len(cold_scheduler.jobs) == 0
    if isfile("tests/test_data/no_data.db"):
        os.remove("tests/test_data/no_data.db")

def test_add_remove_job(warm_scheduler):
    # Copy file to recover it later
    copyfile("tests/test_data/data.db", "tests/test_data/recovery.db")
    payload = {
        "user": "RyanTheTemp",
        "description": "Ceci est temporaire"
    }
    warm_scheduler.add_job(payload)
    assert len(warm_scheduler.jobs) == 4
    assert warm_scheduler.db_manager.last_id == 9
    warm_scheduler.remove_job(9)
    assert len(warm_scheduler.jobs) == 3
    assert warm_scheduler.db_manager.last_id == 8
    # Recover original db file
    os.remove("tests/test_data/data.db")
    os.rename("tests/test_data/recovery.db", "tests/test_data/data.db")

def test_get_jobs(warm_scheduler):
    assert len(warm_scheduler.get_jobs()) == 3
    assert len(warm_scheduler.get_jobs(active=False)) == 6

def test_get_next(warm_scheduler):
    assert warm_scheduler.get_next().user == "Tyler"
    assert warm_scheduler.get_next().description == "sleep 10"

def test_update_status(warm_scheduler):
    # Copy file to recover it later
    copyfile("tests/test_data/data.db", "tests/test_data/recovery.db")
    
    warm_scheduler.update_job_status(0, "RUNNING")
    assert len(warm_scheduler.jobs) == 2
    
    # Recover original db file
    os.remove("tests/test_data/data.db")
    os.rename("tests/test_data/recovery.db", "tests/test_data/data.db")

