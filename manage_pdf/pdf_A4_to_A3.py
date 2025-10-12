import fitz  # pip install PyMuPDF  # https://pymupdf.readthedocs.io/en/latest/

# 使用範例：
# input_pdf = "input.pdf"   # 原始的 A4 PDF 檔案
# output_pdf = "output_A3.pdf"  # 轉換後的 A3 PDF 檔案
# convert_pdf_a4_to_a3_unresized(input_pdf, output_pdf)
# return True/False

def convert_pdf_a4_to_a3_unresized(input_pdf_path, output_pdf_path):
    # 打開原 PDF 文件
    input_pdf = fitz.open(input_pdf_path)
    # 獲取原檔的總頁數
    input_pdf_pages = len(input_pdf)
    if input_pdf_pages < 2:
        # 低於兩頁無法轉換
        print("至少需要兩頁A4轉換為一頁A3")
        return False

    # 建立新PDF文件
    output_pdf = fitz.open()

    # 定義 A4 和 A3 尺寸
    a4_width, a4_height = fitz.paper_size("a4")
    print(f"A4 size (orignal): w={a4_width} x h={a4_height}")
    a3_width = a4_width * 2
    a3_height = a4_height
    print(f"A3 size (converted): w={a3_width} x h={a3_height}")

    # 讀取每兩頁 A4，放入一頁 A3
    for i in range(0, len(input_pdf), 2): 
        # 建立新頁面，尺寸為 A3 橫式
        new_page = output_pdf.new_page(width=a3_width, height=a3_height)
        
        # 第一頁在左側
        page1 = input_pdf[i]
        rect1 = fitz.Rect(0, 0, a4_width, a4_height)
        new_page.show_pdf_page(rect1, input_pdf, i)

        # 第二頁在右側(最後一頁若為單數頁，則不處理)
        if i + 1 < len(input_pdf):
            page2 = input_pdf[i + 1]
            rect2 = fitz.Rect(a4_width, 0, a3_width, a4_height)
            new_page.show_pdf_page(rect2, input_pdf, i + 1)

    # 儲存新PDF文件
    output_pdf.save(output_pdf_path)
    output_pdf.close()
    input_pdf.close()

    print(f"PDF-A4成功轉換成A3: {output_pdf_path}")
    return True
