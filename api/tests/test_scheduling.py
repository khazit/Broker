import pytest
import os
from shutil import copyfile
from os.path import isfile
from broker.scheduling import Scheduler
from broker.utils import Job

########################################################################################
# Fixtures
########################################################################################

@pytest.fixture
def warm_scheduler():
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
    yield Scheduler("tests/test_data/data.db")
    os.remove("tests/test_data/data.db")
    os.rename("tests/test_data/backup", "tests/test_data/data.db")

@pytest.fixture
def warm_empty_scheduler():
    copyfile("tests/test_data/empty.db", "tests/test_data/empty_backup")
    yield Scheduler("tests/test_data/empty.db")
    os.remove("tests/test_data/empty.db")
    os.rename("tests/test_data/empty_backup", "tests/test_data/empty.db")   

@pytest.fixture
def cold_scheduler():
    yield Scheduler("/tmp/no.db")
    os.remove("/tmp/no.db")

########################################################################################
# Tests
########################################################################################

def test_warm_init(warm_scheduler):
    assert len(warm_scheduler.jobs) == 3

def test_warm_empty_init(warm_empty_scheduler):
    assert len(warm_empty_scheduler.jobs) == 0

def test_cold_init(cold_scheduler):
    assert len(cold_scheduler.jobs) == 0

def test_add_job(warm_scheduler, warm_empty_scheduler, cold_scheduler):
    payload = {
        "user": "RyanTheTemp",
        "description": "ls /tmp"
    }
    
    warm_scheduler.add_job(Job.from_payload(payload))
    assert len(warm_scheduler.jobs) == 4
    assert warm_scheduler.db_manager.last_id == 9

    warm_empty_scheduler.add_job(Job.from_payload(payload))
    assert len(warm_empty_scheduler.jobs) == 1
    assert warm_empty_scheduler.db_manager.last_id == 1

    cold_scheduler.add_job(Job.from_payload(payload))
    assert len(cold_scheduler.jobs) == 1
    assert cold_scheduler.db_manager.last_id == 1
    
def test_remove_jobs(warm_scheduler):
     # Index out of range test
    with pytest.raises(IndexError):
        warm_scheduler.remove_job(270)

    warm_scheduler.remove_job(8)
    assert len(warm_scheduler.jobs) == 2
    assert warm_scheduler.db_manager.last_id == 7


def test_get_jobs(warm_scheduler):
    assert len(warm_scheduler.get_jobs()) == 3
    assert len(warm_scheduler.get_jobs(active=False)) == 6


def test_get_next(warm_scheduler):
    assert warm_scheduler.get_next().user == "Tyler"
    assert warm_scheduler.get_next().description == "sleep 10"


def test_update_status(warm_scheduler):
    #warm_scheduler.update_job_status(0, "RUNNING")
    #assert len(warm_scheduler.jobs) == 2
    pass
