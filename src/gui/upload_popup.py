import tkinter as tk
from tkinter import *
from textModel import *
from extras import *
from tkinter.filedialog import askdirectory


def upload_images(img):
    if img == 1:
        open_printed_image()
    if img == 2:
        dir = askdirectory()
        text_model.set_dir_path(dir)


def select_upload_type():
    window = Toplevel()
    window.title("Select Upload Type")
    window.geometry('250x150')

    var = IntVar()

    one = Radiobutton(window, text='Upload one image', value=1, variable=var)
    one.pack(fill='x', padx=5, pady=10)
    two = Radiobutton(window, text='Upload a folder', value=2, variable=var)
    two.pack(fill='x', padx=5, pady=5)

    Button(window, text='Select', command=lambda: {upload_images(var.get()), window.destroy}).pack(side='bottom', pady=15) #, command=lambda: [upload_images(var.get())]
    
    window.wait_window()