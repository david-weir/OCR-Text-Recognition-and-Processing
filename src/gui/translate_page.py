from pydoc import cli
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import options_page
import edit_page
from textModel import *
import translation_popup
import text_preview

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import translation as t
import summarise

class TranslatePage(Frame):
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

        translate_opt = IntVar()
        summarise_opt = IntVar()

        Checkbutton(center, text="Translate", variable=translate_opt, onvalue=1, offvalue=0).place(relx=0.5, rely=0.3, anchor=CENTER)
        Checkbutton(center, text="Summarise", variable=summarise_opt, onvalue=1, offvalue=0).place(relx=0.5, rely=0.4, anchor=CENTER)

        Button(center, text="Confirm", command= lambda: self.text_options(translate_opt, summarise_opt)).place(relx=0.5, rely=0.6, anchor=CENTER)

        previous = Button(btm_frame, text ="Back",
                   command = lambda : controller.show_frame(edit_page.EditPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text ="Next",
               command = lambda : controller.show_frame(options_page.OptionsPage))
        next.pack(side='right', padx=8, pady=5)

    def text_options(self, translate_opt, summarise_opt):
        if translate_opt.get() == 1 and summarise_opt.get() == 1:
            translation_popup.select_translation()
            file = text_model.get_textfile()
            
            with open("translated.txt", 'w') as ft:
                summarised = summarise.summarisation(file)
                ft.write(t.translate(text_model.get_src_language(), text_model.get_dst_language(), summarised))
            text_preview.view_new_version()

        elif translate_opt.get() == 1:
            translation_popup.select_translation()
            
            file = text_model.get_textfile()
            with open(file, 'r') as f:
                with open("translated.txt", 'w') as ft:
                    ft.write(t.translate(text_model.get_src_language(), text_model.get_dst_language(), f.read()))

        elif summarise_opt.get() == 1:
            file = text_model.get_textfile()
            with open("translated.txt", 'w') as ft:
                ft.write(summarise.summarisation(file))
            text_preview.view_new_version()

    def show_page(self, center):
        options = [
            "Language",
            "English",
            "French",
            "German"
        ]

        lang_codes = {
            "English": "en",
            "French": "fr",
            "German": "de"
        }

        lang_codes2 = { # include in text model
            "en": "English",
            "fr": "French",
            "de": "German"
        }

        detected = lang_codes2[text_model.get_src_language()]
        options.remove(detected)
        
        # datatype of menu text
        clicked = StringVar()
        
        # initial menu text
        clicked.set("Language")
        
        # Create Dropdown menu
        dropdown = OptionMenu(center, clicked, *options)
        dropdown.config(width=7)

        message = Label(center, text=detected).place(relx=0.3, rely=0.7, anchor=CENTER)
        select_message = Label(center, text="To").place(relx=0.5, rely=0.7, anchor=CENTER)
        dropdown.place(relx=0.7, rely=0.7, anchor=CENTER)

        confirm = Button(center, text="Confirm", command=lambda: self.confirm(clicked.get())).place(relx=0.5, rely=0.8, anchor=CENTER)

    def confirm(self, clicked):
        lang_codes = {
            "English": "en",
            "French": "fr",
            "German": "de"
        }

        text_model.set_dst_language(lang_codes[clicked])
        file = text_model.get_textfile()
        with open(file, 'r') as f:
            with open("translated.txt", 'w') as ft:
                ft.write(t.translate(text_model.get_src_language(), text_model.get_dst_language(), f.read()))