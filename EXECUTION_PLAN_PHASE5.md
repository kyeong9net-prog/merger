# Execution Plan: Phase 5 구현

## 목표
SPEC.md Phase 5에 정의된 테스트만 수행 (추가 테스트 없음)

## Phase 5 요구사항

### 1. 단위 테스트
- 파일 선택 기능 테스트
- 데이터 추출 기능 테스트
- 헤더 검증 로직 테스트
- 예외 처리 테스트

### 2. 통합 테스트
- 파일 20개 기준 병합 테스트
- 파일 50개 기준 병합 테스트
- 파일 100개 기준 병합 테스트
- 성능 테스트 (5초 이내 처리)

### 3. 엣지 케이스 테스트
- 빈 파일 처리
- summary 시트가 없는 파일 처리
- 잠긴 파일 처리
- 열 개수가 다른 파일들 병합
- 한국어 파일명 처리

## 구현 전략

### 원칙
- Phase 5에 정의되지 않은 테스트는 작성하지 않음
- pytest를 사용한 간단하고 명확한 테스트 작성
- 실제 엑셀 파일을 사용한 실용적인 테스트
- SOLID 원칙 유지

### 테스트 프레임워크
- **pytest**: Python의 표준 테스트 프레임워크
- **openpyxl**: 테스트용 엑셀 파일 생성
- 복잡한 mocking보다 실제 파일 기반 테스트 선호

## 구현 단계

### Step 1: 테스트 환경 설정
**작업 내용**:
- [ ] requirements.txt에 pytest 추가
- [ ] tests/ 디렉토리 생성
- [ ] tests/__init__.py 생성
- [ ] tests/fixtures/ 디렉토리 생성 (테스트용 엑셀 파일)
- [ ] pytest.ini 설정 파일 생성
- [ ] .gitignore 업데이트 (pytest 캐시 제외)

**파일 구조**:
```
tests/
├── __init__.py
├── fixtures/
│   └── (테스트용 엑셀 파일들)
├── test_file_selector.py
├── test_excel_reader.py
├── test_header_validator.py
├── test_exception_handling.py
├── test_integration.py
└── test_edge_cases.py
```

Lint & TypeCheck 실행

### Step 2: 단위 테스트 작성
**작업 내용**:

#### 2-1. test_file_selector.py
- [ ] 파일 개수 검증 테스트 (0개, 1개, 100개, 101개)
- [ ] 파일 확장자 검증 테스트 (.xlsx, .xls, .txt 등)

**테스트 케이스**:
```python
def test_validate_file_count_valid()
def test_validate_file_count_zero()
def test_validate_file_count_exceeded()
def test_validate_file_extensions()
```

#### 2-2. test_excel_reader.py
- [ ] summary 시트 찾기 테스트 (대소문자 구분 없이)
- [ ] 1행 추출 테스트
- [ ] 2행 추출 테스트
- [ ] 빈 행 검증 테스트

**테스트 케이스**:
```python
def test_find_summary_sheet_case_insensitive()
def test_extract_row_data()
def test_is_row_empty()
def test_read_file_success()
```

#### 2-3. test_header_validator.py
- [ ] 헤더 비어있음 검증 테스트
- [ ] 병합 셀 검증 테스트
- [ ] 날짜 형식 검증 테스트
- [ ] 수식 검증 테스트

**테스트 케이스**:
```python
def test_header_empty_raises_error()
def test_header_merged_cells_raises_error()
def test_header_date_format_raises_error()
def test_header_formula_raises_error()
def test_header_valid_passes()
```

#### 2-4. test_exception_handling.py
- [ ] PermissionError 처리 테스트
- [ ] FileNotFoundError 처리 테스트
- [ ] 잘못된 파일 형식 처리 테스트

**테스트 케이스**:
```python
def test_file_locked_handling()
def test_file_not_found_handling()
def test_invalid_file_format_handling()
```

Lint & TypeCheck 실행

### Step 3: 통합 테스트 작성
**작업 내용**:

