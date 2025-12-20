# PDF Manager 部署指南

## 概述
PDF Manager 是一個用於處理PDF文件的桌面應用程序，支援 PDF 合併、分割、格式轉換等功能。

## 部署選項

### 1. 本地打包 (Windows)
```bash
# 安裝依賴
pip install -r requirements.txt

# 運行打包腳本
cd deploy
python build_exe.py
```

### 2. 本地打包 (Linux/Mac) toCheck
```bash
# 安裝依賴
pip install -r requirements.txt

# 運行打包腳本
cd deploy
python build_exe.py
```

### 3. 自動化部署腳本 toCheck
```bash
# 運行完整部署腳本
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

### 4. CI/CD 自動化 toCheck
推送標籤到GitHub將自動觸發釋出：
```bash
git tag v1.0.0
git push origin v1.0.0
```
## 測試部署腳本

### A. 完整測試流程
```bash
# 進入專案根目錄
cd /path/to/manage_pdf

# 1. 檢查Python版本
python -c "import sys; print('Python版本:', sys.version.split()[0])"

# 2. 檢查依賴模組
python -c "import PySide6, pypdf, fitz; print('✅ 所有依賴已安裝')"

# 3. 運行基本測試
python -c "
import sys
sys.path.insert(0, 'src')
from models.pdf_model import PDFModel
model = PDFModel()
print('✅ Model 載入成功')
"

# 4. 打包應用程式
cd deploy
python build_exe.py

# 5. 檢查打包結果
# Windows:
dir dist
# Linux/Mac:
ls -la dist/
```

### B. 測試 deploy.sh 腳本

#### Windows (PowerShell)
```powershell
# 方法1: 直接使用Python腳本
cd deploy
python build_exe.py

# 方法2: 模擬deploy.sh的完整流程
cd /path/to/manage_pdf
python -c "import sys; print('Python版本:', sys.version.split()[0])"
python -c "import PySide6, pypdf, fitz; print('所有依賴已安裝')"
python -c "import sys; sys.path.insert(0, 'src'); from models.pdf_model import PDFModel; model = PDFModel(); print('Model 載入成功')"
cd deploy && python build_exe.py
Get-ChildItem dist  # 檢查結果
```

#### Linux/Mac (Bash)
```bash
# 完整自動化測試
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

#### Git Bash (Windows)
```bash
# 如果安裝了Git Bash
cd /path/to/manage_pdf
chmod +x deploy/deploy.sh
./deploy/deploy.sh
```

### C. 測試檢查清單

- [ ] Python版本 ≥ 3.8
- [ ] PySide6 模組可導入
- [ ] pypdf 模組可導入
- [ ] fitz (PyMuPDF) 模組可導入
- [ ] PDFModel 類別可實例化
- [ ] build_exe.py 執行無錯誤
- [ ] dist/ 目錄包含可執行文件
- [ ] 可執行文件大小合理 (>50MB)

## 打包輸出
打包後的可執行文件將位於 `deploy/dist/` 目錄中。

## 系統需求
- Python 3.8+
- PySide6
- PyPDF2 或 pypdf
- PyMuPDF (fitz)

## 故障排除
- 如果打包失敗，請確保所有依賴都已正確安裝
- 檢查Python版本是否符合要求
- 查看控制台輸出以獲取詳細錯誤信息