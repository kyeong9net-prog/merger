# 인스톨러 제작 가이드

## 개요
이 문서는 Excel Merger의 **설치 프로그램 (ExcelMerger_Setup.exe)**을 만드는 방법을 설명합니다.

---

## 배포 옵션 비교

### 옵션 1: 단순 배포 (현재 방식)
```
사용자가 받는 파일: ExcelMerger.exe (1개)
장점:
  ✅ 간단하고 빠름
  ✅ 다운로드 즉시 실행
  ✅ 추가 도구 불필요
단점:
  ❌ 시작 메뉴 등록 안됨
  ❌ 제거 프로그램에 안나타남
```

### 옵션 2: 인스톨러 배포 (전문적)
```
사용자가 받는 파일: ExcelMerger_Setup.exe (1개)
장점:
  ✅ 시작 메뉴에 자동 등록
  ✅ 바탕화면 바로가기 생성
  ✅ 제거 프로그램에서 삭제 가능
  ✅ 전문적인 느낌
단점:
  ❌ 인스톨러 제작 필요
  ❌ Inno Setup 설치 필요
```

---

## 1. Inno Setup 설치

### 다운로드
1. 공식 사이트 방문: https://jrsoftware.org/isdl.php
2. **Inno Setup 6.x** 다운로드 (무료)
3. 설치 진행 (기본 설정으로)

### 설치 확인
```
Inno Setup Compiler가 설치되었는지 확인
경로: C:\Program Files (x86)\Inno Setup 6\ISCC.exe
```

---

## 2. 인스톨러 빌드 절차

### 전제 조건
먼저 `ExcelMerger.exe`를 빌드해야 합니다:
```bash
# 1. .exe 파일 빌드
build.bat

# 2. 빌드 결과 확인
dir dist\ExcelMerger.exe
```

### 인스톨러 제작

#### 방법 1: GUI 사용 (쉬움)
```
1. Inno Setup Compiler 실행
2. File > Open > installer.iss 선택
3. Build > Compile 클릭
4. 완료되면 installer_output\ExcelMerger_Setup.exe 생성됨
```

#### 방법 2: 명령줄 사용 (자동화)
```bash
# Windows PowerShell 또는 CMD
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

#### 방법 3: 빌드 스크립트 사용 (권장)
`build_installer.bat` 파일 사용:
```bash
build_installer.bat
```

---

## 3. 빌드 스크립트 (자동화)

### build_installer.bat
```batch
@echo off
echo ====================================
echo Excel Merger 인스톨러 빌드
echo ====================================
echo.

REM Step 1: .exe 파일 빌드
echo [1/3] ExcelMerger.exe 빌드 중...
call build.bat
if errorlevel 1 (
    echo 오류: .exe 빌드 실패
    pause
    exit /b 1
)
echo.

REM Step 2: dist\ExcelMerger.exe 확인
echo [2/3] 빌드된 파일 확인 중...
if not exist "dist\ExcelMerger.exe" (
    echo 오류: dist\ExcelMerger.exe가 없습니다
    pause
    exit /b 1
)
echo ✓ dist\ExcelMerger.exe 확인 완료
echo.

REM Step 3: Inno Setup으로 인스톨러 빌드
echo [3/3] 인스톨러 빌드 중...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
if errorlevel 1 (
    echo 오류: 인스톨러 빌드 실패
    echo.
    echo Inno Setup이 설치되어 있는지 확인하세요:
    echo https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)
echo.

echo ====================================
echo ✓ 인스톨러 빌드 완료!
echo ====================================
echo.
echo 생성된 파일:
echo   installer_output\ExcelMerger_Setup.exe
echo.
echo 파일 크기: 약 20-30MB
echo.
pause
```

---

## 4. 빌드 결과 확인

### 생성되는 파일
```
installer_output/
└── ExcelMerger_Setup.exe  (약 20-30MB)
```

### 테스트 방법
```
1. ExcelMerger_Setup.exe 실행
2. 설치 진행
3. 시작 메뉴에서 "Excel Merger" 확인
4. 프로그램 실행 테스트
5. 제어판 > 프로그램 제거에서 "Excel Merger" 확인
6. 제거 테스트
```

---

## 5. 인스톨러 기능

### 설치 시
- ✅ 프로그램 파일 복사 (`C:\Program Files\ExcelMerger\`)
- ✅ 시작 메뉴에 "Excel Merger" 폴더 생성
- ✅ 바탕화면 바로가기 생성 (선택 옵션)
- ✅ 문서 파일 복사 (사용자 가이드 등)
- ✅ 제거 프로그램 등록

### 시작 메뉴 항목
```
시작 > Excel Merger >
  ├── Excel Merger (프로그램 실행)
  ├── 사용자 가이드
  ├── 문제 해결
  └── Uninstall Excel Merger
```

### 제거 시
- ✅ 프로그램 파일 삭제
- ✅ 시작 메뉴 항목 삭제
- ✅ 바탕화면 바로가기 삭제
- ✅ 제거 프로그램 등록 해제

---

## 6. 사용자 배포 방법

### 배포할 파일
```
ExcelMerger_Setup.exe
```
단 1개 파일만 배포하면 됩니다!

### 사용자 사용법
```
1. ExcelMerger_Setup.exe 다운로드
2. 더블클릭하여 실행
3. 설치 마법사 진행
4. 시작 메뉴에서 "Excel Merger" 실행
```

### 배포 채널
- 이메일 첨부
- 클라우드 스토리지 (Google Drive, Dropbox 등)
- GitHub Releases
- 회사 내부 공유 폴더

---

## 7. 문제 해결

### 오류: "ISCC.exe를 찾을 수 없습니다"
```
해결: Inno Setup 설치 경로 확인
기본 경로: C:\Program Files (x86)\Inno Setup 6\ISCC.exe

설치 안되어 있으면:
https://jrsoftware.org/isdl.php 에서 다운로드
```

### 오류: "dist\ExcelMerger.exe가 없습니다"
```
해결: 먼저 .exe 파일 빌드
> build.bat
```

### 바이러스 경고 발생
```
해결: ANTIVIRUS_CHECK.md 참고
- VirusTotal로 검증
- Windows Defender 예외 추가
- 필요시 코드 서명 (선택사항)
```

---

## 8. 고급 옵션 (선택사항)

### 아이콘 커스터마이징
```
1. icon.ico 파일 준비 (256x256 권장)
2. installer.iss에서 아이콘 경로 설정 확인:
   SetupIconFile=icon.ico
```

### 코드 서명 (디지털 서명)
```
1. 코드 서명 인증서 구매
2. SignTool.exe 사용
3. installer.iss에 서명 명령 추가:
   SignTool=signtool.exe sign /f mycert.pfx /p password $f
```

### 라이센스 추가
```
1. LICENSE.txt 파일 생성
2. installer.iss에 추가:
   LicenseFile=LICENSE.txt
```

---

## 요약

### 빠른 시작
```bash
# Windows에서 실행
build_installer.bat
```

### 배포 파일
```
installer_output\ExcelMerger_Setup.exe
```

### 사용자가 하는 일
```
1. Setup.exe 더블클릭
2. 설치 진행
3. 시작 메뉴에서 실행
```

**이제 전문적인 설치 프로그램으로 배포할 수 있습니다!** 🎉
