from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames 
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from textModel import *

from pdf2jpg import pdf2jpg

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detection import *


def open_pdf():
    file_path = askopenfilename(filetypes=[('PDFs', '*pdf')])  # mode='rb',

    if file_path is not None:
        resource_mgr = PDFResourceManager()
        ret_data = StringIO()
        device = TextConverter(resource_mgr, ret_data, codec='latin-1', laparams=LAParams())
        input_file = open(file_path, 'rb')
        interpreter = PDFPageInterpreter(resource_mgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()

        for page in PDFPage.get_pages(input_file, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
            interpreter.process_page(page)

        text = ret_data.getvalue()

        with open('output.txt', 'w') as f:
            f.write(text)
        
        text_model.set_textfile('output.txt')
        text_model.set_output_file('output.txt')
        text_model.set_text()
        text_model.set_src_language()
        text_model.set_curr_language(text_model.get_src_language())
        text_model.set_filename(file_path)

        input_file.close()
        device.close()
        ret_data.close()

        return text


def alternate_pdf_for_ocr_test():
    pdf_path = askopenfilename(filetypes=[('PDFs', '*pdf')])

    if pdf_path is not None:

        pdf2jpg.convert_pdf2jpg(pdf_path, "./", pages="ALL")

        text_model.set_filename(pdf_path + "_dir")
        text_model.set_dir_path(text_model.get_filename())

        text_model.set_format("directory")


def open_printed_image():
    file_path = askopenfilename(filetypes=[('Image Files', ['*jpeg', '*png', '*jpg'])])
    if file_path is not None:
        text_model.set_filename(file_path)
        text_model.set_dir_path(file_path)


def open_folder():
    dir_path = askdirectory()

    if dir_path is not None:
        text_model.set_filename(dir_path)
        text_model.set_dir_path(dir_path)


def open_handwritten_images():
    img_path = askopenfilename(filetypes=[('Image Files', ['*jpeg', '*jpg', '*png'])])

    if img_path is not None:
        text_model.set_filename(img_path)
        text_model.set_dir_path(img_path)

