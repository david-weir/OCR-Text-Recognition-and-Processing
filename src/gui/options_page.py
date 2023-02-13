from tkinter import *
from tkinter.ttk import *
import tkinter as tk
#from src.detection import *
import edit_page
import upload_page

class OptionsPage(Frame):
    
    def __init__(self, parent, controller):
        
        Frame.__init__(self, parent)
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # create all of the main containers
        top_frame = tk.Frame(self, width=450, height=50, pady=3)
        center = tk.Frame(self, width=450, height=40, padx=3, pady=3)
        btm_frame = tk.Frame(self, width=450, height=45, pady=3)

        # layout all of the main containers

        top_frame.grid(row=0, sticky="ew")
        center.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")

        pdf_option = IntVar()
        mp3_option = IntVar()

        Checkbutton(center, text="Convert to PDF", variable=pdf_option).place(relx=0.5, rely=0.3, anchor=CENTER)
        Checkbutton(center, text="Convert to MP3", variable=mp3_option).place(relx=0.5, rely=0.4, anchor=CENTER)

        Button(center, text="Confirm").place(relx=0.5, rely=0.6, anchor=CENTER)

        pdf_frame = tk.Frame(center, bg="red").pack(side='bottom', fill='both')
        Button(pdf_frame, text="Confirm").place(relx=0.2, rely=0.5, anchor=CENTER)
        
        # pdf_filename = StringVar()
        # name_label = Label(center, text='PDF filename:')
        # name_label.place(relx=0.1, rely=0.9, anchor=CENTER)
        # Entry(pdf_frame, textvariable=pdf_filename).place(relx=0.2, rely=0.5, anchor=CENTER)


        previous = Button(btm_frame, text="Back",
                   command = lambda : controller.show_frame(edit_page.EditPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text="Next",
               command = lambda : controller.show_frame(upload_page.UploadPage))
        next.pack(side='right', padx=8, pady=5)