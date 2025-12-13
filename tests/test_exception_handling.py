"""Unit tests for exception handling (Phase 5)"""
import os
import pytest
from src.excel_reader import ExcelReader
from src.file_writer import FileWriter
from tests.test_helpers import (
    get_temp_directory,
    cleanup_test_files
)


class TestExceptionHandling:
    """예외 처리 테스트"""

    def setup_method(self) -> None:
        """테스트 셋업"""
        self.test_dir = get_temp_directory()

    def teardown_method(self) -> None:
        """테스트 정리"""
        cleanup_test_files(self.test_dir)

    def test_file_not_found_handling(self) -> None:
        """파일 없음 오류 처리"""
        reader = ExcelReader()
        filepath = os.path.join(self.test_dir, "nonexistent.xlsx")

        header, row2, status = reader.read_file(filepath)

        assert status == "FILE_ERROR"
        assert header is None
        assert row2 is None

    def test_invalid_file_format_handling(self) -> None:
        """잘못된 파일 형식 처리"""
        reader = ExcelReader()

        # 텍스트 파일을 엑셀로 읽으려고 시도
        filepath = os.path.join(self.test_dir, "invalid.xlsx")
        with open(filepath, 'w') as f:
            f.write("This is not an Excel file")

        header, row2, status = reader.read_file(filepath)

        assert status == "FILE_ERROR"
        assert header is None
        assert row2 is None

    def test_file_writer_invalid_path(self) -> None:
        """파일 저장 경로 오류 처리"""
        writer = FileWriter()

        # 존재하지 않는 경로
        invalid_path = "/nonexistent/path/file.xlsx"
        header = ["A", "B"]
        data_rows = [[1, 2]]

        with pytest.raises(Exception) as exc_info:
            writer.create_merged_file(invalid_path, header, data_rows)

        # 오류 메시지가 포함되어야 함
        assert "오류" in str(exc_info.value)

    def test_file_writer_empty_data(self) -> None:
        """빈 데이터로 파일 생성 시도"""
        writer = FileWriter()

        filepath = os.path.join(self.test_dir, "empty.xlsx")
        header = ["A", "B"]
        data_rows: list[list[int]] = []  # 빈 데이터

        # 빈 데이터라도 파일 생성은 성공해야 함 (헤더만 있음)
        writer.create_merged_file(filepath, header, data_rows)

        assert os.path.exists(filepath)

    def test_excel_reader_handles_corrupted_workbook(self) -> None:
        """손상된 워크북 처리"""
        reader = ExcelReader()

        # 빈 파일을 .xlsx로 저장
        filepath = os.path.join(self.test_dir, "corrupted.xlsx")
        with open(filepath, 'wb') as f:
            f.write(b'corrupted data')

        header, row2, status = reader.read_file(filepath)

        assert status == "FILE_ERROR"
        assert header is None
        assert row2 is None
