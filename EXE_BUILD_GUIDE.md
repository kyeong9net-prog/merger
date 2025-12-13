# EXE 파일 생성 및 최적화 가이드

## 개요
이 문서는 Excel Merger를 Windows 실행 파일(.exe)로 빌드하고 최적화하는 방법을 설명합니다.

---

## 1. .exe 파일 생성

### 시스템 요구사항
- **운영체제**: Windows 10 이상
- **Python**: 3.9 이상
- **필수 패키지**: requirements.txt 참조

### 빌드 절차

#### 1단계: 의존성 설치
```bash
pip install -r requirements.txt
```

필수 패키지:
- openpyxl >= 3.1.0
- pyinstaller >= 6.0.0
- pytest >= 7.4.0 (테스트용)

#### 2단계: 테스트 실행 (선택사항)
```bash
python -m pytest tests/ -v
```

모든 테스트가 통과하는지 확인합니다.

#### 3단계: .exe 파일 빌드
```bash
# Windows에서 실행
build.bat
```

또는 직접 PyInstaller 실행:
```bash
pyinstaller excel_merger.spec
```

#### 4단계: 생성된 파일 확인
```bash
dist/ExcelMerger.exe
```

---

## 2. 파일 크기 최적화

### 현재 최적화 설정

`excel_merger.spec` 파일에 이미 적용된 최적화:

#### 2.1 UPX 압축 사용
```python
exe = EXE(
    # ...
    upx=True,  # UPX 압축 활성화
    upx_exclude=[],
    # ...
)
```

**효과**: 실행 파일 크기를 30-50% 감소

#### 2.2 불필요한 패키지 제외
```python
a = Analysis(
    # ...
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'PIL',
        'tkinter.test',
        'test',
        'unittest',
        'distutils',
    ],
    # ...
)
```

**효과**: 불필요한 대용량 라이브러리 제외로 크기 감소

#### 2.3 단일 파일 모드
```python
exe = EXE(
    # ...
    name='ExcelMerger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI 모드 (콘솔 숨김)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

**효과**: 하나의 .exe 파일로 배포 (의존성 내장)

### 추가 최적화 방법

#### 2.4 Python 최적화 모드
build.bat에 이미 포함됨:
```batch
python -O -m PyInstaller excel_merger.spec
```

`-O` 플래그: Python 바이트코드 최적화

#### 2.5 예상 파일 크기
- **최적화 전**: ~50-70 MB
- **최적화 후**: ~20-30 MB

실제 크기는 포함된 라이브러리에 따라 달라질 수 있습니다.

---

## 3. 빌드 스크립트 설명

### build.bat (Windows)

```batch
@echo off
echo ========================================
echo Excel Merger .exe 파일 빌드
echo ========================================
echo.

REM 이전 빌드 정리
echo [1/4] 이전 빌드 파일 정리 중...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo 정리 완료.
echo.

REM PyInstaller 설치 확인
echo [2/4] PyInstaller 설치 확인 중...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller가 설치되어 있지 않습니다. 설치를 시작합니다...
    pip install pyinstaller>=6.0.0
)
echo PyInstaller 확인 완료.
echo.

REM .exe 파일 빌드
echo [3/4] .exe 파일 빌드 중...
python -O -m PyInstaller excel_merger.spec
if errorlevel 1 (
    echo 빌드 실패!
    pause
    exit /b 1
)
echo 빌드 완료.
echo.

REM 결과 확인
echo [4/4] 빌드 결과 확인 중...
if exist "dist\ExcelMerger.exe" (
    echo ========================================
    echo 빌드 성공!
    echo 생성된 파일: dist\ExcelMerger.exe
    echo ========================================
    dir dist\ExcelMerger.exe
) else (
    echo 빌드 실패: dist\ExcelMerger.exe 파일을 찾을 수 없습니다.
    pause
    exit /b 1
)

echo.
pause
```

### 빌드 프로세스
1. **정리**: 이전 build, dist 폴더 삭제
2. **확인**: PyInstaller 설치 확인 및 자동 설치
3. **빌드**: 최적화 모드로 .exe 파일 생성
4. **검증**: 생성된 파일 존재 확인

---

## 4. 빌드 후 검증

### 4.1 실행 테스트
```bash
dist\ExcelMerger.exe
```

프로그램이 정상 실행되는지 확인합니다.

### 4.2 기능 테스트
1. 파일 선택 UI 표시 확인
2. 엑셀 파일 병합 테스트
3. 결과 파일 생성 확인
4. 로그 파일 생성 확인

### 4.3 성능 테스트
- 100개 파일 병합: 5초 이내 완료
- 메모리 사용: 안정적

---

## 5. 문제 해결

### 빌드 실패 시
```bash
# 캐시 정리
rmdir /s /q build
rmdir /s /q dist
rmdir /s /q __pycache__

# 재빌드
build.bat
```

### ImportError 발생 시
`excel_merger.spec`의 `hiddenimports`에 누락된 모듈 추가:
```python
hiddenimports=[
    'openpyxl',
    'openpyxl.cell',
    'openpyxl.workbook',
    # ... 누락된 모듈 추가
]
```

### UPX 압축 오류 시
UPX 압축 비활성화:
```python
exe = EXE(
    # ...
    upx=False,  # UPX 압축 비활성화
    # ...
)
```

---

## 6. 배포 준비

### 배포 파일 목록
```
배포 폴더/
├── ExcelMerger.exe          # 실행 파일
├── USER_GUIDE.md            # 사용자 가이드
├── INSTALLATION.md          # 설치 가이드
└── TROUBLESHOOTING.md       # 문제 해결 가이드
```

### 체크리스트
- [ ] .exe 파일 정상 빌드
- [ ] 실행 테스트 통과
- [ ] 기능 테스트 통과
- [ ] 성능 테스트 통과
- [ ] 파일 크기 확인 (30MB 이하 권장)
- [ ] 문서 포함 확인

---

## 7. 참고사항

### 크로스 플랫폼 빌드
- Windows .exe는 Windows에서만 빌드 가능
- Linux에서는 build.sh를 참고용으로만 사용
- 각 플랫폼별로 별도 빌드 필요

### 코드 서명 (선택사항)
코드 서명을 통해 Windows Defender 오탐 감소:
```bash
# 서명 도구 필요 (별도 인증서 구매)
signtool sign /f certificate.pfx /p password ExcelMerger.exe
```

**Note**: 코드 서명은 Phase 6 범위를 벗어나므로 선택사항입니다.

---

## 8. 버전 관리

### 버전 정보 추가 (선택사항)
`excel_merger.spec`에 버전 정보 추가:
```python
exe = EXE(
    # ...
    version='version.txt',  # 버전 정보 파일
    # ...
)
```

version.txt 예시:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # ...
  ),
  # ...
)
```

---

## 요약

1. **빌드 명령**: `build.bat` 실행
2. **결과 파일**: `dist/ExcelMerger.exe`
3. **최적화**: UPX 압축 + 불필요한 패키지 제외
4. **예상 크기**: 20-30 MB
5. **배포**: .exe + 문서 파일 함께 배포

자세한 빌드 옵션은 BUILD.md를 참조하세요.