#### 3-1. test_integration.py
- [ ] 파일 20개 병합 테스트
- [ ] 파일 50개 병합 테스트
- [ ] 파일 100개 병합 테스트
- [ ] 성능 테스트 (100개 파일 5초 이내)

**테스트 케이스**:
```python
def test_merge_20_files()
def test_merge_50_files()
def test_merge_100_files()
def test_performance_100_files_under_5_seconds()
```

**테스트 데이터 생성**:
- 테스트용 엑셀 파일 자동 생성 함수
- summary 시트가 있는 정상 파일
- 각 파일에 2행 데이터 포함

Lint & TypeCheck 실행

### Step 4: 엣지 케이스 테스트 작성
**작업 내용**:

#### 4-1. test_edge_cases.py
- [ ] 빈 파일 처리 테스트
- [ ] summary 시트 없는 파일 처리 테스트
- [ ] 잠긴 파일 처리 테스트 (시뮬레이션)
- [ ] 열 개수가 다른 파일들 병합 테스트
- [ ] 한국어 파일명 처리 테스트

**테스트 케이스**:
```python
def test_empty_file_handling()
def test_no_summary_sheet_handling()
def test_locked_file_handling()
def test_different_column_counts()
def test_korean_filename_handling()
```

**테스트 시나리오**:
- 빈 파일: 시트는 있지만 데이터 없음
- summary 시트 없음: 다른 시트만 있는 파일
- 열 개수 다름: 파일1(5개), 파일2(10개), 파일3(3개)
- 한국어 파일명: "테스트_파일_한글.xlsx"

Lint & TypeCheck 실행

### Step 5: 테스트 실행 및 검증
**작업 내용**:
- [ ] pytest 실행하여 모든 테스트 통과 확인
- [ ] 테스트 커버리지 확인 (선택사항)
- [ ] 실패하는 테스트 수정

**실행 명령**:
```bash
python -m pytest tests/ -v
python -m pytest tests/ -v --tb=short  # 짧은 트레이스백
```

### Step 6: SPEC.md 업데이트
- [ ] Phase 5 체크박스 업데이트

## 주의사항

- Phase 5에 정의되지 않은 테스트는 작성하지 않음
- 실제 파일 기반 테스트로 실용성 확보
- 간단하고 명확한 테스트 작성
- 각 단계마다 lint와 typecheck 실행

## 완료 기준

- [ ] 모든 단위 테스트 작성 및 통과
- [ ] 모든 통합 테스트 작성 및 통과
- [ ] 모든 엣지 케이스 테스트 작성 및 통과
- [ ] 성능 테스트 통과 (100개 파일 5초 이내)
- [ ] SPEC.md Phase 5 체크박스 업데이트
- [ ] Lint 에러 0개
- [ ] Type check 에러 0개

## 예상 파일 변경

1. **EXECUTION_PLAN_PHASE5.md** (신규)
2. **requirements.txt** (수정 - pytest 추가)
3. **pytest.ini** (신규 - pytest 설정)
4. **.gitignore** (수정 - pytest 캐시 제외)
5. **tests/__init__.py** (신규)
6. **tests/test_file_selector.py** (신규)
7. **tests/test_excel_reader.py** (신규)
8. **tests/test_header_validator.py** (신규)
9. **tests/test_exception_handling.py** (신규)
10. **tests/test_integration.py** (신규)
11. **tests/test_edge_cases.py** (신규)
12. **SPEC.md** (수정 - Phase 5 체크박스)

## 테스트 데이터 생성 전략

### 간단한 헬퍼 함수
```python
def create_test_excel_file(filepath, has_summary=True, has_data=True,
                          columns=5, merged_cells=False, has_formula=False):
    """테스트용 엑셀 파일 생성"""
    # openpyxl로 간단한 테스트 파일 생성
```

이 함수를 사용하여 필요한 테스트 파일을 동적으로 생성하고,
테스트 종료 후 정리(cleanup)합니다.
