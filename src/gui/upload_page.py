from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from extras import *
import edit_page
import config
from textModel import *

class UploadPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create all of the main containers
        top_frame = tk.Frame(self, width=450, height=50, pady=3)
        center = tk.Frame(self, width=50, height=40, padx=3, pady=3)
        btm_frame = tk.Frame(self, width=450, height=45, pady=3)

        # layout all of the main containers

        top_frame.grid(row=0, sticky="ew")
        center.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")
        
        center.grid_rowconfigure(0, weight=1)
        center.grid_columnconfigure(0, weight=1)
        center.grid_columnconfigure(1, weight=1)
        
        ctr_left = tk.Frame(center)
        ctr_right = tk.Frame(center)

        ctr_left.grid(row=0, column=0, sticky="nsew")
        ctr_right.grid(row=0, column=1, sticky="nsew")
        
        
        label = Label(top_frame, text="Upload Documents", font=("Verdana", 20))
        label.place(relx=.5, rely=.5,anchor= CENTER)

        pdf_upload = Button(ctr_left, text="Upload PDFs", command=lambda:[open_pdf(), text_model.set_format("pdf")])
        pdf_upload.place(relx=.5, rely=.5, anchor=CENTER)

        options = [
            "Upload Images",
            "Printed",
            "Handwritten"
        ]
        
        # datatype of menu text
        clicked = StringVar()
        
        # initial menu text
        clicked.set("Upload Images")
        
        # Create Dropdown menu
        drop = OptionMenu(ctr_right, clicked, *options)
        drop.config(width=10)
        drop.place(relx=.5, rely=.5, anchor=CENTER)

        def upload_type():
            if clicked.get() == "Printed":
                open_images()
                text_model.set_format("printed image")
            elif clicked.get() == "Handwritten":
                open_images()
                text_model.set_format("handwritten image")

        caller_button = Button(ctr_right, text="Select", command=lambda:upload_type())
        caller_button.place(relx=.5, rely=.6, anchor=CENTER)

        previous = Button(btm_frame, text ="Back",
                   command = lambda : controller.show_frame(edit_page.EditPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text ="Next",
               command = lambda : controller.show_frame(edit_page.EditPage))
        next.pack(side='right', padx=8, pady=5)