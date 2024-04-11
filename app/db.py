from typing import List

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
import os
import databases
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.environ.get('DATABASE_URL')
database = None
if DATABASE_URL != None:
    database = databases.Database(DATABASE_URL)
    metadata = sqlalchemy.MetaData()

Base = declarative_base()

class Customer(Base):

    __tablename__: str = "customers"
    id:int = Column(Integer, primary_key=True, index=True)
    name:str = Column(String)
    age:int = Column(Integer)

    order = relationship("Order", back_populates="customer")
class Order(Base):

    __tablename__: str = "orders"
    id: int = Column(Integer, primary_key=True, index=True)
    customer_id: int = Column(Integer, ForeignKey("customers.id"))
    customer:Mapped[List["Shop"]] = relationship("Customer", back_populates="order")
    shop = relationship("Shop", back_populates="shop_order")
class Shop(Base):

    __tablename__: str = "shops"
    id:int = Column(Integer, primary_key=True, index=True)
    name:str = Column(String)
    customer_id:int = Column(Integer, ForeignKey("orders.id"))
    shop_order = relationship("Order", back_populates="shop")

if DATABASE_URL != None:
    engine = sqlalchemy.create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
