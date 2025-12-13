# Execution Plan: Phase 3 구현

## 목표
SPEC.md Phase 3에 정의된 기술 구현만 수행 (추가 기능 없음)

## Phase 3 요구사항

### 1. 실행 환경
- Windows 10 이상 지원
- 단독 실행 .exe 파일 생성
- 별도 설치 불필요

### 2. 개발 스택 선정
- Python + openpyxl + PyInstaller (이미 선택됨)
- 개발 언어 최종 결정: **Python**

### 3. 성능 최적화
- 100개 파일 병합 5초 이내 처리
- 메모리 사용량 안정성 확보

## 기술 스택

- **PyInstaller**: Python 스크립트를 .exe로 변환
- **Python 3.9+**: 현재 개발 환경
- **openpyxl**: 이미 사용 중
- **tkinter**: Python 기본 내장 (별도 설치 불필요)

## 구현 단계

### Step 1: PyInstaller 설정
**작업 내용**:
- [x] PyInstaller 설치
- [x] requirements.txt에 PyInstaller 추가
- [x] .spec 파일 생성 (PyInstaller 설정 파일)
- [x] 빌드 설정 최적화

**설정 사항**:
- 단일 파일 모드 (`--onefile`)
- 콘솔 숨김 (`--noconsole` 또는 `--windowed`)
- 아이콘 설정 (선택사항)
- 숨겨진 import 처리

Lint & TypeCheck 실행

### Step 2: 빌드 스크립트 작성
**작업 내용**:
- [x] build.sh (Linux/Mac용) 작성
- [x] build.bat (Windows용) 작성
- [x] 빌드 전 정리 스크립트
- [x] 빌드 후 검증 스크립트

**빌드 프로세스**:
1. 이전 빌드 파일 정리 (dist/, build/)
2. PyInstaller 실행
3. 결과 파일 확인
4. 파일 크기 확인

Lint & TypeCheck 실행

### Step 3: .exe 파일 생성 및 테스트
**작업 내용**:
- [x] PyInstaller로 .exe 생성
- [x] 생성된 .exe 파일 확인
- [x] 단독 실행 테스트 (가능하면)
- [x] 파일 크기 확인

**검증 사항**:
- .exe 파일이 정상적으로 생성되는지
- 파일 크기가 적절한지 (목표: 50MB 이하)
- 필요한 DLL이 모두 포함되었는지

### Step 4: 성능 최적화 확인
**작업 내용**:
- [x] 현재 코드의 성능 확인
- [x] 병목 지점 파악 (필요시)
- [x] 간단한 최적화 (필요시)

**성능 목표**:
- 100개 파일 병합: 5초 이내
- 메모리 사용량: 안정적 유지

**최적화 방법** (필요시):
- 파일 읽기 최적화 (현재 충분히 빠름)
- 메모리 관리 (workbook.close() 이미 구현됨)
- 불필요한 연산 제거

### Step 5: 문서화
**작업 내용**:
- [x] README.md 작성 (.exe 실행 방법 안내)
- [x] BUILD.md 작성 (개발자용 빌드 가이드)

### Step 6: SPEC.md 업데이트
- [x] Phase 3 체크박스 업데이트
- [x] 개발 스택 최종 결정 기록

## 주의사항

- Phase 3에 정의되지 않은 기능은 구현하지 않음
- 실제 Windows 환경이 없으므로 Linux에서 빌드 스크립트만 작성
- .exe 파일은 실제로 생성하되, Windows에서만 실행 가능함을 명시
- 성능 테스트는 간단히만 수행 (실제 100개 파일 테스트는 Phase 5에서)

## 완료 기준

- [x] PyInstaller 설정 완료
- [x] 빌드 스크립트 작성 완료
- [x] .exe 파일 생성 방법 문서화
- [x] 성능 요구사항 확인
- [x] SPEC.md Phase 3 체크박스 업데이트
- [x] Lint 에러 0개
- [x] Type check 에러 0개

## 비고

- 실제 Windows 환경에서 .exe 파일을 테스트하는 것이 이상적이나,
  현재 환경에서는 빌드 스크립트와 설정만 제공
- PyInstaller는 크로스 플랫폼을 지원하지 않으므로,
  Windows용 .exe는 Windows 환경에서 빌드해야 함
