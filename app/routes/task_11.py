from typing import List

from sqlalchemy.orm import Session, declarative_base
from fastapi import APIRouter
from sqlalchemy import create_engine, Column, Integer, String, Boolean

from app.models import User

router = APIRouter(tags=["API для хранения файлов"])

Base = declarative_base()
engine = create_engine("sqlite:///test.db")
# Base.metadata.drop_all(engine)
class UserTB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    message = Column(String)
    adult = Column(Boolean)


# Create database and table
Base.metadata.create_all(engine)


@router.post("/user_add", description="Добавление строк")
async def user_add(body: List[User]):

    lst = {}

    for us in body:
        user = UserTB(name = us.name, age = us.age, message = us.message, adult = us.adult)
        with Session(engine) as session:
            session.add(user)
            session.commit()
            lst[user.id] = ['Name = ' + us.name + ", Age = " + str(us.age) + ", Message = " + us.message + ", Adult = "
                            + str(us.adult)]
    return lst

@router.get("/get_all_user", description=" Получение всех строк")
async def all_user_get() -> dict:
    lst = {}
    with Session(engine) as session:
        for user in session.query(UserTB).all():
                lst[user.id] = ['Name = ' + user.name + ", Age = " + str(user.age) + ", Message = " + user.message + ", Adult = "
                                + str(user.adult)]
    return lst
@router.get("/get_user/{user_id}", description=" Получение строки по ID")
async def user_get(user_id:int):
    with Session(engine) as session:
        results = session.get(UserTB,user_id)
    return results

@router.post("/change_user/{user_id}", description=" Изменение строки по ID")
async def user_get(body : User, user_id:int)->List[str]:
    with Session(engine) as session:
        user = session.get(UserTB,user_id)
        user.age = body.age
        user.name = body.name
        user.adult = body.adult
        user.message = body.message
        res = ['Name = ' + user.name + ", Age = " + str(user.age) + ", Message = " + user.message + ", Adult = "
         + str(user.adult)]
        session.commit()

    return res

@router.post("/delete_user/{user_id}", description=" Удаление строки по ID")
async def delete_user( user_id:int) -> str:
    with Session(engine) as session:
        flag = session.query(UserTB).filter(UserTB.id == user_id).delete()
        if flag:
            res = f'Пользователь c ID =  {user_id} удален'
        else:
            res = 'Такого пользователя нет'
        print(flag)
        session.commit()
    return res
