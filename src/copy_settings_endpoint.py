import asyncio
import datetime
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from database import async_session, get_data, insert_data
from sqlalchemy import func, create_engine, Table, MetaData, inspect, select, insert, null, delete, join, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import now
from models import EndpointWeights
from dotenv import load_dotenv

load_dotenv()

PG_DATABASE = os.environ.get('PG_DATABASE')
PG_HOST = os.environ.get('PG_HOST')
PG_PASS = os.environ.get('PG_PASS')
PG_PORT = os.environ.get('PG_PORT')
PG_USER = os.environ.get('PG_USER')

"""


1) Endpoint_weights +
2) Endpoint_states +
3) Endpoint_reasons -
4) Endpoint_persons +
5) Endpoint_hierarchies+
6) Endpoint_schedules+
7) Endpoint_flags+
8) Delivery_params+
9) Добавить проверку о наличие записи в каждой таблице
10) Сделать динамическую подгрузку данных 
11) Сделать добавление одним большим запросом, а не многими маленькими
12) В endpoint_schedules добавить подгрузку текущей даты, а не той, которая указана у источника
13) Проверка на то, что id, в который вставляем данные уже имеет записи в определённой таблице
14) Выпуск продукции
"""


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


app = FastAPI(title='Рабочее место Энкост')


async def get_all_endpoints():
    async with get_db() as db:
        try:
            query = select(Endpoint).join(EndpointFlags, Endpoint.id == EndpointFlags.endpoint_id).where(
                EndpointFlags.is_active == True, EndpointFlags.is_visible == True)
            result = await db.execute(query)

            return result.scalars().all()
        except Exception as ex:
            return f"Произошла ошибка {ex}"


async def get_all_hierarchies():
    async with get_db() as db:
        try:
            query = select(EndpointHierarchies).where(EndpointHierarchies.endpoint_id == 4)
            result = await db.execute(query)
            result = result.scalars().all()
            return result
        except Exception as ex:
            return f"Произошла ошибка {ex}"

async def get_all_endpoint_flags():
    async with get_db() as db:
        try:
            query = select(EndpointFlags).where(EndpointFlags.endpoint_id == 4)
            result = await db.execute(query)
            result = result.scalars().all()
            return result
        except Exception as ex:
            return f"Произошла ошибка {ex}"



async def get_all_schedules():
    async with get_db() as db:
        try:
            query = select(EndpointSchedules).where(EndpointSchedules.endpoint_id == 4,
                                                    EndpointSchedules.datetime_to == null())
            result = await db.execute(query)
            result = result.scalars().all()
            return result
        except Exception as ex:
            return f"Произошла ошибка {ex}"


async def add_weight(endpoint_id, weight):
    query = insert(EndpointWeights).values(
        client_id=333,
        endpoint_id=endpoint_id,
        weight=weight,
        weight_2=null(),
        weights=null()
    )
    res = await insert_data(query)
    return res


async def add_endpoint_states(new_endpoint, states):
    # Добавить id точки на которую переносим

    list_answers = []
    for state in states:
        query = insert(EndpointStates).values(
            client_id=state.client_id,
            endpoint_id=new_endpoint,
            state_name=state.state_name,
            class_name=state.class_name,
            menu_button=state.menu_button,
            params=state.params,
            source_states=state.source_states,
            exclude_load=state.exclude_load,
            show_in_total=state.show_in_total,
            is_broken=state.is_broken,
            is_repaired=state.is_repaired,
            is_reduced_performance=state.is_reduced_performance,
            is_blocking=state.is_blocking,
            union_state=state.union_state,
            layer=state.layer,
            is_work=state.is_work,
            state_color=state.state_color,
            state_category=state.state_category,
            button_params=state.button_params,
            is_idle=state.is_idle,
            is_manual=state.is_manual)
        res = await insert_data(query)
        list_answers.append(res)
    return list_answers


