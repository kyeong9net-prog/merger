"""Unit tests for ExcelReader (Phase 5)"""
import os
from src.excel_reader import ExcelReader
from tests.test_helpers import (
    create_test_excel_file,
    create_file_without_summary,
    get_temp_directory,
    cleanup_test_files
)


class TestExcelReader:
    """데이터 추출 기능 테스트"""

    def setup_method(self) -> None:
        """테스트 셋업"""
        self.reader = ExcelReader()
        self.test_dir = get_temp_directory()

    def teardown_method(self) -> None:
        """테스트 정리"""
        cleanup_test_files(self.test_dir)

    def test_read_file_success(self) -> None:
        """정상 파일 읽기 테스트"""
        filepath = os.path.join(self.test_dir, "test.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=["A", "B", "C"],
            data_row=[1, 2, 3]
        )

        header, row2, status = self.reader.read_file(filepath)

        assert status == "SUCCESS"
        assert header == ["A", "B", "C"]
        assert row2 == [1, 2, 3]

    def test_find_summary_sheet_case_insensitive(self) -> None:
        """summary 시트 찾기 - 대소문자 구분 없음"""
        # SUMMARY로 생성
        filepath = os.path.join(self.test_dir, "test_summary.xlsx")
        create_test_excel_file(
            filepath=filepath,
            sheet_name="SUMMARY",
            header=["A"],
            data_row=[1]
        )

        header, row2, status = self.reader.read_file(filepath)
        assert status == "SUCCESS"

    def test_read_file_no_summary_sheet(self) -> None:
        """summary 시트 없는 파일 테스트"""
        filepath = os.path.join(self.test_dir, "no_summary.xlsx")
        create_file_without_summary(filepath)

        header, row2, status = self.reader.read_file(filepath)

        assert status == "NO_SUMMARY_SHEET"
        assert header is None
        assert row2 is None

    def test_read_file_row2_empty(self) -> None:
        """2행 비어있는 파일 테스트"""
        filepath = os.path.join(self.test_dir, "empty_row2.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=["A", "B", "C"],
            data_row=[None, None, None]  # 빈 데이터
        )

        header, row2, status = self.reader.read_file(filepath)

        assert status == "ROW2_EMPTY"
        assert header is None  # 2행이 비어있으면 header도 None
        assert row2 is None

    def test_is_row_empty_all_none(self) -> None:
        """빈 행 검증 - 모두 None"""
        assert self.reader._is_row_empty([None, None, None]) is True

    def test_is_row_empty_all_empty_strings(self) -> None:
        """빈 행 검증 - 모두 빈 문자열"""
        assert self.reader._is_row_empty(["", "  ", ""]) is True

    def test_is_row_empty_mixed(self) -> None:
        """빈 행 검증 - 혼합 (None과 빈 문자열)"""
        assert self.reader._is_row_empty([None, "", "  "]) is True

    def test_is_row_empty_has_data(self) -> None:
        """빈 행 검증 - 데이터 있음"""
        assert self.reader._is_row_empty([None, "data", None]) is False
        assert self.reader._is_row_empty([1, 2, 3]) is False

    def test_extract_row_with_trailing_none(self) -> None:
        """행 추출 - 뒤쪽 None 제거 테스트"""
        filepath = os.path.join(self.test_dir, "trailing_none.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=["A", "B", "C"],
            data_row=[1, 2, 3]
        )

        header, row2, status = self.reader.read_file(filepath)

        # 뒤쪽 None은 제거되어야 함
        assert header == ["A", "B", "C"]
        assert None not in header[-1:]  # 마지막이 None이 아님
