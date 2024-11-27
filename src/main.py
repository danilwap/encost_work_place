import datetime
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from sqlalchemy import create_engine, Table, MetaData, inspect, select, insert, null, delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql.functions import now

PG_DATABASE = 'encost_333'
PG_HOST = 'cluster-homer.encosts.com'
PG_PASS = 'mhvid1999R'
PG_PORT = 5432
PG_USER = 'bds'

URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

sync_engine = create_engine(URL.replace('+asyncpg', ''))
engine = create_async_engine(URL)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

metadata = MetaData()
inspector = inspect(sync_engine)

# Получаем список таблиц в указанной схеме
tables = inspector.get_table_names(schema="parameters")
print(tables)
table_info = {}

# Проходимся по всем таблицам и загружаем их
for table_name in tables:
    Table(table_name, metadata, autoload_with=sync_engine, schema="parameters")

Base = declarative_base(metadata=metadata)


class Operators(Base):
    __table__ = metadata.tables["parameters.client_persons"]


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


app = FastAPI(title='Рабочее место Энкост')


@app.get('/client_operators')
async def read_operators():
    async with get_db() as db:
        result = await db.execute(select(Operators))

        return result.scalars().all()


@app.get('/add_operator')
async def add_operator():
    async with get_db() as db:
        try:
            query = insert(Operators).values(
                comment=null(),
                client_id=333,
                added=now(),
                is_active=True,
                person_name="test",
                updated=now())
            await db.execute(query)
            await db.commit()
            return 'Новая запись добавлена'
        except Exception as ex:
            return f"Ошибка {ex}"


@app.get('/delete_person')
async def delete_person():
    async with get_db() as db:
        try:
            query = delete(Operators).where(Operators.id == 955)
            await db.execute(query)
            await db.commit()
            return 'Пользователь удалён'
        except Exception as ex:
            return f"Error: {ex}"



@app.get('')
async def main_routes():
    return 'Работу работаем)'



