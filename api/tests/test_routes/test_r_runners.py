import os
import logging
from shutil import copyfile

import pytest


logging.basicConfig(level=logging.ERROR)


@pytest.fixture(autouse=True, scope="module")
def backup():
    # before
    copyfile("tests/test_data/data.db", "tests/test_data/backup")
    yield
    # after
    os.remove("tests/test_data/data.db")
    os.rename("tests/test_data/backup", "tests/test_data/data.db")


def test_get_next_job(client):
    response = client.get("/runners/available-job")
    assert response.status_code == 200
    assert response.get_json()["identifier"] == 0

    # this is done 2 times to check that if a job's status is not
    # explicitely updated, it remains available
    response = client.get("/runners/available-job")
    assert response.status_code == 200
    assert response.get_json()["identifier"] == 0

def test_update_job_status(client):
    response = client.put(
        "/runners/update-job",
        json={
            "identifier": 7,
            "status": "nothing",
        }   
    )
    assert response.status_code == 400
    response = client.put(
        "/runners/update-job",
        json={
            "identifier": 70,
            "status": "DONE",
        }   
    )
    assert response.status_code == 404
    response = client.put(
        "/runners/update-job",
        json={
            "identifier": 0,
            "status": "DONE",
        }   
    )
    assert response.status_code == 204
    response = client.put(
        "/runners/update-job",
        json={
            "identifier": 7,
            "status": "DONE",
        }   
    )
    assert response.status_code == 204
    response = client.put(
        "/runners/update-job",
        json={
            "identifier": 8,
            "status": "DONE",
        }   
    )
    assert response.status_code == 204   

def test_get_next_job_none(client):
    response = client.get("/runners/available-job")
    assert response.status_code == 204
