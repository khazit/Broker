import os
from shutil import copyfile
import pytest
from broker.database import DataBaseManager
from broker.utils import Job, JobStatus

########################################################################################
# Fixtures
########################################################################################

@pytest.fixture
def warm_db():
    copyfile("tests/test_data/data.db", "tests/test_data/backup")
    yield DataBaseManager("tests/test_data/data.db")
    os.remove("tests/test_data/data.db")
    os.rename("tests/test_data/backup", "tests/test_data/data.db")

@pytest.fixture
def warm_empty_db():
    copyfile("tests/test_data/empty.db", "tests/test_data/empty_backup")
    yield DataBaseManager("tests/test_data/empty.db")
    os.remove("tests/test_data/empty.db")
    os.rename("tests/test_data/empty_backup", "tests/test_data/empty.db")   

@pytest.fixture
def cold_db():
    yield DataBaseManager("/tmp/no.db")
    os.remove("/tmp/no.db")

@pytest.fixture
def dummy_job_1():
    payload = {
        "user": "Hafthor",
        "description": "Deadlift",
        "command": "Lift"
    }
    return Job.from_payload(payload) 

@pytest.fixture
def dummy_job_2():
    payload = {
        "user": "Brian",
        "description": "Deadlift",
        "command": "Lift harder"
    }
    return Job.from_payload(payload) 

########################################################################################
# Tests
########################################################################################

def test_init_db_warm(warm_db):
    assert warm_db.db_n_jobs() == 3
    assert warm_db.db_n_jobs(active=False) == 6 

def test_init_db_warm_empty(warm_empty_db):
    assert warm_empty_db.db_n_jobs() == 0
    assert warm_empty_db.db_n_jobs(active=False) == 0

def test_init_db_cold(cold_db):
    assert cold_db.db_n_jobs() == 0
    assert cold_db.db_n_jobs(active=False) == 0   

def test_add_job(warm_db, warm_empty_db, dummy_job_1, dummy_job_2):
    warm_db.db_add_job(dummy_job_1)
    assert warm_db.db_n_jobs() == 4
    assert warm_db.db_n_jobs(active=False) == 7

    warm_empty_db.db_add_job(dummy_job_2) 
    assert warm_empty_db.db_n_jobs() == 1
    assert warm_empty_db.db_n_jobs(active=False) == 1

def test_remove_job(warm_db, warm_empty_db):
    warm_db.db_remove_job(5)
    assert warm_db.db_n_jobs() == 3
    assert warm_db.db_n_jobs(active=False) == 5

    warm_db.db_remove_job(162)
    assert warm_db.db_n_jobs() == 3
    assert warm_db.db_n_jobs(active=False) == 5
    
    warm_db.db_remove_job(7)
    assert warm_db.db_n_jobs() == 2
    assert warm_db.db_n_jobs(active=False) == 4

    warm_empty_db.db_remove_job(0) 
    assert warm_empty_db.db_n_jobs() == 0
    assert warm_empty_db.db_n_jobs(active=False) == 0

    warm_empty_db.db_remove_job(270) 
    assert warm_empty_db.db_n_jobs() == 0
    assert warm_empty_db.db_n_jobs(active=False) == 0

def test_update_job_status(warm_db):
    warm_db.db_update_job_status(7, JobStatus.TERMINATED.value)
    assert warm_db.db_n_jobs() == 2
    assert warm_db.db_n_jobs(active=False) == 6
