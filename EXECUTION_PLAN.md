# Execution Plan: Phase 1 구현

## 목표
SPEC.md Phase 1에 정의된 기본 기능만 구현 (추가 기능 없음)

## 기술 스택
- **언어**: Python 3.8+
- **엑셀 처리**: openpyxl
- **UI**: tkinter (Python 기본 내장)
- **패키징**: PyInstaller (Phase 1에서는 개발만, Phase 6에서 패키징)
- **코드 품질**: flake8 (lint), mypy (type check)

## 아키텍처 설계 (SOLID 원칙 준수)

### 1. Single Responsibility Principle (단일 책임 원칙)
각 클래스는 하나의 책임만 가짐:
- `FileSelector`: 파일 선택 UI 및 검증
- `ExcelReader`: 엑셀 파일 읽기 및 데이터 추출
- `HeaderValidator`: 헤더 검증
- `ExcelMerger`: 병합 로직
- `FileWriter`: 결과 파일 저장

### 2. 프로젝트 구조
```
merger/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 진입점
│   ├── file_selector.py        # 파일 선택 UI
│   ├── excel_reader.py         # 엑셀 읽기
│   ├── header_validator.py     # 헤더 검증
│   ├── excel_merger.py         # 병합 로직
│   └── file_writer.py          # 파일 저장
├── requirements.txt
├── setup.py
├── .flake8
├── mypy.ini
├── PRD.md
└── SPEC.md
```

## 구현 단계

### Step 1: 프로젝트 구조 및 개발 환경 설정
- [ ] src/ 디렉토리 생성
- [ ] requirements.txt 작성 (openpyxl)
- [ ] .flake8 설정 파일 작성
- [ ] mypy.ini 설정 파일 작성
- [ ] __init__.py 파일들 생성

### Step 2: 파일 선택 UI 구현 (file_selector.py)
Phase 1 요구사항:
- [ ] 1개~100개의 엑셀 파일 선택 UI
- [ ] 다중 파일 선택 지원
- [ ] 폴더 단위 선택 지원 (폴더 내 엑셀 파일만 자동 인식)
- [ ] 최대 100개 파일 제한 검증 및 오류 메시지

구현:
- tkinter.filedialog 사용
- askopenfilenames() - 다중 파일 선택
- askdirectory() - 폴더 선택
- .xlsx, .xls 필터링
- Lint & TypeCheck 실행

### Step 3: 엑셀 데이터 추출 로직 (excel_reader.py)
Phase 1 요구사항:
- [ ] summary 시트 검색 (대소문자 구분 없이)
- [ ] 2행 전체 데이터 추출 (A2부터 마지막 컬럼까지)
- [ ] 2행 전체가 비어있는 경우 스킵 처리
- [ ] 스킵된 파일 로그 기록

구현:
- openpyxl로 엑셀 파일 읽기
- 시트명 대소문자 무시 검색
- 2행 데이터 추출 및 빈 행 체크
- 간단한 로그 출력 (print 사용)
- Lint & TypeCheck 실행

### Step 4: 헤더 검증 로직 (header_validator.py)
Phase 1 요구사항:
- [ ] 첫 번째 성공 파일의 1행을 헤더로 사용
- [ ] 1행 전체가 비어있는 경우 오류
- [ ] 1행에 병합 셀이 있는 경우 오류
- [ ] 1행에 날짜 형식이 포함된 경우 오류
- [ ] 1행에 수식이 포함된 경우 오류

구현:
- 1행 데이터 검증 함수
- 병합 셀 체크
- 날짜/수식 체크
- 검증 실패 시 예외 발생
- Lint & TypeCheck 실행

### Step 5: 결과 파일 생성 로직 (file_writer.py)
Phase 1 요구사항:
- [ ] 모든 2행 데이터를 순차적으로 병합
- [ ] 파일명 형식: merged_summary_yyyyMMdd_HHmm.xlsx
- [ ] 사용자 지정 경로에 저장
- [ ] 동일 파일명 존재 시 자동 번호 증가

구현:
- openpyxl로 새 워크북 생성
- 헤더 + 데이터 행 추가
- 파일명 생성 (datetime 사용)
- 중복 파일명 처리
- Lint & TypeCheck 실행

### Step 6: 병합 로직 통합 (excel_merger.py)
- [ ] 전체 병합 프로세스 조율
- [ ] 에러 처리
- Lint & TypeCheck 실행

### Step 7: 메인 프로그램 (main.py)
- [ ] UI 실행
- [ ] 사용자 플로우 구현
- Lint & TypeCheck 실행

### Step 8: 최종 검증
- [ ] 전체 Lint 실행 (flake8)
- [ ] 전체 TypeCheck 실행 (mypy)
- [ ] SPEC.md Phase 1 체크박스 업데이트

## 주의사항
- Phase 1에 정의되지 않은 기능은 구현하지 않음
- 복잡한 로깅 시스템 대신 print 사용 (Phase 2에서 강화)
- 파일 포맷 검증은 확장자만 체크 (Phase 2에서 강화)
- 간결하고 읽기 쉬운 코드 작성
- SOLID 원칙 준수

## 완료 기준
- [ ] 모든 Phase 1 요구사항 구현
- [ ] Lint 에러 0개
- [ ] Type check 에러 0개
- [ ] SPEC.md Phase 1 체크박스 업데이트
