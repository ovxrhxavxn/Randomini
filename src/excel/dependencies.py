from .services import ExcelService
from .repositories import ExcelRepository


def get_excel_service():
    return ExcelService(ExcelRepository)