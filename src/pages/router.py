from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get('/')
def get_base_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})

@router.get('/copy_settings_endpoint/')
def get_base_page(request: Request):
    return templates.TemplateResponse('copy_settings_endpoint.html', {'request': request})