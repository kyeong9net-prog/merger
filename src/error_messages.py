"""오류 메시지 표준화 헬퍼 (Phase 4)

Phase 4 품질 요구사항:
- 표준화된 포맷으로 오류 메시지 출력
- 사용자가 이해하기 쉬운 메시지 작성
"""


def format_error(title: str, cause: str, solution: str) -> str:
    """표준 포맷의 오류 메시지 생성

    Args:
        title: 오류 제목
        cause: 오류 원인
        solution: 해결 방법

    Returns:
        포맷팅된 오류 메시지
    """
    return f"{title}\n\n원인: {cause}\n\n해결 방법:\n{solution}"


# 헤더 검증 관련 오류 메시지
def header_empty_error() -> str:
    """헤더 비어있음 오류"""
    return format_error(
        title="헤더 검증 오류",
        cause="첫 번째 행(헤더)이 완전히 비어있습니다.",
        solution="첫 번째 파일의 summary 시트 1행에 헤더 데이터를 입력해주세요."
    )


def header_merged_cells_error() -> str:
    """헤더 병합 셀 오류"""
    return format_error(
        title="헤더 검증 오류",
        cause="첫 번째 행(헤더)에 병합된 셀이 포함되어 있습니다.",
        solution="summary 시트 1행의 병합된 셀을 모두 해제해주세요."
    )


def header_date_format_error() -> str:
    """헤더 날짜 형식 오류"""
    return format_error(
        title="헤더 검증 오류",
        cause="첫 번째 행(헤더)에 날짜 형식이 포함되어 있습니다.",
        solution="summary 시트 1행의 날짜 형식을 텍스트로 변경해주세요."
    )


def header_formula_error() -> str:
    """헤더 수식 오류"""
    return format_error(
        title="헤더 검증 오류",
        cause="첫 번째 행(헤더)에 수식이 포함되어 있습니다.",
        solution="summary 시트 1행의 수식을 값으로 변환해주세요."
    )


# 파일 처리 관련 오류 메시지
def no_valid_files_error() -> str:
    """유효한 파일 없음 오류"""
    return format_error(
        title="파일 처리 오류",
        cause="병합 가능한 유효한 파일이 없습니다.",
        solution=(
            "1. 모든 파일에 'summary' 시트가 있는지 확인하세요.\n"
            "2. 각 파일의 summary 시트 2행에 데이터가 있는지 확인하세요.\n"
            "3. 파일이 다른 프로그램에서 열려있지 않은지 확인하세요."
        )
    )


def no_data_rows_error() -> str:
    """데이터 행 없음 오류"""
    return format_error(
        title="데이터 처리 오류",
        cause="모든 파일의 summary 시트 2행이 비어있습니다.",
        solution="최소 한 개 이상의 파일에 summary 시트 2행 데이터가 필요합니다."
    )


def file_count_exceeded_error(max_files: int) -> str:
    """파일 개수 초과 오류"""
    return format_error(
        title="파일 개수 초과",
        cause=f"선택한 파일이 최대 허용 개수({max_files}개)를 초과했습니다.",
        solution=f"파일을 {max_files}개 이하로 선택해주세요."
    )
