import os
import shutil
from pypdf import PdfReader, PdfWriter
import fitz  # pip install PyMuPDF  # https://pymupdf.readthedocs.io/en/latest/

import utils.paths as paths

# def merge_prfs() 使用範例：
# 將原始的 A4 PDF 檔案合併，以及轉換出另一個 A3 PDF 檔案
# A4 合併前，可善用 Edge 列印功能，移除原檔案不必要的頁面
# 原始的 A4 PDF 檔案(至多10個)放在 src 資料夾
# 轉換後的 A4 合併檔、A3 PDF 檔案放在 dest 資料夾

class PDFModel:
    """PDF模型 - 整合pdf合併和轉換功能"""

    def __init__(self):
        #--設定來源與目標檔案夾Desktop路徑
        base_dir = str(paths.PDF_MERGE_BASE_DIR)
        self.src_dir = os.path.join(base_dir, "src")
        self.dest_dir = os.path.join(base_dir, "dest")
        #--確保資料夾存在
        os.makedirs(self.src_dir, exist_ok=True)
        os.makedirs(self.dest_dir, exist_ok=True)

    def merge_pdfs(self, pdf_files):
        """
        合併多個A4的PDF檔案
        Args:
            pdf_files: 要合併的PDF檔案路徑列表
        Returns:
            output_path: 合併後的PDF檔案路徑(單一A4)
        Raises:
            ValueError, FileNotFoundError
        """
        #--檢查是否有檔案可合併
        if not pdf_files:
            raise ValueError(f"{self.src_dir} 沒有檔案可合併")
        
        #--建立PdfWriter物件來寫入合併的PDF
        writer = PdfWriter()
        for pdf_path in pdf_files:
            if not os.path.exists(pdf_path):
                # raise FileNotFoundError(f"檔案不存在: {pdf_path}")
                print(f"檔案不存在: {pdf_path}")
                continue  #--跳過該檔案
            #--讀取PDF並加入至writer
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                writer.add_page(page)
        
        #--設定輸出路徑，並儲存合併後的PDF單一檔案
        output_path = os.path.join(self.dest_dir, 'combined_a4.pdf')
        with open(output_path, 'wb') as output_pdf:
            writer.write(output_pdf)

        return output_path

    def convert_a4_to_a3(self, input_pdf_path, output_pdf_path=None):
        """
        將單一A4轉換為單一A3格式
        Args:
            input_pdf_path: 原始檔案路徑列表
            output_pdf_path: 輸出檔案路徑（可選）
        Returns:
            output_pdf_path: 輸出檔案路徑
        Raises:
            FileNotFoundError, ValueError
        """
        #--檢查輸入檔案是否存在
        if not os.path.exists(input_pdf_path):
            raise FileNotFoundError(f"輸入檔案不存在: {input_pdf_path}")

        if output_pdf_path is None:
            output_pdf_path = os.path.join(self.dest_dir, 'combined_a3.pdf')

        #--打開原 PDF 文件
        input_pdf = fitz.open(input_pdf_path)
        #--獲取原檔的總頁數
        input_pdf_pages = len(input_pdf)
        if input_pdf_pages < 2:
            #--低於兩頁無法轉換
            input_pdf.close()
            raise ValueError("至少需要兩頁A4轉換為一頁A3")

        #--建立新PDF文件
        output_pdf = fitz.open()

        #--定義 A4 和 A3 尺寸
        a4_width, a4_height = fitz.paper_size("a4")
        a3_width = a4_width * 2
        a3_height = a4_height

        #--讀取每兩頁 A4，放入一頁 A3
        for i in range(0, len(input_pdf), 2):
            #--建立新頁面，尺寸為 A3 橫式
            new_page = output_pdf.new_page(width=a3_width, height=a3_height)

            #--第一頁在左側
            page1 = input_pdf[i]
            rect1 = fitz.Rect(0, 0, a4_width, a4_height)
            new_page.show_pdf_page(rect1, input_pdf, i)

            #--第二頁在右側(最後一頁若為單數頁，則不處理)
            if i + 1 < len(input_pdf):
                page2 = input_pdf[i + 1]
                rect2 = fitz.Rect(a4_width, 0, a3_width, a4_height)
                new_page.show_pdf_page(rect2, input_pdf, i + 1)

        #--儲存新PDF文件
        output_pdf.save(output_pdf_path)
        output_pdf.close()
        input_pdf.close()

        return output_pdf_path

    def prepare_files_for_merge(self, ori_files):
        """
        複製原始檔案至src目錄並重新命名
        Args:
            ori_files: 原始檔案路徑列表
        Returns:
            renamed_files: 重新命名後可供合併的檔案路徑列表
        Raises:
            --
        """
        #--清空取用檔案的src目錄
        for f in os.listdir(self.src_dir):
            os.remove(os.path.join(self.src_dir, f))

        #--複製檔案，並重新命名預計取用檔案
        letters = 'abcdefghij'  #--最多10個
        renamed_files = []
        for i, file_path in enumerate(ori_files[:10]):  #--最多10個
            dest_path = os.path.join(self.src_dir, f"{letters[i]}.pdf")
            shutil.copy(file_path, dest_path)
            renamed_files.append(dest_path)

        return renamed_files

    def merge_and_convert(self, file_list):
        """
        合併並轉換PDF檔案的完整流程
        Args:
            file_list: 原始檔案路徑列表
        Returns:
            True, False: 成功與否
        Raises:
            Exception
        """
        try:
            #--準備檔案路徑
            prepared_files = self.prepare_files_for_merge(file_list)
            print(f"準備合併的檔案: {prepared_files}")
            #--合併成單一A4的PDF
            merged_a4_path = self.merge_pdfs(prepared_files)
            print(f"合併後的單一A4檔案: {merged_a4_path}")
            #--轉換為A3
            merged_a3_path = self.convert_a4_to_a3(merged_a4_path)
            print(f"合併後的單一A3檔案: {merged_a3_path}")

            return True
        except Exception as e:
            print(f"合併和轉換過程發生錯誤: {e}")
            return False

    def get_output_path(self, format: str='A3') -> str:
        """
        獲取輸出檔案路徑
        Args:
            format: 輸出格式(預設'A3')
        Returns:
            output_path: 輸出檔案路徑
        Raises:
            ValueError
        """
        #--根據格式決定檔案名稱
        formats = {
            'a4': 'combined_a4.pdf',
            'a3': 'combined_a3.pdf',
        }
        #--組合並檢查完整路徑
        try:
            filename = formats[format.lower()]
            output_path = os.path.join(self.dest_dir, filename)
            if not os.path.exists(output_path):
                raise ValueError(f"檔案不存在: {output_path}")
        except KeyError:
            raise ValueError(f"不支援格式: {format}")

        return output_path