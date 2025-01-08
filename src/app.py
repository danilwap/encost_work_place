import asyncio

import uvicorn
from fastapi import FastAPI
from tools import get_all_active_endpoints, add_weight, del_weights, check_state_or_reason_tool
from logging_create import logger

# Добавить ручки:
# 0) Проверка наличия состояния или причины простоя
# 1) Добавление состояния
# 2) Добавление причины простоя
# 3) Добавление указание будущей причины простоя
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
        return res
    else:
        return res


if __name__ == "__main__":
    uvicorn.run(app)

