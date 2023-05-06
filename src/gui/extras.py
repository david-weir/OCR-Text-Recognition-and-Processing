from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames
from textModel import *

from pdf2jpg import pdf2jpg

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detection import *


def open_pdf():
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

