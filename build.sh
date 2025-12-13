#!/bin/bash
# Excel Merger Tool - Linux/Mac Build Script
# Phase 3: 실행 파일 생성 (참고용)
# 주의: Windows .exe 파일은 Windows 환경에서만 빌드 가능

echo "========================================"
echo "Excel Merger Tool - Build Script"
echo "========================================"
echo ""

# Step 1: 이전 빌드 파일 정리
echo "[1/4] Cleaning previous build files..."
rm -rf dist build
echo "Done."
echo ""

# Step 2: PyInstaller 설치 확인
echo "[2/4] Checking PyInstaller installation..."
if ! python3 -m pip show pyinstaller > /dev/null 2>&1; then
    echo "PyInstaller not found. Installing..."
    python3 -m pip install -r requirements.txt
else
    echo "PyInstaller is already installed."
fi
echo ""

# Step 3: 실행 파일 빌드
echo "[3/4] Building executable with PyInstaller..."
echo ""
echo "WARNING: This script is for reference only."
echo "Windows .exe files must be built on Windows."
echo "On Linux/Mac, this will create a Linux/Mac executable."
echo ""
read -p "Continue building for current platform? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 -m PyInstaller excel_merger.spec

    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERROR] Build failed!"
        exit 1
    fi
    echo "Done."
    echo ""

    # Step 4: 결과 확인
    echo "[4/4] Build completed successfully!"
    echo ""

    if [ -f "dist/ExcelMerger" ]; then
        echo "Output file: dist/ExcelMerger"
        echo "File size: $(stat -f%z dist/ExcelMerger 2>/dev/null || stat -c%s dist/ExcelMerger 2>/dev/null) bytes"
    else
        echo "[WARNING] ExcelMerger executable not found in dist folder!"
    fi
    echo ""
else
    echo "Build cancelled."
    exit 0
fi

echo "========================================"
echo "Build process finished!"
echo "========================================"
