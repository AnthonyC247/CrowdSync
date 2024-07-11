

import pytest
from datetime import datetime
from app import app as flask_app

@pytest.fixture
def client():
    with flask_app.test_client() as client:
        yield client

def test_valid_zip_code(client):
    # Test valid 5-digit zip code
    rv = client.post('/home', data=dict(zip_city='12345', start_date='01/01/2023', end_date='01/02/2023', query='concert'))
    assert b'No events found.' not in rv.data

def test_invalid_zip_code(client):
    # Test invalid zip code (e.g., non-digit characters)
    rv = client.post('/home', data=dict(zip_city='abcde', start_date='01/01/2023', end_date='01/02/2023', query='concert'))
    assert b'Error: Zipcode must be 5 digits' in rv.data

def test_date_format(client):
    # Test invalid date format
    rv = client.post('/home', data=dict(zip_city='12345', start_date='01-01-2023', end_date='01-02-2023', query='concert'))
    assert b'Please enter the date in the correct format' in rv.data

def test_date_logic(client):
    # Test end date before start date
    rv = client.post('/home', data=dict(zip_city='12345', start_date='01/02/2023', end_date='01/01/2023', query='concert'))
    assert b'Error: start date must be before end date' in rv.data

def test_query_input(client):
    # Test search with valid query
    rv = client.post('/home', data=dict(zip_city='12345', start_date='01/01/2023', end_date='01/02/2023', query='concert'))
    assert b'No events found.' not in rv.data
