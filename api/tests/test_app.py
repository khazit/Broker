import logging

import pytest
import flask

from app import app


logging.disable(logging.CRITICAL)


@pytest.fixture
def client():
    app.testing = True
    client = app.test_client()
    return client

def test_append_job(client):
    response = client.post(
        "/jobs",
        data={
            "dummy": "empty"
        }
    )
    
    assert response.get_json() is not None
    assert response.status_code == 201 
