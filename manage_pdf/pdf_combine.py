import os
from pypdf import PdfReader, PdfWriter
import pdf_A4_to_A3 as pdf_a3

# 使用範例：
# 將原始的 A4 PDF 檔案合併，以及轉換出另一個 A3 PDF 檔案
# A4 合併前，可善用 Edge 列印功能，移除原檔案不必要的頁面
# 原始的 A4 PDF 檔案(至多10個)放在 file_src 資料夾
# 轉換後的 A4 合併檔、A3 PDF 檔案放在 file_dest 資料夾

# 設定資料夾路徑
dir_src = os.path.join('file_src')
dir_dest = os.path.join('file_dest')

# 確保來源資料夾存在，且存在檔案
if not os.path.exists(dir_src):
    os.makedirs(dir_src)
    exit()
if not os.listdir(dir_src):
    print(f"來源路徑不存在或空白，請先在 {dir_src} 放入PDF檔案(至多10個，以a.pdf到j.pdf命名)")
    exit()

# 確保目標資料夾存在
if not os.path.exists(dir_dest):
    os.makedirs(dir_dest)

# 定義檔名，需要合併的PDF檔案(10個，從a.pdf到j.pdf依序執行)
pdfs = ['a.pdf', 'b.pdf', 'c.pdf', 'd.pdf', 'e.pdf', 'f.pdf', 'g.pdf', 'h.pdf', 'i.pdf', 'j.pdf']
pdf_a4_combined = 'combined_a4.pdf'
pdf_a3_converted = 'combined_a3.pdf'

try:
    # 創建PdfWriter物件來寫入合併的PDF
    writer = PdfWriter()

    # 迭代每個PDF檔案
    for pdf in pdfs:
        file_path_src = os.path.join(dir_src, pdf)
        
        # 檢查A4檔案是否存在
        if not os.path.exists(file_path_src):
            print(f"檔案不存在: {file_path_src}")
            continue  # 跳過該檔案
        # 讀取PDF檔案
        reader = PdfReader(file_path_src)

        # 將每個PDF的所有頁面加入PdfWriter中
        for page in reader.pages:
            writer.add_page(page)

    # 設定合併後PDF檔案的儲存路徑
    file_path_dest = os.path.join(dir_dest, pdf_a4_combined)
    
    # 寫入合併後的PDF檔案
    with open(file_path_dest, 'wb') as output_pdf:
        writer.write(output_pdf)

    print(f"PDF-A4已合併: {file_path_dest}")

except Exception as e:
    print(f"An error occurred: {e}")


# 將合併後的PDF轉換為A3格式
input_pdf = os.path.join(dir_dest, pdf_a4_combined)  # 合併後的PDF檔案
output_pdf = os.path.join(dir_dest, pdf_a3_converted)  # 轉換後的A3 PDF檔案
try:
    if not os.path.exists(input_pdf):
        raise FileNotFoundError(f"{input_pdf} does not exist.")
    
    if pdf_a3.convert_pdf_a4_to_a3_unresized(input_pdf, output_pdf) == False:
        raise Exception("A3 conversion failed.")

except Exception as e:
    print(f"An error occurred during A3 conversion: {e}")
