@echo off
REM Excel Merger Tool - Windows Build Script
REM Phase 3: .exe 파일 생성

echo ========================================
echo Excel Merger Tool - Build Script
echo ========================================
echo.

REM Step 1: 이전 빌드 파일 정리
echo [1/4] Cleaning previous build files...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
echo Done.
echo.

REM Step 2: PyInstaller 설치 확인
echo [2/4] Checking PyInstaller installation...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install -r requirements.txt
) else (
    echo PyInstaller is already installed.
)
echo.

REM Step 3: .exe 파일 빌드
echo [3/4] Building .exe file with PyInstaller...
python -m PyInstaller excel_merger.spec
if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo Done.
echo.

REM Step 4: 결과 확인
echo [4/4] Build completed successfully!
echo.
echo Output file: dist\ExcelMerger.exe
if exist dist\ExcelMerger.exe (
    for %%A in (dist\ExcelMerger.exe) do echo File size: %%~zA bytes
) else (
    echo [WARNING] ExcelMerger.exe not found in dist folder!
)
echo.

echo ========================================
echo Build process finished!
echo ========================================
pause
