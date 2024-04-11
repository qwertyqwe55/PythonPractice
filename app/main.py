from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.db import database, DATABASE_URL
from app.routes.task_7 import CustomMiddleware

app = FastAPI()

# Задание 10 - Три связанные таблицы создаются в файле db.py
# Условие if database != None служит для того, чтобы можно было запускать приложение без Docker
# Без Docker не будет подключения к базе данных и отсюда будет ошибка
# Чтобы ее не было пришлось использовать такой костыль

# Проверить, что три таблицы созданы можно командой ( после запуска docker-compose build)
# docker-compose exec db psql --username=fastapi_traefik --dbname=fastapi_traefik
# После откроется терминал в бд и вести \dt
# fastapi_traefik=# \dt
# чтобы выйти нужно \q



my_middleware = CustomMiddleware(some_attribute="some_attribute_here_if_needed")
app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware.dispatch)

@app.on_event("startup")
async def startup():
    if database != None:
        if not database.is_connected:
            await database.connect()

@app.on_event("shutdown")
async def shutdown():
    if database != None:
        if database.is_connected:
            await database.disconnect()

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

from app.routes.task_8 import router as r_8
app.include_router(r_8)

