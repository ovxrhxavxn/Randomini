import webbrowser
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from .templates import jinja_templates
from .excel.router import router as excel_router
from .config import server_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    webbrowser.open(url=f'http://{server_config.host}:{server_config.port}', new=2)
    yield
    

app = FastAPI(
    title="Randomini",
    lifespan=lifespan
)

app.mount('/static', StaticFiles(directory='src/static'), 'static')

@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return jinja_templates.TemplateResponse('base.html', {'request': request})


routers = [excel_router]

for router in routers:
    app.include_router(router)