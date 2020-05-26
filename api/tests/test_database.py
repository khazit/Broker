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
    """
    id	user	status	description	            epoch_received
    0	Tyler	2	    sleep 10	            270270270
    3	Boy	    0	    echo "I speak giberish"	2702700014
    4	Scott	4	    df -h	                174585230
    5	Jim	    5	    echo "He done"	        155647850
    7	Creator	2	    docker ps	            14233658740
    8	Good	2	    sleep 15	            1244
    """
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
        "description": "Deadlift"
    }
    return Job.from_payload(payload) 

@pytest.fixture
def dummy_job_2():
    payload = {
        "user": "Brian",
        "description": "Deadlift"
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

    warm_db.db_remove_job(7)
    assert warm_db.db_n_jobs() == 2
    assert warm_db.db_n_jobs(active=False) == 4

    warm_empty_db.db_remove_job(0) 
    assert warm_empty_db.db_n_jobs() == 0
    assert warm_empty_db.db_n_jobs(active=False) == 0

def test_update_job_status(warm_db):
    warm_db.db_update_job_status(7, JobStatus.TERMINATED.value)
    assert warm_db.db_n_jobs() == 2
    assert warm_db.db_n_jobs(active=False) == 6
