from calendar import c
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import translate_page
import detection_page
from textModel import *

class EditPage(Frame):
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

        center.rowconfigure(0, minsize=450, weight=1)
        center.columnconfigure(1, weight=1) #, minsize=400,

        txt_edit = tk.Text(center)
        fr_buttons = tk.Frame(center, relief=tk.RAISED, bd=2)
        btn_open = tk.Button(fr_buttons, text="Save", command=lambda:text_model.set_text(txt_edit.get(1.0, tk.END)))
        #btn_save = tk.Button(fr_buttons, text="Save As...")

        btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        #btn_save.grid(row=1, column=0, sticky="ew", padx=5)

        fr_buttons.grid(row=0, column=0, sticky="ns")
        txt_edit.grid(row=0, column=1, sticky="nsew")
        # txt_edit.rowconfigure(0, minsize=250, weight=1)

        text = text_model.get_text()
        txt_edit.insert(tk.END, text)

        previous = Button(btm_frame, text ="Back",
                   command = lambda : controller.show_frame(detection_page.DetectionPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text ="Next",
               command = lambda : controller.show_frame(translate_page.TranslatePage))
        next.pack(side='right', padx=8, pady=5)