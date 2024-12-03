from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from copy_settings_endpoint import get_max_weight

router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get('/')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})

@router.get('/copy_settings_endpoint/')
def get_base_page(request: Request):
    return templates.TemplateResponse('copy_settings_endpoint.html', {'request': request})

@router.get('/load_weight')
async def load_data():
    max_weight = await get_max_weight()

    return {"items": [max_weight]}

