import os
import io
import logging
from shutil import copyfile

import pytest


logging.basicConfig(level=logging.ERROR)


@pytest.fixture(autouse=True, scope="session")
def backup():
    # before
    copyfile("tests/test_data/data.db", "tests/test_data/backup")
    yield
    # after
    os.rename("tests/test_data/backup", "tests/test_data/data.db")
        

def test_append_job(client):
    response = client.post(
        "/jobs",
        json={
            "user": "CocaCola",
            "description": "A drincc",
            "command": "You will not have the drink !",
        }
    )
    data = response.get_json()
    assert response.status_code == 201
    assert data["events"][-1]["status"] == 2
    assert data["description"] == "A drincc"
    assert data["command"] == "You will not have the drink !"
    assert data["identifier"] == 7
    
def test_remove_job(client):
    response = client.delete("/jobs/1000")
    assert response.status_code == 404
    response = client.delete("/jobs/3")
    assert response.status_code == 204

def test_get_jobs(client):
    response = client.get("/jobs")
    assert response.status_code == 200
    assert len(response.get_json()) == 6

def test_add_logfile(client):
    response = client.post("/jobs/1/logs")
    assert response.status_code == 400

def test_get_logfile(client):
    response = client.get("/jobs/1/logs")
    assert response.status_code == 404

    response = client.get("/jobs/1000/logs")
    assert response.status_code == 404
