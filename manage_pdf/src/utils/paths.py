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

# 資料夾路徑
DIR_SRC = BASE_DIR / "file_src"
DIR_DEST = BASE_DIR / "file_dest"
