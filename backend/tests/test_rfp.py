import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from app import models
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    # use a temporary sqlite file
    db_file = tmp_path / 'test.db'
    url = f"sqlite:///{db_file}"
    monkeypatch.setenv('DATABASE_URL', url)
    # re-import and init DB
    init_db()
    yield

def test_create_rfp():
    payload = {'title': 'Test RFP', 'description': 'We need a test system. Budget: 10k INR. - Feature A - Feature B'}
    res = client.post('/api/rfps/', json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data['title'] == 'Test RFP'
    assert 'structured' in data
    assert data['id'] > 0

def test_create_and_list_vendor():
    payload = {'name':'Vendor1','email':'vendor1@example.com'}
    res = client.post('/api/vendors/', json=payload)
    assert res.status_code == 200
    v = res.json()
    assert v['email'] == 'vendor1@example.com'
    list_res = client.get('/api/vendors/')
    assert list_res.status_code == 200
    assert any(x['email']=='vendor1@example.com' for x in list_res.json())
