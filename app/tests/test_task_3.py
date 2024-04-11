from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_task3():
    json = {
      "user": {
        "name": "Ivan",
        "age": 23,
        "message": ""
      },
      "meta": {
        "last_modification": "20/05/2023",
        "list_of_skills": [
          "ловкий", "смелый"
        ],
        "mapping": {
          "list_of_ids": [
            1, "два"
          ],
          "tags": [
            "стажировка"
          ]
        }
      }
    }

    res = {
      "user": {
        "name": "Ivan",
        "age": 23,
        "message": "",
        "adult": True
      },
      "meta": {
        "last_modification": "20/05/2023",
        "list_of_skills": [
          "ловкий",
          "смелый"
        ],
        "mapping": {
          "list_of_ids": [
            1,
            "два"
          ],
          "tags": [
            "стажировка"
          ]
        }
      }
    }
    response = client.post("/check_json", json = json)
    assert response.status_code == 200
    assert response.json() == res