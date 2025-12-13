"""Edge case tests for Excel Merger (Phase 5)"""
import os
from src.excel_merger import ExcelMerger
from tests.test_helpers import (
    create_test_excel_file,
    create_empty_file,
    create_file_without_summary,
    create_files_with_different_columns,
    get_temp_directory,
    cleanup_test_files
)


class TestEdgeCases:
    """엣지 케이스 테스트"""

    def setup_method(self) -> None:
        """테스트 셋업"""
        self.test_dir = get_temp_directory()
        self.merger = ExcelMerger()

    def teardown_method(self) -> None:
        """테스트 정리"""
        cleanup_test_files(self.test_dir)

    def test_empty_file_handling(self) -> None:
        """빈 파일 처리 테스트"""
        # 빈 파일 생성
        empty_filepath = os.path.join(self.test_dir, "empty.xlsx")
        create_empty_file(empty_filepath)

        # 정상 파일 1개 생성
        normal_filepath = os.path.join(self.test_dir, "normal.xlsx")
        create_test_excel_file(
            filepath=normal_filepath,
            header=["A", "B"],
            data_row=[1, 2]
        )

        # 병합 실행
        file_paths = [normal_filepath, empty_filepath]
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증 - 정상 파일만 병합되어야 함
        assert header is not None
        assert len(data_rows) == 1, "Only 1 valid file should be merged"

    def test_no_summary_sheet_handling(self) -> None:
        """summary 시트 없는 파일 처리 테스트"""
        # summary 시트 없는 파일 생성
        no_summary_filepath = os.path.join(self.test_dir, "no_summary.xlsx")
        create_file_without_summary(no_summary_filepath)

        # 정상 파일 1개 생성
        normal_filepath = os.path.join(self.test_dir, "normal.xlsx")
        create_test_excel_file(
            filepath=normal_filepath,
            header=["A", "B"],
            data_row=[1, 2]
        )

        # 병합 실행
        file_paths = [normal_filepath, no_summary_filepath]
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증 - 정상 파일만 병합되어야 함
        assert header is not None
        assert len(data_rows) == 1, "Only 1 valid file should be merged"

    def test_different_column_counts(self) -> None:
        """열 개수가 다른 파일들 병합 테스트"""
        # 열 개수가 다른 파일들 생성 (3, 5, 10 columns)
        file_paths = create_files_with_different_columns(self.test_dir)

        # 병합 실행
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증 - 모든 파일이 병합되어야 함
        assert header is not None, f"Header should not be None: {error_msg}"
        assert len(data_rows) == 3, "All 3 files should be merged"

        # 첫 번째 파일의 헤더(3개)를 기준으로 함
        assert len(header) == 3, "Header should have 3 columns"

        # 각 data_row는 자신의 열 개수를 유지
        # (Excel writer가 자동으로 처리)

    def test_korean_filename_handling(self) -> None:
        """한국어 파일명 처리 테스트"""
        # 한국어 파일명으로 파일 생성
        korean_filepath = os.path.join(self.test_dir, "테스트_파일_한글.xlsx")
        create_test_excel_file(
            filepath=korean_filepath,
            header=["이름", "나이", "도시"],
            data_row=["홍길동", 25, "서울"]
        )

        # 또 다른 한국어 파일
        korean_filepath2 = os.path.join(self.test_dir, "병합_테스트.xlsx")
        create_test_excel_file(
            filepath=korean_filepath2,
            header=["이름", "나이", "도시"],
            data_row=["김철수", 30, "부산"]
        )

        # 병합 실행
        file_paths = [korean_filepath, korean_filepath2]
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증 - 한국어 파일명이 정상 처리되어야 함
        assert header is not None, f"Header should not be None: {error_msg}"
        assert len(data_rows) == 2, "Both Korean files should be merged"
        assert header == ["이름", "나이", "도시"], "Korean header should be preserved"

    def test_all_files_invalid(self) -> None:
        """모든 파일이 무효한 경우 테스트"""
        # 모두 summary 시트 없는 파일들
        file_paths = []
        for i in range(3):
            filepath = os.path.join(self.test_dir, f"invalid_{i}.xlsx")
            create_file_without_summary(filepath)
            file_paths.append(filepath)

        # 병합 실행
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증 - 오류 메시지가 있어야 함
        assert header is None, "Header should be None when all files are invalid"
        assert len(data_rows) == 0, "No data rows should be returned"
        assert error_msg != "", "Error message should be returned"

    def test_single_file_merge(self) -> None:
        """파일 1개만 병합하는 경우 테스트"""
        # 파일 1개 생성
        filepath = os.path.join(self.test_dir, "single.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=["A", "B", "C"],
            data_row=[1, 2, 3]
        )

        # 병합 실행
        file_paths = [filepath]
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증 - 1개 파일도 정상 처리되어야 함
        assert header is not None, f"Header should not be None: {error_msg}"
        assert len(data_rows) == 1, "Single file should be merged"
        assert header == ["A", "B", "C"]
        assert data_rows[0] == [1, 2, 3]

    def test_file_with_special_characters_in_data(self) -> None:
        """데이터에 특수문자가 포함된 경우 테스트"""
        filepath = os.path.join(self.test_dir, "special_chars.xlsx")
        create_test_excel_file(
            filepath=filepath,
            header=["Name", "Email", "Note"],
            data_row=["John & Jane", "test@example.com", "Test\\nLine"]
        )

        # 병합 실행
        file_paths = [filepath]
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증 - 특수문자가 보존되어야 함
        assert header is not None
        assert len(data_rows) == 1
        assert data_rows[0][0] == "John & Jane"
        assert data_rows[0][1] == "test@example.com"
