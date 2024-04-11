from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_task2_arabic():
    arabic = 1923
    response = client.post("/converter", json = arabic)
    assert response.status_code == 200
    assert response.json() == {'arabic' : 1923, 'roman' : 'MCMXXIII'}

def test_task2_roman():
    arabic = 'MCMXXIII'
    response = client.post("/converter", json = arabic)
    assert response.status_code == 200
    assert response.json() == {'arabic' : 1923, 'roman' : 'MCMXXIII'}