from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QMessageBox, QDialogButtonBox
from PySide6.QtCore import Qt
import utils.paths as paths
from controllers.merge_controller import MergeController

class MainController:
    def __init__(self, main_ui):
        self.main_ui = main_ui
        #--副程式UI與控制器
        self.merge_ui = None
        self.merge_controller = None
        
        #--連接btn觸發監聽，同時避免視窗自動被關閉
        #--不只是：不可使用accepted (預設關閉對話框)，改用clicked (自己控制何時關閉)
        #--self.main_ui.merge_btn.clicked.connect(self.on_confirm)
        #--主要因為：QDialogButtonBox 按鈕判斷是 AcceptRole 自動呼叫 QDialog.accept()，
        #--所以才需要先用 disconnect() 移除預設行為，再改用自訂 click 函式。(C++ Qt 的設計)
        ok_btn = self.main_ui.main_btn.button(QDialogButtonBox.Ok)
        ok_btn.clicked.disconnect()
        ok_btn.clicked.connect(self.on_confirm)

    def on_confirm(self):
        #--取得下拉選單選取的值
        selected = self.main_ui.main_cbx01.currentText()
        match selected:
            case "請選擇":
                msg_clicked = "您未選取任何功能!!(請重選)"
                QMessageBox.critical(self.main_ui, "錯誤 ERROR", msg_clicked)
                return
                
            case "PDF合併":
                msg_clicked = f"您選擇的是【{selected}】功能"
                QMessageBox.information(self.main_ui, "訊息", msg_clicked)
                #--開啟PDF合併視窗
                self.open_merge_ui()
            
    def open_merge_ui(self):
        #--載入PDF合併視窗UI
        loader = QUiLoader()
        self.merge_ui = loader.load(str(paths.UI_MERGE), None)  #--獨立視窗開啟
        #--將merge_controller綁定到merge_ui
        #--避免被回收Python GC回收，確保merge_controller生命週期與merge_ui相同
        self.merge_controller = MergeController(self.merge_ui)
        #--顯示PDF合併視窗
        self.merge_ui.show()