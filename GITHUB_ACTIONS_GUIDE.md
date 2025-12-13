# GitHub Actions 자동 빌드 가이드

## 개요
GitHub에 코드를 푸시하면 **자동으로 Windows에서 빌드**되어 **배포 파일이 생성**됩니다!

---

## 🚀 사용 방법

### 방법 1: Release 태그로 자동 빌드 (권장)

```bash
# 1. 모든 변경사항 커밋
git add -A
git commit -m "Release v1.0.0"

# 2. 태그 생성
git tag v1.0.0

# 3. 푸시 (태그 포함)
git push origin claude/update-spec-checkboxes-01LkcCU2sCGnFjSF65paeQgw
git push origin v1.0.0

# 또는 한 번에
git push origin claude/update-spec-checkboxes-01LkcCU2sCGnFjSF65paeQgw --tags
```

### 방법 2: 수동 실행

1. GitHub 저장소 접속
2. **Actions** 탭 클릭
3. **Build and Release** 워크플로우 선택
4. **Run workflow** 버튼 클릭
5. 브랜치 선택 후 실행

---

## 📦 빌드 결과 확인

### 자동 빌드가 완료되면:

#### 1. Artifacts (수동 실행 시)
- **Actions** > 해당 워크플로우 클릭
- **Artifacts** 섹션에서 다운로드:
  - `ExcelMerger-exe`: ExcelMerger.exe
  - `ExcelMerger-Setup`: ExcelMerger_Setup.exe

#### 2. Releases (태그 푸시 시)
- **Releases** 탭 클릭
- 최신 Release에서 다운로드:
  - ExcelMerger.exe
  - ExcelMerger_Setup.exe

---

## 🔧 워크플로우 동작

### 자동으로 수행되는 작업:

```
1. Windows 환경 준비
2. Python 3.11 설치
3. 의존성 설치 (requirements.txt)
4. PyInstaller로 .exe 빌드
5. Inno Setup 설치
6. 인스톨러 빌드
7. 파일 업로드
8. Release 생성 (태그 푸시 시)
```

### 빌드 시간
약 **5-10분** 소요

---

## 📊 GitHub Actions 확인

### 빌드 상태 확인
1. GitHub 저장소 > **Actions** 탭
2. 최신 워크플로우 실행 클릭
3. 각 단계별 로그 확인

### 빌드 성공 시
- ✅ 녹색 체크 표시
- Artifacts에 파일 업로드됨

### 빌드 실패 시
- ❌ 빨간 X 표시
- 로그에서 오류 확인 가능

---

## 🎯 버전 관리

### 버전 번호 규칙

```
v1.0.0 - 최초 릴리스
v1.0.1 - 버그 수정
v1.1.0 - 기능 추가
v2.0.0 - 주요 변경
```

### 새 버전 배포

```bash
# 코드 수정 후
git add -A
git commit -m "Fix: 버그 수정"

# 새 버전 태그
git tag v1.0.1

# 푸시
git push origin claude/update-spec-checkboxes-01LkcCU2sCGnFjSF65paeQgw --tags
```

자동으로 v1.0.1 Release가 생성됩니다!

---

## 💡 사용자 배포 방법

### GitHub Release 링크 공유

```
사용자에게 전달:
https://github.com/kyeong9net-prog/merger/releases/latest

사용자가 할 일:
1. 위 링크 접속
2. ExcelMerger_Setup.exe 다운로드
3. 더블클릭하여 설치
4. 끝!
```

---

## 🔐 주의사항

### 1. GitHub Repository가 Public이어야 합니다
Private 저장소는 GitHub Actions 사용 시간 제한이 있습니다.

### 2. GITHUB_TOKEN
- 자동으로 제공되므로 별도 설정 불필요
- Release 생성 권한 포함

### 3. 빌드 실패 시
- Actions 탭에서 로그 확인
- 오류 메시지 확인 후 수정
- 다시 푸시하면 자동 재빌드

---

## 📝 워크플로우 파일

`.github/workflows/build-release.yml` 파일이 자동 빌드를 담당합니다.

### 수정 가능한 설정:
- Python 버전 (현재: 3.11)
- 빌드 조건 (현재: v* 태그)
- Release 설명 내용

---

## 🎉 장점

### ✅ 개발자
- Windows PC 없이도 빌드 가능
- 수동 빌드 과정 생략
- 버전 관리 자동화
- 빌드 히스토리 보관

### ✅ 사용자
- 항상 최신 버전 다운로드 가능
- 신뢰할 수 있는 빌드 환경
- 다운로드 링크 하나로 간편하게

---

## 🚀 빠른 시작

```bash
# 1. GitHub에 푸시
git push origin claude/update-spec-checkboxes-01LkcCU2sCGnFjSF65paeQgw

# 2. 릴리스 태그 생성 및 푸시
git tag v1.0.0
git push origin v1.0.0

# 3. GitHub > Releases 에서 다운로드!
```

**이제 Windows PC 없이도 배포 파일을 만들 수 있습니다!** 🎊
