# Execution Plan: Phase 2 구현

## 목표
SPEC.md Phase 2에 정의된 예외 처리 및 로그 강화 기능만 구현 (추가 기능 없음)

## Phase 1에서 이미 구현된 기능
✅ **파일 포맷 검증**: file_selector.py에서 .xlsx, .xls 필터링
✅ **시트 검증**: excel_reader.py에서 summary 시트 및 2행 검증
✅ **기본 로그**: print 문으로 SUCCESS, SKIP 출력

## Phase 2에서 추가/강화할 기능

### 1. 파일 포맷 검증 (이미 구현됨)
- Phase 1에서 file_selector.py에 구현됨
- 확인 및 체크박스 업데이트만 필요

### 2. 시트 검증 (이미 구현됨)
- Phase 1에서 excel_reader.py에 구현됨
- 확인 및 체크박스 업데이트만 필요

### 3. 파일 접근 오류 처리 (신규)
- 파일 잠김(File Locked) 상태 처리
- 잠긴 파일은 스킵하고 전체 작업 계속
- 오류 메시지 출력

### 4. 로그 출력 시스템 강화 (신규)
- 시간 스탬프 포함
- 처리 상태 표시 (SUCCESS, SKIP, ERROR)
- 파일명 기록
- 상세 이유 기록
- 로그 파일 저장 기능

## 아키텍처 설계 (SOLID 원칙 준수)

### Single Responsibility Principle
새로운 Logger 클래스 생성:
- `Logger`: 로깅 전용 클래스 (콘솔 출력 + 파일 저장)

### 기존 클래스 수정 (최소화)
- `ExcelReader`: 파일 잠김 오류 처리 추가
- 모든 클래스: print 문을 Logger로 교체

## 구현 단계

### Step 1: Logger 클래스 구현
**새 파일**: `src/logger.py`

기능:
- [x] 로그 메시지 포맷: `[timestamp] [level] message`
- [x] 레벨: SUCCESS, SKIP, ERROR, INFO
- [x] 콘솔 출력 + 파일 저장
- [x] 파일명: `merger_log_yyyyMMdd_HHmm.txt`
- [x] 싱글톤 패턴 (선택적)

Lint & TypeCheck 실행

### Step 2: 파일 잠김 오류 처리
**수정 파일**: `src/excel_reader.py`

추가 기능:
- [x] try-except로 PermissionError 처리
- [x] 파일 잠김 시 스킵하고 계속 진행
- [x] Logger로 오류 메시지 출력

Lint & TypeCheck 실행

### Step 3: 기존 코드에 Logger 적용
**수정 파일**: 모든 src/*.py 파일

변경 사항:
- [x] print() → logger.log() 교체
- [x] 모든 로그에 시간 스탬프 자동 포함
- [x] 로그 레벨 명확히 지정

Lint & TypeCheck 실행

### Step 4: 검증 및 체크박스 업데이트
- [x] 파일 포맷 검증 확인 (Phase 1 구현 확인)
- [x] 시트 검증 확인 (Phase 1 구현 확인)
- [x] 파일 잠김 처리 테스트
- [x] 로그 파일 생성 확인
- [x] SPEC.md Phase 2 체크박스 업데이트

## 주의사항
- Phase 2에 정의되지 않은 기능은 구현하지 않음
- 기존 Phase 1 코드는 최소한으로만 수정
- SOLID 원칙 유지
- 간결하고 읽기 쉬운 코드 작성

## 완료 기준
- [x] 모든 Phase 2 요구사항 구현
- [x] Lint 에러 0개
- [x] Type check 에러 0개
- [x] SPEC.md Phase 2 체크박스 업데이트
- [x] Phase 1 기능 정상 작동
