# Execution Plan: Phase 6 구현

## 목표
SPEC.md Phase 6에 정의된 배포 작업만 수행 (추가 작업 없음)

## Phase 6 요구사항

### 1. 패키징
- .exe 파일 생성
- exe 파일 크기 최적화
- 바이러스 검사 통과 확인

### 2. 문서화
- 사용자 가이드 작성
- 설치 가이드 작성 (설치 불필요하지만 실행 방법 안내)
- 트러블슈팅 가이드 작성

### 3. 최종 배포
- 최종 exe 파일 제공
- 배포 완료

## 구현 전략

### 원칙
- Phase 6에 정의되지 않은 작업은 수행하지 않음
- 이미 Phase 3에서 생성한 README.md, BUILD.md 활용
- 간단하고 명확한 문서 작성
- 실제 .exe 빌드는 Windows 환경 필요 (문서화로 대체)

### 기존 파일 활용
Phase 3에서 이미 생성된 파일:
- README.md: 기본 사용자 문서
- BUILD.md: 빌드 문서
- build.bat: Windows 빌드 스크립트
- excel_merger.spec: PyInstaller 설정

## 구현 단계

### Step 1: .exe 파일 생성 준비
**작업 내용**:
- [ ] build.bat 스크립트 검증
- [ ] excel_merger.spec 최적화 확인
- [ ] .exe 파일 생성 방법 문서화
- [ ] 크기 최적화 방법 문서화

**최적화 전략**:
- UPX 압축 사용 (이미 spec 파일에 포함)
- 불필요한 모듈 제외 (이미 spec 파일에 포함)
- --onefile 모드 사용 (이미 spec 파일에 포함)

Lint & TypeCheck 실행

### Step 2: 바이러스 검사 통과 확인 방법 문서화
**작업 내용**:
- [ ] ANTIVIRUS_CHECK.md 생성
- [ ] 바이러스 검사 방법 안내
- [ ] VirusTotal 사용 방법 설명
- [ ] False Positive 대응 방법

**내용**:
- PyInstaller로 만든 .exe는 종종 바이러스 오탐 발생
- VirusTotal.com에 업로드하여 검사
- Windows Defender 예외 추가 방법
- 코드 서명 (선택사항, Phase 6 범위 외)

Lint & TypeCheck 실행

### Step 3: 사용자 가이드 작성
**작업 내용**:
- [ ] USER_GUIDE.md 생성
- [ ] 상세한 사용 방법 안내
- [ ] 스크린샷/예시 포함 (텍스트 설명)
- [ ] 주요 기능 설명

**내용 구조**:
1. 프로그램 소개
2. 시작하기
3. 파일 선택 방법
4. 결과 확인 방법
5. 로그 파일 확인
6. 주의사항

Lint & TypeCheck 실행

### Step 4: 설치 가이드 작성
**작업 내용**:
- [ ] INSTALLATION.md 생성
- [ ] .exe 파일 다운로드 및 실행 방법
- [ ] 시스템 요구사항
- [ ] 첫 실행 가이드

**내용**:
- Windows 10 이상 필요
- .exe 파일 다운로드
- 실행 방법 (더블 클릭)
- 관리자 권한 불필요
- 별도 설치 과정 없음

Lint & TypeCheck 실행

### Step 5: 트러블슈팅 가이드 작성
**작업 내용**:
- [ ] TROUBLESHOOTING.md 생성
- [ ] 자주 발생하는 문제와 해결 방법
- [ ] 오류 메시지별 대응 방법

**주요 문제들**:
1. "파일이 잠겨있습니다" 오류
   - 다른 프로그램에서 파일 닫기
2. "summary 시트가 없습니다" 오류
   - 시트명 확인
3. "헤더 검증 오류"
   - 1행 병합 셀 해제, 수식 제거
4. Windows Defender 차단
   - 예외 추가 방법
5. 파일 개수 초과
   - 100개 이하로 선택
6. 성능 문제
   - 대용량 파일 처리 팁

Lint & TypeCheck 실행

### Step 6: 배포 체크리스트 작성
**작업 내용**:
- [ ] DEPLOYMENT_CHECKLIST.md 생성
- [ ] 배포 전 확인 사항 리스트
- [ ] 테스트 항목
- [ ] 배포 절차

**체크리스트**:
- [ ] 모든 테스트 통과
- [ ] lint/typecheck 통과
- [ ] .exe 파일 빌드 성공
- [ ] .exe 파일 실행 테스트
- [ ] 문서 완성도 확인
- [ ] 버전 정보 업데이트
- [ ] README 최종 검토

Lint & TypeCheck 실행

### Step 7: 최종 배포 준비
**작업 내용**:
- [ ] 모든 문서 최종 검토
- [ ] 배포 가이드 작성
- [ ] 릴리스 노트 작성 (선택)

### Step 8: SPEC.md 업데이트
- [ ] Phase 6 체크박스 업데이트

## 주의사항

- Phase 6에 정의되지 않은 작업은 수행하지 않음
- 실제 .exe 빌드는 Windows 환경 필요 (문서화로 대체)
- 간결하고 사용자 친화적인 문서 작성
- 각 단계마다 lint와 typecheck 실행

## 완료 기준

- [ ] .exe 파일 생성 방법 문서화 완료
- [ ] exe 파일 크기 최적화 방법 문서화 완료
- [ ] 바이러스 검사 확인 방법 문서화 완료
- [ ] 사용자 가이드 (USER_GUIDE.md) 작성 완료
- [ ] 설치 가이드 (INSTALLATION.md) 작성 완료
- [ ] 트러블슈팅 가이드 (TROUBLESHOOTING.md) 작성 완료
- [ ] 배포 체크리스트 (DEPLOYMENT_CHECKLIST.md) 작성 완료
- [ ] SPEC.md Phase 6 체크박스 업데이트
- [ ] Lint 에러 0개
- [ ] Type check 에러 0개

## 예상 파일 변경

1. **EXECUTION_PLAN_PHASE6.md** (신규 - 이 파일)
2. **ANTIVIRUS_CHECK.md** (신규 - 바이러스 검사 가이드)
3. **USER_GUIDE.md** (신규 - 상세 사용자 가이드)
4. **INSTALLATION.md** (신규 - 설치/실행 가이드)
5. **TROUBLESHOOTING.md** (신규 - 문제 해결 가이드)
6. **DEPLOYMENT_CHECKLIST.md** (신규 - 배포 체크리스트)
7. **SPEC.md** (수정 - Phase 6 체크박스)

## 배포 프로세스

### Windows 환경에서 실제 빌드 시:

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 테스트 실행
python -m pytest tests/ -v

# 3. .exe 파일 빌드
build.bat

# 4. 생성된 파일 확인
# dist/ExcelMerger.exe
```

### 배포 파일:
- ExcelMerger.exe (메인 실행 파일)
- USER_GUIDE.md (사용자 가이드)
- INSTALLATION.md (설치 가이드)
- TROUBLESHOOTING.md (트러블슈팅)

## 참고사항

Phase 3에서 이미 생성된 문서와 중복되지 않도록:
- README.md: 간단한 소개 및 기능 설명
- BUILD.md: 개발자용 빌드 가이드
- USER_GUIDE.md: 최종 사용자용 상세 가이드 (Phase 6에서 작성)
- INSTALLATION.md: 최종 사용자용 설치/실행 가이드 (Phase 6에서 작성)
- TROUBLESHOOTING.md: 문제 해결 가이드 (Phase 6에서 작성)
