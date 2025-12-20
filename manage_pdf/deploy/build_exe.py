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
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已刪除 {dir_name} 目錄")

def install_dependencies():
    """安裝必要的依賴"""
    print("安裝專案依賴...")
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
    """使用PyInstaller打包exe"""
    print("開始打包exe文件...")

    # 當前已在deploy目錄中，專案根目錄是父目錄
    project_root = Path(__file__).parent.parent
    deploy_dir = Path(__file__).parent

    # 使用絕對路徑的spec文件進行打包
    spec_file = deploy_dir / "pdf_manager.spec"
    if not spec_file.exists():
        print(f"錯誤: {spec_file} 文件不存在")
        sys.exit(1)

    # 在deploy目錄中運行pyinstaller
    cmd = f'pyinstaller --clean "{spec_file}"'
    print(f"執行命令: {cmd}")
    run_command(cmd, cwd=deploy_dir)

    print("exe文件打包完成！")

def create_installer():
    """創建安裝包（可選）"""
    print("創建安裝包...")

    # 檢查是否有NSIS或其他安裝包工具
    dist_dir = Path("dist")
    if dist_dir.exists():
        # 創建zip包作為簡單的安裝包
        import zipfile

        exe_files = list(dist_dir.glob("*.exe"))
        if exe_files:
            zip_name = f"PDFManager_v1.0.0.zip"
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for exe_file in exe_files:
                    zipf.write(exe_file, exe_file.name)
                # 添加README或其他文件
                readme = Path("../README.md")
                if readme.exists():
                    zipf.write(readme, "README.md")

            print(f"安裝包已創建: {zip_name}")

def main():
    """主函數"""
    print("PDF Manager 打包工具")
    print("=" * 40)

    # 確保在deploy目錄中運行
    if not os.path.exists("pdf_manager.spec"):
        print("錯誤: 請在deploy目錄中運行此腳本")
        sys.exit(1)

    try:
        clean_build_dirs()
        install_dependencies()
        build_exe()
        create_installer()

        print("\n打包完成！")
        print("可執行文件位於 dist/ 目錄中")

        # 顯示文件大小
        dist_dir = Path("dist")
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("*.exe"))
            for exe_file in exe_files:
                size_mb = exe_file.stat().st_size / (1024 * 1024)
                print(f"生成的文件: {exe_file.name} ({size_mb:.2f} MB)")
    except Exception as e:
        print(f"\n打包失敗: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()