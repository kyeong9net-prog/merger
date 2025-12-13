"""결과 파일 생성 및 저장 (Phase 1, Phase 2, Phase 4 강화)

Single Responsibility: 병합된 데이터를 엑셀 파일로 저장하는 책임만 담당

Phase 4 품질 요구사항:
- 결과 파일 생성 실패 시 명확한 오류 메시지 제공
"""
import os
from datetime import datetime
from typing import Any, List, Optional
from tkinter import filedialog
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from src.logger import Logger


class FileWriter:
    """결과 파일 생성 및 저장 클래스"""

    def __init__(self, logger: Optional[Logger] = None) -> None:
        """FileWriter 초기화

        Args:
            logger: Logger 인스턴스 (None이면 로깅 안 함)
        """
        self.logger = logger

    def select_save_location(self) -> str:
        """저장 위치 선택 UI

        Returns:
            선택된 디렉토리 경로, 취소 시 빈 문자열
        """
        folder_path = filedialog.askdirectory(
            title="결과 파일 저장 위치 선택"
        )
        return folder_path if folder_path else ""

    def generate_filename(self) -> str:
        """파일명 생성 (merged_summary_yyyyMMdd_HHmm.xlsx)

        Returns:
            생성된 파일명
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"merged_summary_{timestamp}.xlsx"

    def get_unique_filepath(self, directory: str, filename: str) -> str:
        """중복되지 않는 파일 경로 생성

        Args:
            directory: 저장 디렉토리
            filename: 기본 파일명

        Returns:
            중복되지 않는 파일 경로
        """
        base_path = os.path.join(directory, filename)

        # 파일이 존재하지 않으면 그대로 반환
        if not os.path.exists(base_path):
            return base_path

        # 파일명과 확장자 분리
        name_without_ext = os.path.splitext(filename)[0]
        ext = os.path.splitext(filename)[1]

        # 번호를 증가시키면서 중복되지 않는 파일명 찾기
        counter = 1
        while True:
            new_filename = f"{name_without_ext}({counter}){ext}"
            new_path = os.path.join(directory, new_filename)

            if not os.path.exists(new_path):
                return new_path

            counter += 1

    def create_merged_file(
        self,
        save_path: str,
        header: List[Any],
        data_rows: List[List[Any]]
    ) -> None:
        """병합된 데이터로 엑셀 파일 생성

        Args:
            save_path: 저장할 파일 경로
            header: 헤더 데이터 (1행)
            data_rows: 병합할 데이터 행들 (각 파일의 2행들)

        Raises:
            Exception: 파일 생성 실패 시
        """
        try:
            # 새 워크북 생성
            workbook = Workbook()
            sheet = workbook.active

            if sheet is None:
                raise Exception("워크시트 생성 실패")

            # 시트 이름 설정
            sheet.title = "summary"

            # 헤더 추가 (1행)
            self._write_row(sheet, 1, header)

            # 데이터 행들 추가 (2행부터)
            for idx, data_row in enumerate(data_rows, start=2):
                self._write_row(sheet, idx, data_row)

            # 파일 저장
            workbook.save(save_path)
            workbook.close()

            if self.logger:
                self.logger.success(f"병합 완료: {save_path}")
                self.logger.info(f"총 {len(data_rows)}개 파일의 데이터가 병합되었습니다.")

        except PermissionError as e:
            # Phase 4: 명확한 오류 메시지 제공
            raise Exception(
                f"파일 저장 권한 오류\n\n"
                f"원인: 저장 위치에 파일을 쓸 수 없습니다.\n"
                f"상세: {e}\n\n"
                f"해결 방법:\n"
                f"1. 저장 위치의 폴더 권한을 확인하세요.\n"
                f"2. 다른 프로그램에서 동일한 파일을 열고 있다면 닫아주세요.\n"
                f"3. 충분한 디스크 공간이 있는지 확인하세요."
            )
        except Exception as e:
            # Phase 4: 명확한 오류 메시지 제공
            raise Exception(
                f"파일 생성 오류\n\n"
                f"원인: 병합 파일을 생성하는 중 오류가 발생했습니다.\n"
                f"상세: {e}\n\n"
                f"해결 방법:\n"
                f"1. 저장 위치를 다시 확인하세요.\n"
                f"2. 파일명에 특수문자가 없는지 확인하세요.\n"
                f"3. 충분한 디스크 공간이 있는지 확인하세요."
            )

    def _write_row(self, sheet: Worksheet, row_number: int, data: List[Any]) -> None:
        """워크시트에 행 데이터 쓰기

        Args:
            sheet: Worksheet 객체
            row_number: 쓸 행 번호 (1-based)
            data: 쓸 데이터 리스트
        """
        for col_idx, value in enumerate(data, start=1):
            cell = sheet.cell(row=row_number, column=col_idx, value=value)
            # 셀 서식을 "일반"으로 설정 (사용자지정 서식 제거)
            cell.number_format = 'General'
