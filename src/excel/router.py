from fastapi import APIRouter, UploadFile, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from .services import ExcelService
from .dependencies import get_excel_service
from ..templates import jinja_templates


router = APIRouter(
    prefix='/excel'
)

@router.post("/upload", response_class=HTMLResponse)
async def upload_excel(
    request: Request, 
    file: UploadFile,
    excel_service: ExcelService = Depends(get_excel_service)
):
    file_bytes = await file.read()
    values = await sync_parse_excel(excel_service, file_bytes)
    names = [list(d.values())[0] for d in values]  # берем только первый столбец
    return jinja_templates.TemplateResponse(
        "roulette.html",
        {"request": request, "names": names}
    )

async def sync_parse_excel(excel_service: ExcelService, file_bytes: bytes):
    # Для совместимости с ProcessPoolExecutor, если нужно
    import asyncio
    loop = asyncio.get_running_loop()
    from functools import partial
    func = partial(excel_service.parse_values, file_bytes)
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:  # ThreadPool ok для I/O
        values = await loop.run_in_executor(executor, func)
    return values