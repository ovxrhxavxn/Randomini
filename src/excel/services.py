from typing import TypeAlias

from .repositories import AbstractExcelRepository


class ExcelService:

    def __init__(self, excel_repo: type[AbstractExcelRepository]):
        self._excel_repo = excel_repo()

    def parse_values(self, file_bytes: bytes):
        data = self._excel_repo.get_values(file_bytes)
        return data