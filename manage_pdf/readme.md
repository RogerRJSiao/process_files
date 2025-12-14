# PDF Manager with PySide6 GUI

## 概述 📖

這個專案構想是，實作簡單的 PDF 文書工具，使用 PySide6 框架建立圖形用戶介面 (GUI)。從原本的單一腳本執行方式 (`pdf_combine.py` 和 `pdf_A4_to_A3.py`)，重構既有程式，並建立 MVC 框架，實現 PDF 檔案的選取、合併和轉換。

## PDF 合併檔案功能 📄

1. **選取 PDF 檔案**：使用者可以在 GUI 上選擇多個 PDF 檔案（支援最多 10 個）。
2. **輸入檔案到暫存資料夾**：將選取的檔案自動複製到 `file_src` 資料夾，並重命名為 `a.pdf`、`b.pdf` 等，以符合合併邏輯。
3. **合併並轉換 PDF**：將 A4 PDF 檔案合併成一個檔案，然後轉換為 A3 格式（每兩頁 A4 放在一頁 A3 上）。
4. **下載合併後的 PDF**：提供按鈕來打開合併後的 A3 PDF 檔案。
   ### 注意事項

   - 支援最多 10 個 PDF 檔案。
   - 確保輸入的 PDF 是 A4 格式，以正確轉換為 A3。
   - 合併後的檔案會儲存在 `file_dest/combined_a3.pdf`。


## 安裝或擴充 📦

專案開發時，請確保 PC 有安裝好以下 Python 套件：

```bash
pip install PySide6 pypdf PyMuPDF
```
- **PySide6**：用於創建 GUI 界面。
- **pypdf**：用於 PDF 檔案的讀取和寫入。
- **PyMuPDF**：用於 PDF 格式轉換（A4 到 A3）。

## MVC 架構 🏗️

為提高代碼的可維護性與擴展性，採用 MVC (Model-View-Controller) 架構來建構/重構這個專案
- View：以 PySide6 (C:\Python313\Lib\site-packages\PySide6\designer.exe) 建立的 .ui 文件，定義用戶介面，並用 QUiLoader 動態載入。雖然 .ui 文件可轉換成 .py，但考慮設計異動頻繁，不建議使用指令轉換成 .py。
- Controller：主畫面的程式規則在 main_controller.py，根據使用者選單挑出的功能，分流至各別的 xxx_controller.py，負責溝通 View 前端資料渲染、Model 後端資料調用。
- Model：目前業務規則放在 pdf_combine.py 和 pdf_A4_to_A3.py，負責 PDF 合併、轉換和檔案管理，但仍尚待封裝成 Class、Model。

## 原始碼檔案結構 📂

```
project/
├─ src/                          #--內部資源--#
│   ├─ main.py                   # 應用程式入口
│   ├─ controllers/              #--Controller--#
│   │   ├─ main_controller.py
|   |   └─ merge_controller.py
│   └─ utils/                    #--工具函數--#
│       └─ paths.py              # 全域路徑定義
├─ resources/                    #--外部資源--#
│   └─ ui/                       #--View--#
│       ├─ pdf_main.ui           # PDF主視窗UI
│       └─ pdf_merge.ui          # PDF合併視窗UI
├─ file_src/                     # 暫存輸入檔案的資料夾
├─ file_dest/                    # 輸出合併和轉換後檔案的資料夾
├─ pdf_combine.py                # (todo) model-業務規則-PDF合併邏輯
├─ pdf_A4_to_A3.py               # (todo) model-業務規則-PDF格式轉換邏輯
├─ deploy/                       #--自動化部署--#
└─ readme.md                     #--專案說明(本文內容)--#
```

## 技術新里程 🚀

1. **選用 Python GUI 套件種類**：在開發過程時，最終選擇 PySide6 作為 GUI 框架，因為它提供了現代化的 Qt 介面元件，而且具有良好的跨平台支援和豐富的功能。相較於 Python 內建的 Tkinter，根據資料顯示 PySide6 提供了方便的佈局方式和 UX，同時允許用在商用產品的開發。

2. **調整 QDialogButtonBox 按鈕行為控制**：在 PySide6 中，QDialogButtonBox 的 Ok (確定) 按鈕預設會自動關閉對話框（呼叫 accept()）。為避免此行為，使用 disconnect() 移除預設連接，再用 clicked.connect() 自訂處理函式，確保視窗控制權在使用者手中，避免意外關閉。 

3. **理解 Controller 生命週期管理**：在 Python 中，物件可能被垃圾回收器 (GC) 提前清理。將 merge_controller 綁定到 merge_ui 作為實例變數，確保其生命週期與 UI 視窗一致，避免控制器在視窗關閉前被回收，出現類似閃退的不良 UX，維持 GUI 介面上事件處理的穩定性。


## 閱讀資源 🔗
- [[Python 練習筆記] PySide6 做一個簡單的GUI Application](https://medium.com/@benson890720/python%E7%B7%B4%E7%BF%92%E7%AD%86%E8%A8%98-pyside6%E5%81%9A%E4%B8%80%E5%80%8B%E7%B0%A1%E5%96%AE%E7%9A%84gui-application-0-%E7%B0%A1%E4%BB%8B%E8%88%87%E8%A8%AD%E5%AE%9A-96c982d8f90)
- [Qt for Python](https://doc.qt.io/qtforpython-6/index.html)
