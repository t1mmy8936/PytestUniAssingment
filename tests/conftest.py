# tests/conftest.py
import os
import pytest
from importlib import reload

# Ensure we run in a predictable environment for tests
os.environ.setdefault("APP_ENV", "staging")
os.environ.setdefault("SECRET_KEY", "test_secret_key")
os.environ.setdefault("DISABLE_EMAILS", "true")

@pytest.fixture(scope="session")
def app():
    # Import here so env vars above are visible to the app on import
    import app as flask_app
    # If the user later adopts config.py in app.py, this will still work.
    return flask_app.app

@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client
