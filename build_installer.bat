@echo off

REM 배치 파일이 있는 디렉토리로 이동
cd /d %~dp0

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
echo 이 파일을 사용자에게 배포하세요!
echo.
pause
