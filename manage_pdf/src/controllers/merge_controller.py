from PySide6.QtWidgets import QFileDialog, QMessageBox, QDialogButtonBox
from models.pdf_model import PDFModel
import shutil
import os

class MergeController:
    def __init__(self, merge_ui):
        self.merge_ui = merge_ui
        self.pdf_model = PDFModel()  #--初始化PDF模型

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

    def open_save_dialog(self, src_a3_path, src_a4_path):
        """
        顯示儲存檔案對話框，讓用戶選擇存放位置
        Args:
            src_a3_path: 轉換後A3檔案路徑
            src_a4_path: 合併後A4檔案路徑
        Returns:
            None
        Raises:
            Exception
        """
        #--檢查來源檔案是否存在
        if not os.path.exists(src_a4_path) or not os.path.exists(src_a3_path):
            QMessageBox.critical(self.merge_ui, "錯誤", "來源檔案不存在，無法儲存")
            return
        
        #--從原始檔案路徑，取得預設檔案名
        default_filename_a3 = os.path.basename(src_a3_path)
        default_filename_a4 = os.path.basename(src_a4_path)

        #--顯示儲存檔案對話框
        save_path, _ = QFileDialog.getSaveFileName(
            self.merge_ui, "儲存合併後PDF檔案",
            default_filename_a4, "PDF Files (*.pdf);;All Files (*)"
        )
        if save_path:
            try:
                #--複製檔案到用戶選擇的位置
                shutil.copy2(src_a4_path, save_path)
                shutil.copy2(src_a3_path, save_path.replace('.pdf', '_to_A3.pdf'))
                #--顯示成功訊息
                reply = QMessageBox.question(
                    self.merge_ui,
                    "儲存成功",
                    f"檔案已儲存：\n{save_path}？",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                QMessageBox.information(self.merge_ui, "完成", "儲存成功！")

            except Exception as e:
                QMessageBox.critical(self.merge_ui, "儲存失敗", f"儲存檔案時，發生錯誤：\n{str(e)}")
        else:
            #--用戶取消儲存
            QMessageBox.information(self.merge_ui, "取消", "儲存已取消")
    
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

        #--調用Model執行合併與轉換規則
        success, msg = self.pdf_model.merge_and_convert(list_files)
        if success:
            #--取得已產出的檔案路徑
            file_a3_path = self.pdf_model.get_output_path('A3')
            file_a4_path = self.pdf_model.get_output_path('A4')
            QMessageBox.information(self.merge_ui, "成功", f"A4合併A3轉換完成!\n{file_a3_path}")
            #--選擇下載資料夾路徑
            self.open_save_dialog(file_a3_path, file_a4_path)

        else:
            QMessageBox.critical(self.merge_ui, "錯誤", f"處理不成功: {msg}")            
        