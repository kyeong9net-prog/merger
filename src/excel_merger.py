"""엑셀 병합 로직 통합 (Phase 1, Phase 2, Phase 4 강화)

Single Responsibility: 전체 병합 프로세스를 조율하는 책임만 담당

Phase 4 품질 요구사항:
- 표준화된 오류 메시지 제공
"""
import os
from typing import Any, List, Optional
from src.excel_reader import ExcelReader
from src.header_validator import HeaderValidator, HeaderValidationError
from src.logger import Logger
from src.error_messages import no_valid_files_error, no_data_rows_error


class ExcelMerger:
    """엑셀 병합 프로세스 조율 클래스"""

    def __init__(self, logger: Optional[Logger] = None) -> None:
        """ExcelMerger 초기화

        Args:
            logger: Logger 인스턴스 (None이면 로깅 안 함)
        """
        self.logger = logger
        self.reader = ExcelReader(logger)
        self.validator = HeaderValidator()

    def merge_files(self, file_paths: List[str]) -> tuple[Optional[List[Any]], List[List[Any]], str]:  # noqa: E501
        """여러 엑셀 파일 병합

        Args:
            file_paths: 병합할 파일 경로 리스트

        Returns:
            (헤더, 데이터 행들, 오류 메시지) 튜플
            - 성공: (header, data_rows, "")
            - 실패: (None, [], "error message")
        """
        header: Optional[List[Any]] = None
        data_rows: List[List[Any]] = []
        first_success_file: Optional[str] = None

        if self.logger:
            self.logger.info("=== 파일 병합 시작 ===")

        for file_path in file_paths:
            # 파일 읽기
            file_header, row2_data, status = self.reader.read_file(file_path)

            # 실패한 파일은 스킵
            if status != "SUCCESS":
                continue

            # 첫 번째 성공 파일인 경우: 헤더 검증 및 저장
            if header is None:
                try:
                    # 헤더 검증
                    self.validator.validate_header(file_path, "summary")
                    self.validator.validate_header_data(file_header)  # type: ignore

                    # 헤더 저장
                    header = file_header
                    first_success_file = file_path

                    if self.logger:
                        file_name = os.path.basename(file_path)
                        self.logger.info("헤더 설정 완료", file_name)

                except HeaderValidationError as e:
                    error_msg = f"첫 번째 파일의 헤더 검증 실패:\\n{file_path}\\n\\n오류: {e}"
                    if self.logger:
                        self.logger.error(error_msg)
                    return (None, [], error_msg)

            # 2행 데이터 추가
            if row2_data is not None:
                data_rows.append(row2_data)

        # 결과 확인
        if header is None:
            error_msg = no_valid_files_error()
            if self.logger:
                self.logger.error(error_msg)
            return (None, [], error_msg)

        if not data_rows:
            error_msg = no_data_rows_error()
            if self.logger:
                self.logger.error(error_msg)
            return (None, [], error_msg)

        if self.logger:
            self.logger.info("=== 병합 성공 ===")
            self.logger.info(f"헤더 파일: {first_success_file}")
            self.logger.info(f"병합된 파일 수: {len(data_rows)}개")

        return (header, data_rows, "")
