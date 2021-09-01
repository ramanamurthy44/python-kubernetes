from fastapi.testclient import TestClient
from companiesRegistry import app

client = TestClient(app)

def test_registerCompany():

    response = client.post("/home/register", json={"company": "Telstra"})

    assert response.status_code == 200

    assert response.json() == 'Succesfully added'

def test_getCompany():

    response = client.get("/home/verify/Apple")

    assert response.status_code == 200

    assert response.json() == {'valid': True}

def test_getCompany():

    response = client.get("/home/verify/abcd")

    assert response.status_code == 400

    assert response.json() == {'detail': {'valid': False}}