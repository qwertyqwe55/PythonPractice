import logging

from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.routes.task_7 import CustomMiddleware

# from app.routes.task_7 import output_log

app = FastAPI()
# output_log.info('Starting...')

my_middleware = CustomMiddleware(some_attribute="some_attribute_here_if_needed")
app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware.dispatch)
from app.routes.task_1 import router as r_1
app.include_router(r_1)

from app.routes.task_2 import router as r_2
app.include_router(r_2)

from app.routes.task_3 import router as r_3
app.include_router(r_3)

from app.routes.task_4 import router as r_4
app.include_router(r_4)

from app.routes.task_5 import router as r_5
app.include_router(r_5)

from app.routes.task_6 import router as r_6
app.include_router(r_6)


