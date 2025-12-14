@echo off

REM Move to the directory where the batch file is located
cd /d %~dp0

echo ====================================
echo Excel Merger Installer Build
echo ====================================
echo.

REM Step 1: Build .exe file
echo [1/3] Building ExcelMerger.exe...
call build.bat
if errorlevel 1 (
    echo ERROR: .exe build failed
    pause
    exit /b 1
)
echo.

REM Step 2: Check dist\ExcelMerger.exe
echo [2/3] Checking build output...
if not exist "dist\ExcelMerger.exe" (
    echo ERROR: dist\ExcelMerger.exe not found
    pause
    exit /b 1
)
echo OK: dist\ExcelMerger.exe created
echo.

REM Step 3: Build installer with Inno Setup
echo [3/3] Building installer...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
if errorlevel 1 (
    echo ERROR: Installer build failed
    echo.
    echo Please install Inno Setup from:
    echo https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)
echo.

echo ====================================
echo Installer build completed!
echo ====================================
echo.
echo Output file:
echo   installer_output\ExcelMerger_Setup.exe
echo.
echo File size: approximately 20-30MB
echo.
echo You can now distribute this file!
echo.
pause
