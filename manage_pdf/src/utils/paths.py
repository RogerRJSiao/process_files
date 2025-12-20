from pathlib import Path
import sys

def base_path() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent

#--專案根目錄
BASE_DIR = base_path()
#--內部資源目錄
SRC_DIR = BASE_DIR / "src"
#--外部資源目錄
RESOURCES_DIR = BASE_DIR / ".." / "resources"

#--UI文件路徑
UI_DIR = RESOURCES_DIR / "ui"
UI_MAIN = UI_DIR / "pdf_main.ui"
UI_MERGE = UI_DIR / "pdf_merge.ui"

#--設定來源與目標檔案夾Desktop路徑
HOME_DIR = Path.home()
DESKTOP_DIR = HOME_DIR / "Desktop"
PDF_MERGE_BASE_DIR = DESKTOP_DIR / "pdf_merge"