"""결과 파일 생성 및 저장 (Phase 1)

Single Responsibility: 병합된 데이터를 엑셀 파일로 저장하는 책임만 담당
"""
import os
from datetime import datetime
from typing import Any, List
from tkinter import filedialog
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet


class FileWriter:
    """결과 파일 생성 및 저장 클래스"""

    def __init__(self) -> None:
        """FileWriter 초기화"""
        pass

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

            print(f"[SUCCESS] 병합 완료: {save_path}")
            print(f"[INFO] 총 {len(data_rows)}개 파일의 데이터가 병합되었습니다.")

        except Exception as e:
            raise Exception(f"파일 생성 실패: {e}")

    def _write_row(self, sheet: Worksheet, row_number: int, data: List[Any]) -> None:
        """워크시트에 행 데이터 쓰기

        Args:
            sheet: Worksheet 객체
            row_number: 쓸 행 번호 (1-based)
            data: 쓸 데이터 리스트
        """
        for col_idx, value in enumerate(data, start=1):
            sheet.cell(row=row_number, column=col_idx, value=value)