async def add_endpoint_reasons(reasons):
    # Добавить id точки на которую переносим

    list_answers = []
    for reason in reasons:
        query = insert(EndpointReasons).values(
            client_id=reason.client_id,
            endpoint_id=24,
            reason_type=reason.reason_type,
            name=reason.name,
            hierarchy=reason.hierarchy,
            category=reason.category,
            actions=reason.actions,
            is_fixed=reason.is_fixed,
            color=reason.color,
            params=reason.params,
            display_order=reason.display_order,
            is_active=reason.is_active,
            is_work=reason.is_work,
            exclude_load=reason.exclude_load)
        res = await insert_data(query)
        list_answers.append(res)
    return list_answers


async def add_endpoint_persons(id_new, persons):
    list_answers = []
    for person in persons:
        query = insert(EndpointPersons).values(
            client_id=person.client_id,
            endpoint_id=id_new,
            person_id=person.person_id,
            role_id=person.role_id,
            added=now(),
            updated=now()
        )
        res = await insert_data(query)
        list_answers.append(res)
    return list_answers


async def add_endpoint_schedules(id_new, schedules):
    list_answers = []
    for schedule in schedules:
        query = insert(EndpointSchedules).values(
            client_id=schedule.client_id,
            endpoint_id=id_new,
            schedule_id=schedule.schedule_id,
            date_from=schedule.date_from,
            date_to=schedule.date_to,
            datetime_from=schedule.datetime_from,
            datetime_to=schedule.datetime_to
        )
        res = await insert_data(query)
        list_answers.append(res)
    return list_answers


async def add_endpoint_hierarchies(id_new, hierarchies):
    list_answers = []
    for hierarch in hierarchies:
        query = insert(EndpointHierarchies).values(
            client_id=hierarch.client_id,
            endpoint_id=id_new,
            hierarchy_id=hierarch.hierarchy_id,
            group=hierarch.group,
            nodes=hierarch.nodes
        )
        res = await insert_data(query)
        list_answers.append(res)
    return list_answers

async def add_endpoint_flags(id_new, flags):
    list_answers = []
    for flag in flags:
        query = insert(EndpointFlags).values(
            client_id=flag.client_id,
            endpoint_id=id_new,
            is_visible=flag.is_visible,
            has_terminal=flag.has_terminal,
            has_repair=flag.has_repair,
            has_production=flag.has_production,
            states_source_id=flag.states_source_id,
            is_active=flag.is_active,
            params=flag.params,
            is_virtual=flag.is_virtual
        )
        res = await insert_data(query)
        list_answers.append(res)
    return list_answers

async def add_delivery_params(id_new):
    list_answers = []

    query = insert(DeliveryParams).values(
        endpoint_id=id_new,
        telegram_chat_id=null(),
        app=True
    )
    res = await insert_data(query)
    list_answers.append(res)
    return list_answers



async def delete_person():
    async with get_db() as db:
        try:
            query = delete(Operators).where(Operators.id == 955)
            await db.execute(query)
            await db.commit()
            return 'Пользователь удалён'
        except Exception as ex:
            return f"Error: {ex}"


async def get_source_endpoint_state():
    query = select(EndpointStates).where(EndpointStates.endpoint_id == 4)
    result = await get_data(query)
    return result.scalars().all()


async def get_source_endpoint_reasons():
    try:
        query = select(EndpointReasons).where(EndpointReasons.endpoint_id == 4)
        print(query)
        result = await get_data(query)
        result = result.scalars().all()
        return result
    except Exception as ex:
        print(ex)


async def get_source_endpoint_persons():
    try:
        query = select(EndpointPersons).where(EndpointPersons.endpoint_id == 4)
        result = await get_data(query)
        result = result.scalars().all()
        return result
    except Exception as ex:
        print(ex)


async def get_max_weight():

    query = select(EndpointWeights).order_by(desc(EndpointWeights.weight))
    result = await get_data(query)
    return result.scalars().all()[0].weight if result else 1


