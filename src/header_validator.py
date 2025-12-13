"""헤더 검증 로직 (Phase 1, Phase 4 강화)

Single Responsibility: 첫 번째 파일의 헤더(1행) 검증만 담당

Phase 4 품질 요구사항:
- 원본 파일 읽기 전용 처리 (read_only=True)
- 표준화된 오류 메시지 제공
"""
from typing import Any, List
from datetime import datetime, date
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from src.error_messages import (
    header_empty_error,
    header_merged_cells_error,
    header_date_format_error,
    header_formula_error
)


class HeaderValidationError(Exception):
    """헤더 검증 실패 예외"""
    pass


class HeaderValidator:
    """헤더 검증 클래스"""

    def __init__(self) -> None:
        """HeaderValidator 초기화"""
        pass

    def validate_header(self, file_path: str, sheet_name: str) -> None:
        """헤더(1행) 검증

        Args:
            file_path: 검증할 엑셀 파일 경로
            sheet_name: 검증할 시트 이름

        Raises:
            HeaderValidationError: 헤더 검증 실패 시
        """
        try:
            # Phase 4: 병합 셀/수식 검증을 위해 read_only=False 사용
            # (검증 후 저장하지 않으므로 원본 수정 없음)
            workbook = load_workbook(file_path, data_only=False, read_only=False)
        except Exception as e:
            raise HeaderValidationError(f"파일 읽기 실패: {e}")

        # 시트 찾기 (대소문자 구분 없이)
        sheet = None
        for sn in workbook.sheetnames:
            if sn.lower() == sheet_name.lower():
                sheet = workbook[sn]
                break

        if sheet is None:
            workbook.close()
            raise HeaderValidationError(f"{sheet_name} 시트를 찾을 수 없습니다.")

        # 1행 검증
        self._validate_row1_not_empty(sheet)
        self._validate_no_merged_cells(sheet)
        self._validate_no_dates(sheet)
        self._validate_no_formulas(sheet)

        workbook.close()

    def _validate_row1_not_empty(self, sheet: Worksheet) -> None:
        """1행이 비어있지 않은지 검증

        Args:
            sheet: Worksheet 객체

        Raises:
            HeaderValidationError: 1행이 비어있을 때
        """
        row1 = list(sheet[1])
        values = [cell.value for cell in row1]

        # 뒤에서부터 None 제거
        while values and values[-1] is None:
            values.pop()

        # 모든 값이 None이거나 빈 문자열인지 확인
        if not values:
            raise HeaderValidationError(header_empty_error())

        for value in values:
            if value is not None and str(value).strip() != "":
                return  # 하나라도 값이 있으면 통과

        raise HeaderValidationError(header_empty_error())

    def _validate_no_merged_cells(self, sheet: Worksheet) -> None:
        """1행에 병합 셀이 없는지 검증

        Args:
            sheet: Worksheet 객체

        Raises:
            HeaderValidationError: 1행에 병합 셀이 있을 때
        """
        for merged_range in sheet.merged_cells.ranges:
            # 병합 셀의 최소/최대 행 확인
            if merged_range.min_row <= 1 <= merged_range.max_row:
                raise HeaderValidationError(header_merged_cells_error())

    def _validate_no_dates(self, sheet: Worksheet) -> None:
        """1행에 날짜 형식이 없는지 검증

        Args:
            sheet: Worksheet 객체

        Raises:
            HeaderValidationError: 1행에 날짜 형식이 있을 때
        """
        row1 = list(sheet[1])

        for cell in row1:
            if cell.value is None:
                continue

            # datetime 또는 date 타입 체크
            if isinstance(cell.value, (datetime, date)):
                raise HeaderValidationError(header_date_format_error())

    def _validate_no_formulas(self, sheet: Worksheet) -> None:
        """1행에 수식이 없는지 검증

        Args:
            sheet: Worksheet 객체

        Raises:
            HeaderValidationError: 1행에 수식이 있을 때
        """
        # data_only=False로 로드했을 때만 수식 확인 가능
        row1 = list(sheet[1])

        for cell in row1:
            if cell.value is None:
                continue

            # 수식이 있는지 확인 (data_type이 'f'이거나 value가 '='로 시작)
            if hasattr(cell, 'data_type') and cell.data_type == 'f':
                raise HeaderValidationError(header_formula_error())

            # 추가 안전장치: value가 문자열이고 '='로 시작하는 경우
            if isinstance(cell.value, str) and cell.value.startswith('='):
                raise HeaderValidationError(header_formula_error())

    def validate_header_data(self, header_data: List[Any]) -> None:
        """헤더 데이터 검증 (간단한 검증)

        Args:
            header_data: 헤더 데이터 리스트

        Raises:
            HeaderValidationError: 헤더가 비어있을 때
        """
        if not header_data:
            raise HeaderValidationError("헤더 데이터가 비어있습니다.")

        # 모든 값이 None이거나 빈 문자열인지 확인
        for value in header_data:
            if value is not None and str(value).strip() != "":
                return  # 하나라도 값이 있으면 통과

        raise HeaderValidationError("헤더 데이터가 비어있습니다.")
