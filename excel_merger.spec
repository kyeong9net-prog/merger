# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Excel Merger Tool

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.cell.cell',
        'openpyxl.worksheet',
        'openpyxl.worksheet.worksheet',
        'openpyxl.workbook',
        'openpyxl.workbook.workbook',
        'openpyxl.styles',
        'openpyxl.styles.stylesheet',
        'openpyxl.xml.functions',
        'openpyxl.utils',
        'openpyxl.utils.cell',
        'et_xmlfile',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'PIL',
        'PyQt5',
        'scipy',
        'setuptools',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ExcelMerger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 콘솔 창 숨김 (GUI 모드)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',  # 아이콘 파일이 있다면 주석 해제
)
