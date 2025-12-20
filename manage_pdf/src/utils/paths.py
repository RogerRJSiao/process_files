from pathlib import Path
import sys

def base_path() -> Path:
    if getattr(sys, 'frozen', False):
        #--打包環境：返回exe所在目錄
        return Path(sys._MEIPASS)
    else:
        #--開發環境：找到專案根目錄（包含src和resources的目錄）
        current = Path(__file__).resolve().parent
        # 向上查找直到找到resources目錄
        while current.parent != current:  # 避免無限循環
            if (current / "resources").exists() and (current / "src").exists():
                return current
            current = current.parent
        #--如果沒找到，返回src的父目錄（備用方案）
        return Path(__file__).resolve().parent.parent

#--專案根目錄
BASE_DIR = base_path()
#--內部資源目錄
SRC_DIR = BASE_DIR / "src"
#--外部資源目錄 (打包時resources在exe同一階目錄，打包前在專案根目錄)
if getattr(sys, 'frozen', False):
    #--打包環境：resources在exe同級目錄
    RESOURCES_DIR = BASE_DIR / "resources"
else:
    #--開發環境：resources在專案根目錄
    RESOURCES_DIR = BASE_DIR / "resources"

#--UI文件路徑
UI_DIR = RESOURCES_DIR / "ui"
UI_MAIN = UI_DIR / "pdf_main.ui"
UI_MERGE = UI_DIR / "pdf_merge.ui"

#--設定來源與目標檔案夾Desktop路徑
HOME_DIR = Path.home()
DESKTOP_DIR = HOME_DIR / "Desktop"
PDF_MERGE_BASE_DIR = DESKTOP_DIR / "pdf_merge"