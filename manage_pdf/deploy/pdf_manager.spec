# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# 專案根目錄 (deploy目錄的父目錄)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(SPEC)))

# 添加src目錄到路徑
sys.path.insert(0, os.path.join(project_root, 'src'))

a = Analysis(
    [os.path.join(project_root, 'src', 'main.py')],
    pathex=[project_root],
    binaries=[],
    datas=[
        # UI 文件 - 使用Tree包含整個目錄
        (os.path.join(project_root, 'resources'), 'resources'),
    ],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'PySide6.QtUiTools',
        'utils.paths',
        'controllers.main_controller',
        'controllers.merge_controller',
        'models.pdf_model',
        'pypdf',
        'fitz',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='PDFManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不顯示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加圖標文件
)