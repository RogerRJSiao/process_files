#!/usr/bin/env python3
"""
PDF Manager 打包腳本
使用 PyInstaller 將專案打包成可執行檔案
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """執行命令並返回結果"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"命令執行失敗: {cmd}")
        print(f"錯誤輸出: {e.stderr}")
        raise

def clean_build_dirs():
    """清理build和dist目錄"""
    print("清理舊的build和dist目錄...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):    #--檢查目錄是否存在，或用FileNotFoundError
            shutil.rmtree(dir_name)     #--遞歸刪除目錄，或用PermissionError
            print(f"已刪除 {dir_name} 目錄")

def install_dependencies():
    """安裝必要的依賴模組"""
    print("安裝專案的依賴模組...")
    requirements = [
        'PySide6',
        'pypdf',
        'PyMuPDF',
        'pyinstaller'
    ]

    for package in requirements:
        print(f"安裝 {package}...")
        run_command(f"pip install {package}")

def build_exe():
    """使用PyInstaller打包exe執行檔"""
    print("開始打包exe執行檔...")

    #--當前路徑是在deploy目錄內
    project_root = Path(__file__).parent.parent
    deploy_dir = Path(__file__).parent

    #--指定絕對路徑，打包前確認spec文件存在
    spec_name = "pdf_manager"
    spec_file = deploy_dir / f"{spec_name}.spec"
    if not spec_file.exists():
        print(f"錯誤: {spec_file} 文件不存在")
        sys.exit(1) #--退出程式

    #--清除舊的build快取，在deploy目錄執行PyInstaller
    cmd = f'pyinstaller --clean "{spec_file}"'
    print(f"執行命令: {cmd}")
    run_command(cmd, cwd=deploy_dir)

    print("執行檔exe打包完成！")

def create_installer():
    """建立安裝檔zip"""
    print("建立安裝檔zip...")

    #--使用絕對路徑建立安裝檔
    project_root = Path(__file__).parent.parent
    deploy_dir = Path(__file__).parent
    dist_dir = deploy_dir / "dist"
    if dist_dir.exists():
        #--建立zip安裝檔
        import zipfile
        #--檢查並取得已打包成功的exe檔案
        exe_files = list(dist_dir.glob("*.exe"))
        if exe_files:
            zip_name = f"PDFManager_v1.0.0.zip"
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for exe_file in exe_files:
                    zipf.write(exe_file, exe_file.name)
                #--加入README或其他文件
                readme = project_root / "README.md"
                if readme.exists():
                    zipf.write(readme, "README.md")

            print(f"安裝檔案zip已建立: {zip_name}")

def main():
    """主函式"""
    print("=" * 40)
    print("PDF Manager 打包工具")
    print("=" * 40)

    project_root = Path(__file__).parent.parent
    deploy_dir = Path(__file__).parent

    #--確保在deploy目錄中運行，同時檢查spec文件是否存在
    if not os.path.exists("pdf_manager.spec"):
        print("錯誤: 請在deploy目錄中運行此腳本")
        sys.exit(1) #--退出程式
        
        #--提示是否重建spec文件
        # response = input(f"是否要重建 {spec_name}.spec 文件？ (y/n): ")
        # if response.lower() == 'y':
        #     main_py = project_root / "src" / "main.py"
        #     #--產生spec文件(不包含自訂內容，也不會執行打包)
        #     cmd = f'pyinstaller --name pdf_manager --specpath "{deploy_dir}" --spec-only "{main_py}"'
        #     print(f"產生spec文件: {cmd}")
        #     run_command(cmd, cwd=deploy_dir)
        #     if spec_file.exists():
        #         print("spec已重建")
        #     else:
        #         print("spec重建失敗")
        #         sys.exit(1)
        # else:
        #     sys.exit(1)

    try:
        clean_build_dirs()      #--清理build和dist目錄
        install_dependencies()  #--安裝必要的依賴模組
        build_exe()             #--使用PyInstaller打包exe
        create_installer()      #--建立安裝zip檔
        print("\n打包完成！\n可執行 exe 在 dist/ 目錄")
        print("-" * 40)

        #--檢查並顯示執行檔大小
        dist_dir = deploy_dir / "dist"
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("*.exe"))
            for exe_file in exe_files:
                size_mb = exe_file.stat().st_size / (1024 * 1024)
                print(f"產生檔案: {exe_file.name} ({size_mb:.2f} MB)")
                print("=" * 40)
    except Exception as e:
        print(f"\n打包失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()