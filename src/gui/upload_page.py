from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from extras import *
import edit_page
from textModel import *
from upload_popup import *

from img_ocr import single_ocr
import sys

sys.path.insert(0, '../src/')


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
        ctr_bottom = tk.Frame(center, height=100)

        ctr_left.grid(row=0, column=0, sticky="nsew")
        ctr_right.grid(row=0, column=1, sticky="nsew")
        ctr_bottom.grid(row=1, columnspan=2, sticky='nsew')
        ctr_bottom.pack_propagate(False)

        label = Label(top_frame, text="Upload Documents", font=("Verdana", 20))
        label.place(relx=.5, rely=.5, anchor=CENTER)
        # files = Listbox(ctr_bottom, width=100, height=40)
        files = Label(ctr_bottom, text="Uploaded File: ")
        confirm_btn = Button(ctr_bottom, text="Confirm",
                             command=lambda: self.dir_ocr(btm_frame, controller, files, confirm_btn))

        pdf_upload = Button(ctr_left, text="Upload PDFs", command=lambda: [open_pdf(), text_model.set_format("pdf"),
                                                                           self.show_pdf_file(files, confirm_btn,
                                                                                              ctr_bottom, btm_frame,
                                                                                              controller)])
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
                select_upload_type()
                self.show_printed_file(files, confirm_btn, ctr_bottom, btm_frame, controller)

            elif clicked.get() == "Handwritten":
                # open_images()
                text_model.set_format("handwritten image")

        caller_button = Button(ctr_right, text="Select", command=lambda: {upload_type()})
        caller_button.place(relx=.5, rely=.7, anchor=CENTER)

    def show_pdf_file(self, files, confirm_btn, ctr_bottom, btm_frame, controller):
        file_name = text_model.get_filename()
        if file_name is not None:
            if files['text'] == "Uploaded File: ":
                files['text'] += file_name
            else:
                files['text'] = "Uploaded File: " + file_name
            files.pack(anchor=CENTER)
            confirm_btn = Button(ctr_bottom, text="Confirm",
                                 command=lambda: self.show_next(btm_frame, controller, files, confirm_btn))
            confirm_btn.pack(anchor=CENTER, pady=5)

    def show_printed_file(self, files, confirm_btn, ctr_bottom, btm_frame, controller):
        file_name = text_model.get_filename()
        if file_name is not None:
            if files['text'] == "Uploaded: ":
                files['text'] += file_name
            else:
                files['text'] = "Uploaded: " + file_name
            files.pack(anchor=CENTER)
            format = text_model.get_format()
            if format == 'single image':
                confirm_btn = Button(ctr_bottom, text="Confirm",
                                     command=lambda: self.dir_ocr(btm_frame, controller, files, confirm_btn))
            confirm_btn.pack(anchor=CENTER, pady=5)

    def reset_page(self, files, confirm_btn):
        files.pack_forget()
        confirm_btn.pack_forget()

    def dir_ocr(self, btm_frame, controller, files, confirm_btn):
        single_ocr(text_model.get_dir_path())
        self.show_next(btm_frame, controller, files, confirm_btn)

    def show_next(self, btm_frame, controller, files, confirm_btn):
        next = Button(btm_frame, text="Next",
                      command=lambda: {controller.show_frame(edit_page.EditPage), self.reset_page(files, confirm_btn),
                                       next.destroy()})
        next.pack(side='right', padx=8, pady=5)
