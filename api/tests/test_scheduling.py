import pytest
import os
from shutil import copyfile
import logging
from os.path import isfile
from broker.core.scheduling import Scheduler
from broker.core.models import Job


logging.basicConfig(level=logging.ERROR)

########################################################################################
# Fixtures
########################################################################################

@pytest.fixture
def warm_scheduler():
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
    assert warm_scheduler.n_jobs == 6

def test_warm_empty_init(warm_empty_scheduler):
    assert warm_empty_scheduler.n_jobs == 0

def test_cold_init(cold_scheduler):
    assert cold_scheduler.n_jobs == 0

def test_add_job(warm_scheduler, warm_empty_scheduler, cold_scheduler):
    payload = {
        "user": "RyanTheTemp",
        "command": "ls /tmp",
        "description": "Unix joke"
    }

    warm_scheduler.add_job(Job.from_payload(payload))
    assert warm_scheduler.n_jobs == 7
    warm_empty_scheduler.add_job(Job.from_payload(payload))
    assert warm_empty_scheduler.n_jobs == 1
    cold_scheduler.add_job(Job.from_payload(payload))
    assert cold_scheduler.n_jobs == 1

def test_update_status(warm_scheduler):
    warm_scheduler.update_job_status(1, "DONE")
    assert warm_scheduler.get_job_status(1) == 5 

def test_remove_jobs(warm_scheduler):
     # Index out of range test
    with pytest.raises(IndexError):
        warm_scheduler.remove_job(270)
    assert warm_scheduler.n_jobs == 6

    warm_scheduler.remove_job(5)
    assert warm_scheduler.n_jobs == 5

def test_get_jobs(warm_scheduler):
    assert len(warm_scheduler.get_jobs()) == 6

def test_get_next(warm_scheduler):
    assert warm_scheduler.get_next().user == "jim@mail.com"

