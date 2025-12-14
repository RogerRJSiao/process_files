import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from controllers.main_controller import MainController
import utils.paths as paths

def main():
    app = QApplication(sys.argv)

    #--載入主視窗UI
    loader = QUiLoader()
    main_ui = loader.load(str(paths.UI_MAIN), None)
    #--建立主視窗Controller
    controller = MainController(main_ui)
    #--將controller綁定到main_ui
    #--避免被回收Python GC回收，確保controller生命週期與main_ui相同
    main_ui.controller = controller

    #--顯示主視窗
    main_ui.show()

    #--啟動Qt事件迴圈
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
