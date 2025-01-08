import os
import pickle
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine, Table, MetaData, inspect
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base


from dotenv import load_dotenv

load_dotenv()  # Загружает в os.environ переменные из .env

PG_DATABASE = os.environ.get('PG_DATABASE')
PG_HOST = os.environ.get('PG_HOST')
PG_PASS = os.environ.get('PG_PASS')
PG_PORT = os.environ.get('PG_PORT')
PG_USER = os.environ.get('PG_USER')

all_endpoints = {}

URL = f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
engine = create_async_engine(URL)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


def save_metadata():
    sync_engine = create_engine(URL.replace('+asyncpg', ''))
    metadata = MetaData()
    inspector = inspect(sync_engine)

    # Получаем список таблиц в указанной схеме
    tables = inspector.get_table_names(schema="parameters")
    print(tables)

    for table_name in tables:
        Table(table_name, metadata, autoload_with=sync_engine, schema='parameters')

        # Сериализуем метаданные и сохраняем их в файл
    with open('metadata.pkl', 'wb') as file:
        pickle.dump(metadata, file)
        print('Файл с данными метадата сохранён')


def load_or_create_metadata():
    try:
        # Попробовать загрузить ранее сохранённые метаданные
        with open('metadata.pkl', 'rb') as file:
            metadata = pickle.load(file)

        print("Метаданные успешно загружены.")
    except FileNotFoundError:
        print("Файл с метаданными не найден. Создаём новые...")
        save_metadata()
        return load_or_create_metadata()  # Рекурсивная попытка загрузки после сохранения

    Base = declarative_base(metadata=metadata)
    return Base, metadata


#----------------------------------- Module CRUD ------------------------------------------

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


async def get_data(query):
    async with get_db() as db:
        try:
            result = await db.execute(query)
            return result
        except Exception as ex:
            return f"Произошла ошибка {ex}"

async def insert_data(query):
    async with get_db() as db:
        try:
            await db.execute(query)
            await db.commit()
            return 'Новая запись добавлена'
        except Exception as ex:
            return f"Произошла ошибка {ex}"

async def delete_data(query):
    async with get_db() as db:
        try:
            await db.execute(query)
            await db.commit()
            return 'Запись удалена'
        except Exception as ex:
            return f"Произошла ошибка {ex}"

Base, metadata = load_or_create_metadata()
