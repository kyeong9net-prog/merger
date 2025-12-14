"""엑셀 파일 병합 도구 - 메인 프로그램 (Phase 1, Phase 2 강화)

Entry Point: 사용자와의 인터페이스 및 전체 플로우 관리
"""
import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from typing import List, Optional
from src.file_selector import FileSelector
from src.excel_merger import ExcelMerger
from src.file_writer import FileWriter
from src.logger import Logger


class ExcelMergerApp:
    """엑셀 병합 도구 메인 애플리케이션"""

    def __init__(self) -> None:
        """애플리케이션 초기화"""
        # Logger 생성
        self.logger: Optional[Logger] = None

        # 클래스 초기화 (Logger는 run()에서 생성 후 전달)
        self.file_selector: FileSelector
        self.merger: ExcelMerger
        self.file_writer: FileWriter

        # Tkinter root 생성 (UI 백엔드)
        self.root = tk.Tk()
        self.root.withdraw()  # 메인 윈도우 숨기기

    def run(self) -> None:
        """애플리케이션 실행"""
        # 만료 날짜 체크
        expiry_date = datetime(2026, 11, 30, 23, 59, 59)
        if datetime.now() > expiry_date:
            messagebox.showerror(
                "프로그램 만료",
                "이 프로그램은 2026년 11월 30일에 만료되었습니다.\n\n"
                "최신 버전을 다운로드하시거나 개발자에게 문의하세요."
            )
            sys.exit(0)

        # Logger 생성 및 초기화
        save_location = self._get_initial_save_location()
        if not save_location:
            print("[INFO] 저장 위치가 선택되지 않았습니다. 프로그램을 종료합니다.")
            return

        log_filename = Logger.generate_log_filename()
        log_path = os.path.join(save_location, log_filename)
        self.logger = Logger(log_path)

        # 클래스 초기화 (Logger 전달)
        self.file_selector = FileSelector(self.logger)
        self.merger = ExcelMerger(self.logger)
        self.file_writer = FileWriter(self.logger)

        self.logger.info("=" * 60)
        self.logger.info("엑셀 파일 병합 도구 (Phase 2)")
        self.logger.info("=" * 60)

        # Step 1: 파일 선택 방법 선택
        file_paths = self._select_files()

        if not file_paths:
            self.logger.info("파일이 선택되지 않았습니다. 프로그램을 종료합니다.")
            return

        # Step 2: 파일 개수 검증
        if not self.file_selector.validate_file_count(file_paths):
            return

        # Step 3: 파일 확장자 검증 및 필터링
        valid_files = self.file_selector.validate_file_extensions(file_paths)

        if not valid_files:
            messagebox.showerror(
                "오류",
                "유효한 엑셀 파일이 없습니다.\\n.xlsx 또는 .xls 파일만 지원됩니다."
            )
            return

        self.logger.info(f"선택된 파일 수: {len(valid_files)}개")

        # Step 4: 파일 병합
        header, data_rows, error_msg = self.merger.merge_files(valid_files)

        if error_msg:
            messagebox.showerror("병합 실패", error_msg)
            return

        # Step 5: 파일 저장 (저장 위치는 이미 선택됨)
        try:
            filename = self.file_writer.generate_filename()
            save_path = self.file_writer.get_unique_filepath(save_location, filename)

            self.file_writer.create_merged_file(save_path, header, data_rows)  # type: ignore  # noqa: E501

            messagebox.showinfo(
                "완료",
                f"병합이 완료되었습니다!\\n\\n저장 위치:\\n{save_path}\\n\\n병합된 파일: {len(data_rows)}개"  # noqa: E501
            )

        except Exception as e:
            error_msg = f"파일 저장 중 오류가 발생했습니다:\\n\\n{e}"
            if self.logger:
                self.logger.error(error_msg)
            messagebox.showerror("저장 실패", error_msg)

    def _get_initial_save_location(self) -> str:
        """초기 저장 위치 선택 (로그 파일 생성용)

        Returns:
            선택된 디렉토리 경로, 취소 시 빈 문자열
        """
        from tkinter import filedialog
        folder_path = filedialog.askdirectory(
            title="결과 파일 및 로그 파일 저장 위치 선택"
        )
        return folder_path if folder_path else ""

    def _select_files(self) -> Optional[List[str]]:
        """파일 선택 방법을 선택하고 파일 목록 반환

        Returns:
            선택된 파일 경로 리스트, 취소 시 None
        """
        choice = messagebox.askquestion(
            "파일 선택 방법",
            "폴더를 선택하시겠습니까?\\n\\n예: 폴더 선택 (폴더 내 모든 엑셀 파일)\\n아니오: 파일 직접 선택"  # noqa: E501
        )

        if choice == "yes":
            return self.file_selector.select_folder()
        else:
            return self.file_selector.select_files()


def main() -> None:
    """메인 함수"""
    app = ExcelMergerApp()
    app.run()


if __name__ == "__main__":
    main()
