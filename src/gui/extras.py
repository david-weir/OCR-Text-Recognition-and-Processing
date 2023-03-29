from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import fitz
from textModel import *

def open_pdf():
    file_path = askopenfile(mode='rb', filetypes=[('PDFs', '*pdf')])
    if file_path is not None:
        resource_mgr = PDFResourceManager()
        ret_data = StringIO()
        device = TextConverter(resource_mgr, ret_data, codec='utf-8', laparams=LAParams())
        # input_file = open(file_path, 'rb')
        interpreter = PDFPageInterpreter(resource_mgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(file_path, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = ret_data.getvalue()

        with open('output.txt', 'w') as f:
            f.write(text)
        
        text_model.set_textfile('output.txt')

        file_path.close()
        device.close()
        ret_data.close()
        # print(text)
        return text

# open_pdf()

"""def open_pdf1():
    file_path = askopenfile(mode='r', filetypes=[('PDFs', '*pdf')])
    if file_path is not None:
        doc = fitz.open(file_path)

        text = open("example.txt", "w")
        for page in doc:
            text.write(page.get_text())

        return text"""


def open_images():
    file_path = askopenfile(mode='r', filetypes=[('Image Files', ['*jpeg', '*png'])])
    if file_path is not None:
        return file_path
