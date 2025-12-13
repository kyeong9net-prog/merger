"""로깅 시스템 (Phase 2)

Single Responsibility: 로그 출력 및 파일 저장만 담당
"""
import os
from datetime import datetime
from typing import Optional


class Logger:
    """로그 출력 및 파일 저장 클래스"""

    def __init__(self, log_file_path: Optional[str] = None) -> None:
        """Logger 초기화

        Args:
            log_file_path: 로그 파일 경로 (None이면 파일 저장 안 함)
        """
        self.log_file_path = log_file_path
        self._initialized = False

        if log_file_path:
            self._initialize_log_file()

    def _initialize_log_file(self) -> None:
        """로그 파일 초기화"""
        if not self.log_file_path:
            return

        try:
            # 로그 파일 디렉토리 생성
            log_dir = os.path.dirname(self.log_file_path)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # 로그 파일 헤더 작성
            with open(self.log_file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\\n")
                f.write("엑셀 파일 병합 도구 - 로그 파일\\n")
                f.write(f"생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                f.write("=" * 60 + "\\n\\n")

            self._initialized = True

        except Exception as e:
            print(f"[경고] 로그 파일 초기화 실패: {e}")
            self.log_file_path = None

    def log(self, level: str, message: str, file_name: str = "") -> None:
        """로그 메시지 출력 및 저장

        Args:
            level: 로그 레벨 (SUCCESS, SKIP, ERROR, INFO)
            message: 로그 메시지
            file_name: 파일명 (선택)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 로그 메시지 포맷
        if file_name:
            log_message = f"[{timestamp}] [{level}] {file_name} - {message}"
        else:
            log_message = f"[{timestamp}] [{level}] {message}"

        # 콘솔 출력
        print(log_message)

        # 파일에 저장
        if self.log_file_path and self._initialized:
            try:
                with open(self.log_file_path, 'a', encoding='utf-8') as f:
                    f.write(log_message + "\\n")
            except Exception as e:
                print(f"[경고] 로그 파일 쓰기 실패: {e}")

    def success(self, message: str, file_name: str = "") -> None:
        """SUCCESS 레벨 로그

        Args:
            message: 로그 메시지
            file_name: 파일명 (선택)
        """
        self.log("SUCCESS", message, file_name)

    def skip(self, message: str, file_name: str = "") -> None:
        """SKIP 레벨 로그

        Args:
            message: 로그 메시지
            file_name: 파일명 (선택)
        """
        self.log("SKIP", message, file_name)

    def error(self, message: str, file_name: str = "") -> None:
        """ERROR 레벨 로그

        Args:
            message: 로그 메시지
            file_name: 파일명 (선택)
        """
        self.log("ERROR", message, file_name)

    def info(self, message: str, file_name: str = "") -> None:
        """INFO 레벨 로그

        Args:
            message: 로그 메시지
            file_name: 파일명 (선택)
        """
        self.log("INFO", message, file_name)

    @staticmethod
    def generate_log_filename() -> str:
        """로그 파일명 생성

        Returns:
            생성된 로그 파일명
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        return f"merger_log_{timestamp}.txt"
