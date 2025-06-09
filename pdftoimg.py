import fitz
import os
from PIL import Image

def pdf2image1(pdf,path1, path2):

    pdfDoc = fitz.open(path1)
    pg=0
    page = pdfDoc.load_page(pg)

    pix = page.get_pixmap(matrix=fitz.Matrix(4,4))

    print(pix.width, pix.height)

    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    if not os.path.exists(path2):  
        os.makedirs(path2)  

    img.save(path2 + '/' + f'{pdf}.jpg', )
    # img.save(f'output_{page_number}.png',)



    # pix.save(path2 + '/' + 'images_%s.png' % pg)  # 将图片写入指定的文件夹内
pdfs=[]
pdfs_path="./paper_pdfs"
for filename in os.listdir(pdfs_path):
    if filename.endswith('.pdf'):
        new_filename,_ = os.path.splitext(filename)
        pdfs.append(new_filename)
for pdf in pdfs:
    path1 = f"./paper_pdfs/{pdf}.pdf"
    path2 = "./images"
    pdf2image1(pdf,path1, path2)
