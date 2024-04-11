import datetime
import logging
import os
import re
import sys
import traceback
from contextvars import ContextVar
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# lineno через фильтр


output_log = logging.getLogger("output")
client_host: ContextVar[str | None] = ContextVar("client_host", default=None)

formatter = logging.Formatter(
    fmt="%(levelname)s:     %(message)s"
)

stream_heandler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')

stream_heandler.setFormatter(formatter)
file_handler.setFormatter(formatter)
output_log.handlers = [stream_heandler, file_handler]
output_log.setLevel(logging.INFO)
"""
Задание_7. Логирование в FastAPI с использованием middleware.

Написать конфигурационный файл для логгера "output"
Формат выводимых логов:
[CURRENT_DATETIME] {file: line} LOG_LEVEL - | EXECUTION_TIME_SEC | HTTP_METHOD | URL | STATUS_CODE |

[2023-12-15 00:00:00] {example:62} INFO | 12 | GET | http://localhost/example | 200 |


Дописать класс CustomMiddleware.
Добавить middleware в приложение (app).
"""


class CustomMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            some_attribute: str,
    ):
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        try:

            # Необходимо для считываения количества выполненных запросов
            try:
                with open('number_request.txt', 'r') as f:
                    counter = int(f.read())
            except FileNotFoundError:
                counter = 0
            except ValueError:
                counter = 0

            responce = await call_next(request)

            # В счетчик запросов добавляем только успешные запросы
            if responce.status_code == 200:
                with open('number_request.txt', 'w') as f:
                    f.write(str(counter+1))

            # Получаем уровень логов
            level = str(re.findall(r'\(.*?\)', str(output_log))[0]).replace('(',"").replace(')',"")
            # Получаем текущее время
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Создаем нужный формат логов
            output_log.info(f"{date_time} " + '{' +
                            f"{os.path.realpath(__file__)} : {traceback.extract_stack()[-1].lineno}" + '}' +
                            f" {level} {request.method} {request.url} {responce.status_code}")

            return responce
        except:
            # В случае ошибки при запросе, возвращать код 500
            response = Response("Internal Server Error", status_code=500)
            return response
