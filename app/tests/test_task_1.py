from typing import Mapping

from fastapi import requests
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_task1():
    # t = {'words':
    #          ['Мама', 'МАМА', 'Мама', 'папа', 'ПАПА', 'Мама', 'ДЯдя', 'брАт', 'Дядя', 'Дядя', 'Дядя']}
    words = ["Мама", "МАМА", "Мама", "папа", "ПАПА", "Мама", "ДЯдя", "брАт", "Дядя", "Дядя", "Дядя"]
    # response = client.post("/find_in_different_registers", content = words)
    response = client.post("/find_in_different_registers", json = words)
    assert response.status_code == 200
    assert response.json() == ['папа', 'брат'] or response.json() == ['брат', 'папа']
