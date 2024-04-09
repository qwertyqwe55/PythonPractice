import datetime
import logging
import os
import re
import sys
import traceback
from contextvars import ContextVar
import time

from fastapi import Request
from starlette.background import BackgroundTask
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
        """Load request ID from headers if present. Generate one otherwise."""

        responce = await call_next(request)
        level = str(re.findall(r'\(.*?\)', str(output_log))[0]).replace('(',"").replace(')',"")
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output_log.info(f"{date_time} " + '{' +
                        f"{os.path.realpath(__file__)} : {traceback.extract_stack()[-1].lineno}" + '}' +
                        f" {level} {request.method} {request.url} {responce.status_code}")

        return responce


        # В случае ошибки при запросе, возвращать код 500
        # response = Response("Internal Server Error", status_code=500)
