#!/usr/bin/env bash
"""
PDF Manager 部署腳本
用於自動化部署到不同環境
"""

set -e  # 遇到錯誤立即退出

echo "PDF Manager 部署腳本"
echo "===================="

# 檢查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 檢查必要依賴模組
echo "檢查依賴模組..."
python3 -c "import PySide6, pypdf, fitz; print('所有依賴已安裝')"

# 運行測試（如果有的話）
echo "運行基本測試..."
python3 -c "
import sys
sys.path.insert(0, 'src')
try:
    from models.pdf_model import PDFModel
    model = PDFModel()
    print('Model 載入成功')
except Exception as e:
    print(f'Model 載入失敗: {e}')
    exit(1)
"

# 打包應用程式
echo "打包應用程式..."
cd deploy
python3 build_exe.py

# 檢查打包結果
if [ -d "dist" ] && [ "$(ls -A dist)" ]; then
    echo "打包成功！"
    ls -la dist/
else
    echo "打包失敗！"
    exit 1
fi

echo "部署完成！"