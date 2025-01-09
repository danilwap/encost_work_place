import asyncio

import uvicorn
from fastapi import FastAPI
from tools import get_all_active_endpoints, add_weight, del_weights, get_last_id_app, check_state_or_reason_tool, add_endpoint_states
from logging_create import logger

# Добавить ручки:
# ! Создать 10 активных ручек
# 4) Добавление функции отправки сообщения о проблеме
# 5) Добавление функции указания комментария к причине простоя
# 6) Добавление создания тестовой точки
# 7) Создания расписания




app = FastAPI()

@app.get("/add_weights")
async def add_weights():
    all_endpoint_id = await get_all_active_endpoints()

    status_del = await del_weights()
    logger.info("Старые веса удалены")

    if status_del == 200:
        for weight, endpoint_id in enumerate(all_endpoint_id):
            await add_weight(endpoint_id, weight + 1)
        logger.info("Новые веса добавлены")
    else:
        return status_del


@app.get("/check_state_or_reason")
async def check_state_or_reason(name: str):
    res = await check_state_or_reason_tool(name)
    if res == "Всё ок":
        await add_endpoint_states(name)
        return 'Новое состояние добавлено!'
    else:
        return res

@app.get("/add_next_idle_reason")
async def add_next_idle_reason():
    # Нет доступа
    return "Нет доступа"



if __name__ == "__main__":
    uvicorn.run(app)

