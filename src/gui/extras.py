from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile 
import time
import fitz # install PyMuPDF

def open_pdf():
    file_path = askopenfile(mode='r', filetypes=[('PDFs', '*pdf')])
    if file_path is not None:
        doc = fitz.open(file_path)

        text = open("example.txt", "w")
        for page in doc:
            text.write(page.get_text())

        return text


def open_images():
    file_path = askopenfile(mode='r', filetypes=[('Image Files', ['*jpeg', '*png'])])
    if file_path is not None:
        return file_path

"""def change_page(self, prev, next, controller, row):
    change_page = Frame(self, bg='red')
    change_page.grid(row=3, column=1)
    
    prev_page = Button(change_page, text ="Page 1",
                command = lambda : controller.show_frame(prev))

    # putting the button in its place by
    # using grid
    prev_page.grid(row = row, column = 1, padx = 10, pady = 10)

    ## button to show frame 2 with text layout2
    next_page = Button(change_page, text ="Page 2",
                command = lambda : controller.show_frame(next))
    
    next_page.grid(row = row, column = 2, padx = 10, pady = 10)"""