import pytest

from broker import create_app
from broker.config import TestConfig

@pytest.fixture(scope="session")
def client():
    _app = create_app(TestConfig)
    client = _app.test_client()
    return client
