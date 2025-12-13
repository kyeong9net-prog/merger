"""Unit tests for HeaderValidator (Phase 5)"""
import os
import pytest
from src.header_validator import HeaderValidator, HeaderValidationError
from tests.test_helpers import (
    create_test_excel_file,
    get_temp_directory,
    cleanup_test_files
)


class TestHeaderValidator:
    """헤더 검증 로직 테스트"""

    def setup_method(self) -> None:
        """테스트 셋업"""
        self.validator = HeaderValidator()
        self.test_dir = get_temp_directory()

    def teardown_method(self) -> None:
        """테스트 정리"""
        cleanup_test_files(self.test_dir)

    def test_header_valid_passes(self) -> None:
        """정상 헤더 검증 통과"""
        filepath = os.path.join(self.test_dir, "valid.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=["Name", "Age", "City"],
            data_row=["John", 25, "Seoul"]
        )

        # 예외가 발생하지 않아야 함
        self.validator.validate_header(filepath, "summary")

    def test_header_empty_raises_error(self) -> None:
        """헤더 비어있음 - 오류 발생"""
        filepath = os.path.join(self.test_dir, "empty_header.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=[None, None, None],
            data_row=[1, 2, 3]
        )

        with pytest.raises(HeaderValidationError):
            self.validator.validate_header(filepath, "summary")

    def test_header_merged_cells_raises_error(self) -> None:
        """헤더 병합 셀 - 오류 발생"""
        filepath = os.path.join(self.test_dir, "merged.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=["Name", "Age", "City"],
            data_row=[1, 2, 3],
            has_merged_cells=True
        )

        with pytest.raises(HeaderValidationError):
            self.validator.validate_header(filepath, "summary")

    def test_header_date_format_raises_error(self) -> None:
        """헤더 날짜 형식 - 오류 발생"""
        filepath = os.path.join(self.test_dir, "date_header.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=["Name", "Age", "City"],
            data_row=[1, 2, 3],
            has_date=True
        )

        with pytest.raises(HeaderValidationError):
            self.validator.validate_header(filepath, "summary")

    def test_header_formula_raises_error(self) -> None:
        """헤더 수식 - 오류 발생"""
        filepath = os.path.join(self.test_dir, "formula_header.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=["Name", "Age", "City"],
            data_row=[1, 2, 3],
            has_formula=True
        )

        with pytest.raises(HeaderValidationError):
            self.validator.validate_header(filepath, "summary")

    def test_validate_header_data_valid(self) -> None:
        """헤더 데이터 검증 - 유효"""
        header_data = ["Name", "Age", "City"]
        # 예외가 발생하지 않아야 함
        self.validator.validate_header_data(header_data)

    def test_validate_header_data_empty_raises_error(self) -> None:
        """헤더 데이터 검증 - 비어있음"""
        header_data: list[str] = []
        with pytest.raises(HeaderValidationError):
            self.validator.validate_header_data(header_data)

    def test_validate_header_data_all_none_raises_error(self) -> None:
        """헤더 데이터 검증 - 모두 None"""
        header_data = [None, None, None]
        with pytest.raises(HeaderValidationError):
            self.validator.validate_header_data(header_data)
