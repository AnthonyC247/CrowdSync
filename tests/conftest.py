import sys
import os
import pytest

# Add the project root and the app directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app.app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client


