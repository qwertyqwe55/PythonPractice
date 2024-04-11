from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_task4():
    file = {'file': open('app/files/employees.csv', 'rb')}
    response = client.post("/get_average_age_by_position", files=file)
    assert response.status_code == 200
    assert response.json() == {
      "Менеджер": 32.5,
      "Разработчик": 26.5
    }