from functools import wraps

from fastapi import APIRouter

router = APIRouter(tags=["Стажировка"])

"""
Задание_8. Декоратор - счётчик запросов.

Напишите декоратор который будет считать кол-во запросов сделанных к приложению.
Оберните роут new_request() этим декоратором.
Подумать, как хранить переменную с кол-вом сделаных запросов.
"""

count_requst = 0

def count_requests(func):
    @wraps(func)
    async def wrapper():
        global count_requst
        with open('number_request.txt', 'r') as f:
            count_requst = int(f.read())
        return await func()
    return wrapper



@router.get("/new_request", description="Задание_8. Декоратор - счётчик запросов.")
@count_requests
async def new_request() -> int:
    """Возвращает кол-во сделанных запросов."""
    return count_requst
