import asyncpg
import asyncio
from fastapi import Depends
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
import datetime
from sqlalchemy.future import select
from sqlalchemy import text, MetaData, inspect, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base

PG_USER, PG_PASS, PG_DATABASE, PG_HOST, PG_PORT = os.environ['PG_USER'], os.environ['PG_PASS'], os.environ[
    'PG_DATABASE'], \
    os.environ['PG_HOST'], os.environ['PG_PORT']
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


async def test():
    async with get_db() as db:
        result = await db.execute(select(Operators))
        for i in result.scalars().all():
            print(i)

        # res = await db.execute(text("select * from spider.endpoints"))
        # for i in res:
        #    print(i)


asyncio.run(test())