async def main():
    print("Список всех точек:")
    all_endpoints_res = await get_all_endpoints()
    print(*[f"ID: {i.id}\nНазвание: {i.name}\n" for i in all_endpoints_res])
    id_source, id_new = input('С какого id копируем и на какой переносим через пробел: ').split()

    id_source, id_new = int(id_source), int(id_new)

    # ----------------------------------endpoint_weights---------------------------------------
    print('Добавляем веса, следующий после последнего')
    max_weight = await get_max_weight()
    print(f'Максимальный вес: {max_weight}')
    res = await add_weight(id_new, max_weight + 1)
    print(res)
    #Дальше написать создание весов для новых точек

    # ----------------------------------Endpoint_states---------------------------------------
    ###Добавить считывание точки, откуда взято и динамический выбор столбцов, которые подтягивать
    endpoint_states = await get_source_endpoint_state()
    print(f"Собраны такие состояния, добавляем (y/n) {[x.state_name for x in endpoint_states]}")
    step1 = input()

    if step1 == 'y':
       res = await add_endpoint_states(id_new, endpoint_states)
    else:
       assert 'Ручной выход'
    print(f'Результат: {res}')

    # ----------------------------------Endpoint_persons---------------------------------------
    ###Добавить считывание точки, откуда взято и динамический выбор столбцов, которые подтягивать
    endpoint_persons = await get_source_endpoint_persons()
    print(f"Собраны такие id операторов, добавляем (y/n) {[x.person_id for x in endpoint_persons]}")
    step1 = input()

    if step1 == 'y':
       res = await add_endpoint_persons(id_new, endpoint_persons)
    else:
       assert 'Ручной выход'
    print(f'Результат: {res}')

    # ----------------------------------Endpoint_hierarchies---------------------------------------
    ###Добавить считывание точки, откуда взято и динамический выбор столбцов, которые подтягивать
    endpoint_hierarchies = await get_all_hierarchies()
    print(f"У точки такая иерархия, добавляем (y/n) {[x.group for x in endpoint_hierarchies]}")
    step1 = input()

    if step1 == 'y':
       res = await add_endpoint_hierarchies(id_new, endpoint_hierarchies)
    else:
       assert 'Ручной выход'
    print(f'Результат: {res}')

    # ----------------------------------Endpoint_schedules---------------------------------------
    ###Добавить считывание точки, откуда взято и динамический выбор столбцов, которые подтягивать
    endpoint_schedules = await get_all_schedules()
    print(f"У точки такое id расписания, добавляем (y/n) {[x.schedule_id for x in endpoint_schedules]}")
    step1 = input()

    if step1 == 'y':
        res = await add_endpoint_schedules(id_new, endpoint_schedules)
    else:
        assert 'Ручной выход'
    print(f'Результат: {res}')

    # ----------------------------------Endpoint_flags---------------------------------------
    ###Добавить считывание точки, откуда взято и динамический выбор столбцов, которые подтягивать
    endpoint_flags = await get_all_endpoint_flags()
    print(f"У точки такое флаги, добавляем (y/n) {[x for x in endpoint_flags]}")
    step1 = input()

    if step1 == 'y':
        res = await add_endpoint_flags(id_new, endpoint_flags)
    else:
        assert 'Ручной выход'
    print(f'Результат: {res}')





# ----------------------------------delivery_params---------------------------------------
    ###Добавить считывание точки, откуда взято и динамический выбор столбцов, которые подтягивать

    print(f"Делаем, чтобы точка начала писать в app? delivery_params")
    step1 = input()

    if step1 == 'y':
        res = await add_delivery_params(id_new)
    else:
        assert 'Ручной выход'
    print(f'Результат: {res}')

























# ----------------------------------Endpoint_reasons---------------------------------------
###Добавить считывание точки, откуда взято и динамический выбор столбцов, которые подтягивать
# endpoint_reasons = await get_source_endpoint_reasons()
# print(f"Собраны такие причины простоя, добавляем (y/n) {[x.name for x in endpoint_reasons]}")
# step1 = input()
#
# if step1 == 'y':
#    res = await add_endpoint_reasons(endpoint_reasons)
# else:
#    assert 'Ручной выход'
# print(f'Результат: {res}')
# Переделать под sql запрос

#asyncio.run(main())
