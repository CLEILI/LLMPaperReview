import fitz
import os
from PIL import Image

def pdf2image1(pdf,path1, path2):

    pdfDoc = fitz.open(path1)
    pg=0
    page = pdfDoc.load_page(pg)

    # 获取页面的图像对象
    # matrix = fitz.Matrix(1.0, 1.0)  # 1.0 表示原始尺寸
    # pix = page.get_pixmap(matrix=matrix,dpi=200)
    pix = page.get_pixmap(matrix=fitz.Matrix(4,4))

    print(pix.width, pix.height)
    # 将图像转换为Pillow的Image对象
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    if not os.path.exists(path2):  # 判断存放图片的文件夹是否存在
        os.makedirs(path2)  # 若图片文件夹不存在就创建

    # 保存图像为PNG格式，不进行压缩
    # dpi = 96  # 设置所需的 DPI 值
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
