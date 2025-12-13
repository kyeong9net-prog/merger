"""엑셀 병합 로직 통합 (Phase 1)

Single Responsibility: 전체 병합 프로세스를 조율하는 책임만 담당
"""
from typing import Any, List, Optional
from src.excel_reader import ExcelReader
from src.header_validator import HeaderValidator, HeaderValidationError


class ExcelMerger:
    """엑셀 병합 프로세스 조율 클래스"""

    def __init__(self) -> None:
        """ExcelMerger 초기화"""
        self.reader = ExcelReader()
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

        print("\\n=== 파일 병합 시작 ===\\n")

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

                    print(f"[INFO] 헤더 설정 완료: {file_path}")

                except HeaderValidationError as e:
                    error_msg = f"첫 번째 파일의 헤더 검증 실패:\\n{file_path}\\n\\n오류: {e}"
                    print(f"\\n[ERROR] {error_msg}")
                    return (None, [], error_msg)

            # 2행 데이터 추가
            if row2_data is not None:
                data_rows.append(row2_data)

        # 결과 확인
        if header is None:
            error_msg = "모든 파일 처리에 실패했습니다.\\n유효한 summary 시트와 2행 데이터를 가진 파일이 없습니다."  # noqa: E501
            print(f"\\n[ERROR] {error_msg}")
            return (None, [], error_msg)

        if not data_rows:
            error_msg = "병합할 데이터가 없습니다.\\n모든 파일의 2행이 비어있습니다."
            print(f"\\n[ERROR] {error_msg}")
            return (None, [], error_msg)

        print("\\n=== 병합 성공 ===")
        print(f"헤더 파일: {first_success_file}")
        print(f"병합된 파일 수: {len(data_rows)}개\\n")

        return (header, data_rows, "")
