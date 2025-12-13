# 빌드 가이드 (Build Guide)

개발자를 위한 .exe 파일 빌드 가이드입니다.

## 빌드 환경

### 필수 요구사항

- **운영체제**: Windows 10 이상 (Windows에서만 .exe 빌드 가능)
- **Python**: 3.9 이상
- **Git**: 최신 버전

### 의존성 설치

```bash
pip install -r requirements.txt
```

**설치되는 패키지**:
- openpyxl (엑셀 처리)
- pyinstaller (실행 파일 생성)
- flake8 (코드 품질 검사)
- mypy (타입 체크)

## 빌드 방법

### Windows에서 빌드

#### 방법 1: 빌드 스크립트 사용 (권장)

```cmd
build.bat
```

빌드 스크립트가 자동으로:
1. 이전 빌드 파일 정리
2. PyInstaller 설치 확인
3. .exe 파일 생성
4. 결과 확인

#### 방법 2: 수동 빌드

```cmd
# 1. 이전 빌드 정리
rmdir /s /q dist build

# 2. PyInstaller 실행
python -m PyInstaller excel_merger.spec

# 3. 결과 확인
dir dist\ExcelMerger.exe
```

### Linux/Mac에서 빌드 (참고용)

Linux/Mac에서는 Windows .exe 파일을 빌드할 수 없습니다.
대신 해당 플랫폼용 실행 파일을 생성할 수 있습니다:

```bash
chmod +x build.sh
./build.sh
```

## 빌드 설정

### PyInstaller Spec 파일 (`excel_merger.spec`)

주요 설정:

```python
# 콘솔 숨김 (GUI 모드)
console=False

# UPX 압축 활성화 (파일 크기 감소)
upx=True

# 불필요한 패키지 제외
excludes=[
    'matplotlib', 'numpy', 'pandas',
    'PIL', 'PyQt5', 'scipy', 'setuptools'
]
```

### 아이콘 추가 (선택사항)

1. `icon.ico` 파일을 프로젝트 루트에 추가
2. `excel_merger.spec` 파일 수정:

```python
exe = EXE(
    # ...
    icon='icon.ico',  # 주석 해제
)
```

3. 다시 빌드

## 빌드 결과

### 출력 파일

- **위치**: `dist/ExcelMerger.exe`
- **예상 크기**: 20-40 MB (압축 시)
- **형식**: Windows 실행 파일 (.exe)

### 실행 파일 특징

- ✅ **단독 실행**: 별도 Python 설치 불필요
- ✅ **단일 파일**: 모든 의존성 포함
- ✅ **콘솔 숨김**: GUI 모드로 실행
- ✅ **Windows 10 이상 지원**

## 코드 품질 검사

빌드 전 코드 품질 확인:

```bash
# Lint 검사
python -m flake8 src/

# 타입 체크
python -m mypy src/
```

모든 검사를 통과해야 안정적인 .exe 파일을 생성할 수 있습니다.

## 문제 해결

### Q: "Cannot find module" 오류

**A**: 숨겨진 import를 `excel_merger.spec`의 `hiddenimports`에 추가:

```python
hiddenimports=[
    'openpyxl',
    'your_missing_module',
],
```

### Q: .exe 파일이 너무 큼

**A**:
1. UPX 압축 활성화 확인
2. 불필요한 패키지를 `excludes`에 추가
3. PyInstaller 옵션 최적화

### Q: .exe 파일이 실행되지 않음

**A**:
1. Windows Defender/백신 프로그램 예외 추가
2. 관리자 권한으로 실행
3. 로그 확인 (console=True로 변경 후 재빌드)

### Q: tkinter 관련 오류

**A**: Python이 tkinter와 함께 설치되었는지 확인:

```bash
python -m tkinter
```

## 배포

### 배포 전 체크리스트

- [ ] 코드 품질 검사 통과 (flake8, mypy)
- [ ] .exe 파일 정상 빌드
- [ ] Windows에서 실행 테스트
- [ ] 파일 크기 확인 (50MB 이하 권장)
- [ ] README.md 업데이트
- [ ] CHANGELOG.md 작성

### 배포 방법

1. `dist/ExcelMerger.exe` 파일 복사
2. README.md와 함께 배포
3. 사용자에게 사용법 안내

## 개발 환경

### 프로젝트 구조

```
merger/
├── src/
│   ├── __init__.py
│   ├── main.py           # 진입점
│   ├── file_selector.py  # 파일 선택
│   ├── excel_reader.py   # 엑셀 읽기
│   ├── header_validator.py # 헤더 검증
│   ├── excel_merger.py   # 병합 로직
│   ├── file_writer.py    # 파일 저장
│   └── logger.py         # 로깅
├── excel_merger.spec     # PyInstaller 설정
├── build.bat             # Windows 빌드 스크립트
├── build.sh              # Linux/Mac 빌드 스크립트
├── requirements.txt
├── README.md
└── BUILD.md              # 이 파일
```

### 코드 스타일

- **Linter**: flake8
- **Type Checker**: mypy
- **Line Length**: 100자
- **원칙**: SOLID 원칙 준수

## 참고 자료

- [PyInstaller 공식 문서](https://pyinstaller.org/)
- [openpyxl 공식 문서](https://openpyxl.readthedocs.io/)
- [Python tkinter 가이드](https://docs.python.org/3/library/tkinter.html)
