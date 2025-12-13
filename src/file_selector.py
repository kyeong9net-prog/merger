"""파일 선택 UI 및 검증 (Phase 1)

Single Responsibility: 파일 선택과 기본 검증만 담당
"""
import os
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import List, Optional


class FileSelector:
    """엑셀 파일 선택 및 검증을 담당하는 클래스"""

    MAX_FILES = 100
    ALLOWED_EXTENSIONS = ('.xlsx', '.xls')

    def __init__(self) -> None:
        """FileSelector 초기화"""
        pass

    def select_files(self) -> Optional[List[str]]:
        """다중 파일 선택 UI 표시

        Returns:
            선택된 파일 경로 리스트, 취소 시 None
        """
        file_paths = filedialog.askopenfilenames(
            title="엑셀 파일 선택 (최대 100개)",
            filetypes=[
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*")
            ]
        )

        if not file_paths:
            return None

        return list(file_paths)

    def select_folder(self) -> Optional[List[str]]:
        """폴더 선택 UI 표시 및 엑셀 파일 자동 인식

        Returns:
            폴더 내 엑셀 파일 경로 리스트, 취소 시 None
        """
        folder_path = filedialog.askdirectory(
            title="폴더 선택 (폴더 내 엑셀 파일만 자동 인식)"
        )

        if not folder_path:
            return None

        excel_files = self._find_excel_files(folder_path)
        return excel_files

    def _find_excel_files(self, folder_path: str) -> List[str]:
        """폴더 내 엑셀 파일 찾기

        Args:
            folder_path: 검색할 폴더 경로

        Returns:
            발견된 엑셀 파일 경로 리스트
        """
        excel_files = []
        folder = Path(folder_path)

        for file_path in folder.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in self.ALLOWED_EXTENSIONS:
                excel_files.append(str(file_path))

        return excel_files

    def validate_file_count(self, file_paths: List[str]) -> bool:
        """파일 개수 검증 (최대 100개)

        Args:
            file_paths: 검증할 파일 경로 리스트

        Returns:
            검증 통과 여부
        """
        if len(file_paths) == 0:
            messagebox.showerror(
                "오류",
                "선택된 파일이 없습니다."
            )
            return False

        if len(file_paths) > self.MAX_FILES:
            messagebox.showerror(
                "오류",
                f"최대 {self.MAX_FILES}개의 파일만 선택할 수 있습니다.\\n"
                f"현재 선택된 파일: {len(file_paths)}개"
            )
            return False

        return True

    def validate_file_extensions(self, file_paths: List[str]) -> List[str]:
        """파일 확장자 검증 및 필터링

        Args:
            file_paths: 검증할 파일 경로 리스트

        Returns:
            유효한 엑셀 파일 경로 리스트
        """
        valid_files = []
        invalid_files = []

        for file_path in file_paths:
            ext = os.path.splitext(file_path)[1].lower()
            if ext in self.ALLOWED_EXTENSIONS:
                valid_files.append(file_path)
            else:
                invalid_files.append(os.path.basename(file_path))

        if invalid_files:
            print(f"[SKIP] 지원하지 않는 파일 형식: {', '.join(invalid_files)}")

        return valid_files
