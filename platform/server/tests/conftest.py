import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from app.main import app

@pytest.fixture(autouse=True)
def clear_db():
    # Sync clear of test collections before each test execution using admin credentials
    client = MongoClient("mongodb://ascendrite_admin:Alok%40Mongodb%23AscendriteAdmin@127.0.0.1:27017/ascendrite?authSource=admin")
    db = client["ascendrite"]
    db["users"].delete_many({})
    db["user_identities"].delete_many({})
    db["sessions"].delete_many({})
    client.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
