"""Unit tests for FileSelector (Phase 5)"""
from src.file_selector import FileSelector


class TestFileSelector:
    """파일 선택 기능 테스트"""

    def setup_method(self) -> None:
        """테스트 셋업"""
        self.file_selector = FileSelector()

    def test_validate_file_count_valid_single_file(self) -> None:
        """유효한 파일 개수 테스트 - 1개"""
        file_paths = ["test1.xlsx"]
        assert self.file_selector.validate_file_count(file_paths) is True

    def test_validate_file_count_valid_multiple_files(self) -> None:
        """유효한 파일 개수 테스트 - 여러 개"""
        file_paths = [f"test{i}.xlsx" for i in range(1, 51)]  # 50개
        assert self.file_selector.validate_file_count(file_paths) is True

    def test_validate_file_count_valid_max_files(self) -> None:
        """유효한 파일 개수 테스트 - 최대 100개"""
        file_paths = [f"test{i}.xlsx" for i in range(1, 101)]  # 100개
        assert self.file_selector.validate_file_count(file_paths) is True

    def test_validate_file_count_zero_files(self) -> None:
        """파일 개수 0개 테스트"""
        file_paths: list[str] = []
        # messagebox를 띄우므로 False 반환
        assert self.file_selector.validate_file_count(file_paths) is False

    def test_validate_file_count_exceeded(self) -> None:
        """파일 개수 초과 테스트 - 101개"""
        file_paths = [f"test{i}.xlsx" for i in range(1, 102)]  # 101개
        # messagebox를 띄우므로 False 반환
        assert self.file_selector.validate_file_count(file_paths) is False

    def test_validate_file_extensions_all_valid(self) -> None:
        """파일 확장자 검증 - 모두 유효"""
        file_paths = ["test1.xlsx", "test2.xls", "test3.XLSX"]
        valid_files = self.file_selector.validate_file_extensions(file_paths)
        assert len(valid_files) == 3
        assert all(f in valid_files for f in file_paths)

    def test_validate_file_extensions_mixed(self) -> None:
        """파일 확장자 검증 - 혼합"""
        file_paths = ["test1.xlsx", "test2.txt", "test3.xls", "test4.pdf"]
        valid_files = self.file_selector.validate_file_extensions(file_paths)
        assert len(valid_files) == 2
        assert "test1.xlsx" in valid_files
        assert "test3.xls" in valid_files

    def test_validate_file_extensions_all_invalid(self) -> None:
        """파일 확장자 검증 - 모두 무효"""
        file_paths = ["test1.txt", "test2.pdf", "test3.doc"]
        valid_files = self.file_selector.validate_file_extensions(file_paths)
        assert len(valid_files) == 0

    def test_validate_file_extensions_empty_list(self) -> None:
        """파일 확장자 검증 - 빈 리스트"""
        file_paths: list[str] = []
        valid_files = self.file_selector.validate_file_extensions(file_paths)
        assert len(valid_files) == 0
