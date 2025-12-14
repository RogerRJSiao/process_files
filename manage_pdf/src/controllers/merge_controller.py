from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialogButtonBox

class MergeController:
    def __init__(self, merge_ui):
        self.merge_ui = merge_ui

        #--連接瀏覽按鈕
        for i in range(1, 11):
            btn = getattr(self.merge_ui, f'merge_btn_{i}')
            edit = getattr(self.merge_ui, f'merge_edit_{i}')
            btn.clicked.connect(lambda checked, e=edit: self.browse_file(e))
        
        #--連接btn觸發監聽，同時避免視窗自動被關閉
        #--不只是：不可使用accepted (預設關閉對話框)，改用clicked (自己控制何時關閉)
        #--主要因為：QDialogButtonBox 按鈕判斷是 AcceptRole 自動呼叫 QDialog.accept()，
        #--所以才需要先用 disconnect() 移除預設行為，再改用自訂 click 函式。(C++ Qt 的設計)
        ok_btn = self.merge_ui.merge_btn.button(QDialogButtonBox.Ok)
        ok_btn.clicked.disconnect()
        ok_btn.clicked.connect(self.on_confirm)

    def browse_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self.merge_ui, "選取PDF檔案", "", "PDF Files (*.pdf)")
        if file_path:
            line_edit.setText(file_path)
    
    def on_confirm(self):
        #--取得使用者輸入的值
        list_files = []
        for i in range(1, 11):  
            edit = getattr(self.merge_ui, f'merge_edit_{i}')
            path = edit.text().strip()
            if path:
                list_files.append(path)
        print(f"Merge Function: list_files={list_files}")
        if not list_files:
            QMessageBox.critical(self.merge_ui, "錯誤 ERROR", "請至少選取一個檔案")
            return

        #--執行合併與轉換邏輯 todo            
        