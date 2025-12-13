"""엑셀 파일 병합 도구 - 메인 프로그램 (Phase 1)

Entry Point: 사용자와의 인터페이스 및 전체 플로우 관리
"""
import tkinter as tk
from tkinter import messagebox
from typing import List, Optional
from src.file_selector import FileSelector
from src.excel_merger import ExcelMerger
from src.file_writer import FileWriter


class ExcelMergerApp:
    """엑셀 병합 도구 메인 애플리케이션"""

    def __init__(self) -> None:
        """애플리케이션 초기화"""
        self.file_selector = FileSelector()
        self.merger = ExcelMerger()
        self.file_writer = FileWriter()

        # Tkinter root 생성 (UI 백엔드)
        self.root = tk.Tk()
        self.root.withdraw()  # 메인 윈도우 숨기기

    def run(self) -> None:
        """애플리케이션 실행"""
        print("=" * 60)
        print("엑셀 파일 병합 도구 (Phase 1)")
        print("=" * 60)
        print()

        # Step 1: 파일 선택 방법 선택
        file_paths = self._select_files()

        if not file_paths:
            print("[INFO] 파일이 선택되지 않았습니다. 프로그램을 종료합니다.")
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

        print(f"[INFO] 선택된 파일 수: {len(valid_files)}개\\n")

        # Step 4: 파일 병합
        header, data_rows, error_msg = self.merger.merge_files(valid_files)

        if error_msg:
            messagebox.showerror("병합 실패", error_msg)
            return

        # Step 5: 저장 위치 선택
        save_location = self.file_writer.select_save_location()

        if not save_location:
            print("[INFO] 저장 위치가 선택되지 않았습니다. 프로그램을 종료합니다.")
            return

        # Step 6: 파일 저장
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
            print(f"[ERROR] {error_msg}")
            messagebox.showerror("저장 실패", error_msg)

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
