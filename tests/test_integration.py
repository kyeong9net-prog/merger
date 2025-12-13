"""Integration tests for Excel Merger (Phase 5)"""
import os
import time
from src.excel_merger import ExcelMerger
from src.file_writer import FileWriter
from tests.test_helpers import (
    create_multiple_test_files,
    get_temp_directory,
    cleanup_test_files
)


class TestIntegration:
    """통합 테스트 - 파일 개수별 병합 및 성능 테스트"""

    def setup_method(self) -> None:
        """테스트 셋업"""
        self.test_dir = get_temp_directory()
        self.merger = ExcelMerger()
        self.writer = FileWriter()

    def teardown_method(self) -> None:
        """테스트 정리"""
        cleanup_test_files(self.test_dir)

    def test_merge_20_files(self) -> None:
        """파일 20개 병합 테스트"""
        # 20개 파일 생성
        file_paths = create_multiple_test_files(
            count=20,
            directory=self.test_dir,
            prefix="file_20"
        )

        # 병합 실행
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증
        assert header is not None, f"Header should not be None: {error_msg}"
        assert len(data_rows) == 20, "Should have 20 data rows"
        assert error_msg == "", f"No error expected: {error_msg}"

        # 결과 파일 생성 테스트
        output_path = os.path.join(self.test_dir, "merged_20.xlsx")
        self.writer.create_merged_file(output_path, header, data_rows)
        assert os.path.exists(output_path)

    def test_merge_50_files(self) -> None:
        """파일 50개 병합 테스트"""
        # 50개 파일 생성
        file_paths = create_multiple_test_files(
            count=50,
            directory=self.test_dir,
            prefix="file_50"
        )

        # 병합 실행
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증
        assert header is not None, f"Header should not be None: {error_msg}"
        assert len(data_rows) == 50, "Should have 50 data rows"
        assert error_msg == "", f"No error expected: {error_msg}"

        # 결과 파일 생성 테스트
        output_path = os.path.join(self.test_dir, "merged_50.xlsx")
        self.writer.create_merged_file(output_path, header, data_rows)
        assert os.path.exists(output_path)

    def test_merge_100_files(self) -> None:
        """파일 100개 병합 테스트"""
        # 100개 파일 생성
        file_paths = create_multiple_test_files(
            count=100,
            directory=self.test_dir,
            prefix="file_100"
        )

        # 병합 실행
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증
        assert header is not None, f"Header should not be None: {error_msg}"
        assert len(data_rows) == 100, "Should have 100 data rows"
        assert error_msg == "", f"No error expected: {error_msg}"

        # 결과 파일 생성 테스트
        output_path = os.path.join(self.test_dir, "merged_100.xlsx")
        self.writer.create_merged_file(output_path, header, data_rows)
        assert os.path.exists(output_path)

    def test_performance_100_files_under_5_seconds(self) -> None:
        """성능 테스트 - 100개 파일 5초 이내 처리"""
        # 100개 파일 생성
        file_paths = create_multiple_test_files(
            count=100,
            directory=self.test_dir,
            prefix="perf_test"
        )

        # 시작 시간 측정
        start_time = time.time()

        # 병합 실행
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증 - header가 None이 아닌지 확인
        assert header is not None, f"Header should not be None: {error_msg}"

        # 결과 파일 생성
        output_path = os.path.join(self.test_dir, "perf_merged.xlsx")
        self.writer.create_merged_file(output_path, header, data_rows)

        # 종료 시간 측정
        end_time = time.time()
        elapsed_time = end_time - start_time

        # 검증
        assert header is not None, f"Header should not be None: {error_msg}"
        assert len(data_rows) == 100, "Should have 100 data rows"
        assert os.path.exists(output_path), "Output file should exist"

        # 성능 검증 - 5초 이내
        assert elapsed_time < 5.0, \
            f"Processing should complete within 5 seconds, " \
            f"but took {elapsed_time:.2f} seconds"

        print(f"\n성능 테스트 결과: {elapsed_time:.2f}초 (100개 파일)")

    def test_merge_mixed_valid_invalid_files(self) -> None:
        """정상 파일과 비정상 파일 혼합 병합 테스트"""
        from tests.test_helpers import (
            create_test_excel_file,
            create_file_without_summary
        )

        # 정상 파일 3개
        file_paths = create_multiple_test_files(
            count=3,
            directory=self.test_dir,
            prefix="valid"
        )

        # summary 시트 없는 파일 추가
        invalid_path = os.path.join(self.test_dir, "invalid.xlsx")
        create_file_without_summary(invalid_path)
        file_paths.append(invalid_path)

        # 빈 데이터 파일 추가
        empty_data_path = os.path.join(self.test_dir, "empty_data.xlsx")
        create_test_excel_file(
            filepath=empty_data_path,
            header=["A", "B"],
            data_row=[None, None]  # 빈 데이터
        )
        file_paths.append(empty_data_path)

        # 병합 실행
        header, data_rows, error_msg = self.merger.merge_files(file_paths)

        # 검증 - 정상 파일 3개만 병합되어야 함
        assert header is not None
        assert len(data_rows) == 3, "Only 3 valid files should be merged"
