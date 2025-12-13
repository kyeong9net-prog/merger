# Execution Plan: Phase 4 구현

## 목표
SPEC.md Phase 4에 정의된 품질 요구사항만 수행 (추가 기능 없음)

## Phase 4 요구사항

### 1. 다국어 및 호환성
- 파일명에 한국어 포함 가능
- summary 시트의 열 개수가 파일마다 달라도 정상 병합

### 2. 데이터 안전성
- 원본 파일 읽기 전용(read-only) 처리
- 원본 파일 수정 금지
- 결과 파일 생성 실패 시 명확한 오류 메시지 제공

### 3. 오류 메시지 표준화
- 표준화된 포맷으로 오류 메시지 출력
- 사용자가 이해하기 쉬운 메시지 작성

## 구현 전략

### 원칙
- Phase 4에 정의되지 않은 기능은 구현하지 않음
- 기존 코드를 최대한 활용하고, 필요한 부분만 수정
- 간단하고 명확한 구현 선택
- SOLID 원칙 유지

## 구현 단계

### Step 1: 현재 코드 분석 및 Phase 4 요구사항 매핑
**작업 내용**:
- [ ] 현재 코드가 이미 지원하는 기능 확인
- [ ] 추가/수정이 필요한 기능 파악

**분석 대상**:
1. **한국어 파일명 지원**
   - Python 3.9+ 및 openpyxl은 기본적으로 UTF-8 지원
   - 현재 코드에서 파일명 처리 방식 확인
   - 테스트 케이스 작성 필요 여부 확인

2. **가변 열 개수 지원**
   - 현재 `excel_reader.py`의 row 추출 로직 확인
   - 각 파일의 열 개수가 달라도 문제없는지 확인
   - 필요시 수정

3. **읽기 전용 처리**
   - `load_workbook(file_path, data_only=True)` 사용 확인
   - workbook.save() 호출이 없는지 확인
   - 명시적 read_only 모드 사용 검토

4. **오류 메시지**
   - 현재 오류 메시지들 수집
   - 표준 포맷 정의
   - 사용자 친화적 메시지로 개선

Lint & TypeCheck 실행

### Step 2: 다국어 및 호환성 구현
**작업 내용**:

#### 2-1. 한국어 파일명 지원 확인
- [ ] 현재 코드에서 한국어 파일명 처리 확인
- [ ] `os.path.basename()` 사용 부분 확인
- [ ] 필요시 명시적 UTF-8 인코딩 추가
- [ ] 주석/문서에 한국어 파일명 지원 명시

**구현 방법**:
- Python 3.9+는 기본적으로 UTF-8을 사용하므로 별도 처리 불필요
- 이미 지원되고 있다면 추가 코드 없이 확인만 수행

#### 2-2. 가변 열 개수 지원 구현
- [ ] `excel_reader.py`의 `_extract_row_data()` 메서드 확인
- [ ] 각 파일의 max_column을 동적으로 처리하는지 확인
- [ ] 필요시 수정하여 파일마다 다른 열 개수 지원

**현재 코드**:
```python
max_col = sheet.max_column
row_data = []
for col in range(1, max_col + 1):
    cell_value = sheet.cell(row=2, column=col).value
    row_data.append(cell_value)
```

**확인 사항**:
- 각 파일마다 max_column이 다를 때 정상 작동하는지
- 헤더 열 개수와 데이터 열 개수가 다를 때 처리 방법

**구현 방법**:
- 헤더보다 짧은 row는 None으로 패딩
- 헤더보다 긴 row는 그대로 추가 (Excel에서 자동 처리)

Lint & TypeCheck 실행

### Step 3: 데이터 안전성 강화
**작업 내용**:

#### 3-1. 읽기 전용 처리 명확화
- [ ] `excel_reader.py`에서 `read_only=True` 파라미터 추가
- [ ] workbook.save() 호출이 없는지 전체 코드 확인
- [ ] 주석에 "읽기 전용" 명시

**수정 위치**: `src/excel_reader.py`
```python
# 변경 전
workbook = load_workbook(file_path, data_only=True)

# 변경 후
workbook = load_workbook(file_path, data_only=True, read_only=True)
```

#### 3-2. 결과 파일 생성 실패 시 오류 메시지 개선
- [ ] `file_writer.py`의 예외 처리 개선
- [ ] 구체적인 실패 원인 제공
- [ ] 사용자가 이해하기 쉬운 메시지로 변경

**수정 위치**: `src/file_writer.py`의 `create_merged_file()` 메서드

Lint & TypeCheck 실행

### Step 4: 오류 메시지 표준화
**작업 내용**:

#### 4-1. 오류 메시지 포맷 정의
- [ ] 간단한 메시지 헬퍼 클래스/함수 생성
- [ ] 표준 포맷 정의

**표준 포맷 구조**:
```
[오류 유형]
원인: [구체적인 원인]
해결 방법: [사용자가 취할 수 있는 조치]
```

#### 4-2. 기존 오류 메시지 개선
- [ ] `src/header_validator.py`의 오류 메시지 개선
- [ ] `src/excel_merger.py`의 오류 메시지 개선
- [ ] `src/main.py`의 오류 메시지 개선
- [ ] 기술 용어 제거, 사용자 친화적 표현 사용

**개선 예시**:
```python
# 변경 전
"1행에 병합된 셀이 있습니다."

# 변경 후
"헤더 검증 오류\n원인: 첫 번째 행에 병합된 셀이 포함되어 있습니다.\n해결 방법: 헤더 행(1행)의 병합된 셀을 해제해주세요."
```

**구현 방법**:
- 복잡한 클래스보다 간단한 헬퍼 함수 사용
- `src/error_messages.py` 생성
- 주요 오류 타입별 메시지 템플릿 제공

Lint & TypeCheck 실행

### Step 5: 통합 테스트
- [ ] 한국어 파일명으로 테스트
- [ ] 열 개수가 다른 파일들로 병합 테스트
- [ ] 읽기 전용 확인
- [ ] 오류 메시지 확인

### Step 6: SPEC.md 업데이트
- [ ] Phase 4 체크박스 업데이트

## 주의사항

- Phase 4에 정의되지 않은 기능은 구현하지 않음
- 기존 코드의 구조를 최대한 유지
- 간단하고 명확한 구현 우선
- 각 단계마다 lint와 typecheck 실행

## 완료 기준

- [ ] 한국어 파일명 정상 처리 확인
- [ ] 열 개수가 다른 파일들 병합 지원
- [ ] 원본 파일 읽기 전용 처리 확인
- [ ] 오류 메시지 표준화 및 개선
- [ ] SPEC.md Phase 4 체크박스 업데이트
- [ ] Lint 에러 0개
- [ ] Type check 에러 0개

## 예상 파일 변경

1. **EXECUTION_PLAN_PHASE4.md** (신규)
2. **src/excel_reader.py** (수정 - read_only 추가)
3. **src/error_messages.py** (신규 - 오류 메시지 헬퍼)
4. **src/header_validator.py** (수정 - 오류 메시지 개선)
5. **src/excel_merger.py** (수정 - 오류 메시지 개선)
6. **src/file_writer.py** (수정 - 오류 메시지 개선)
7. **src/main.py** (수정 - 오류 메시지 개선)
8. **SPEC.md** (수정 - Phase 4 체크박스)
