from calendar import c
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import translate_page
import upload_page
from textModel import *

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from detection import *

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

        """options = [
            "Language",
            "English",
            "French",
            "German"
        ]
        
        # datatype of menu text
        clicked = StringVar()
        
        # initial menu text
        clicked.set("Language")
        
        # Create Dropdown menu
        dropdown = OptionMenu(top_frame, clicked, *options)
        dropdown.config(width=7)

        lang_codes = { # include in text model
            "en": "English",
            "fr": "French",
            "de": "German"
        }
        select_message = Label(top_frame, text="Please Select:   ")
        detected = detection_text(text_model.get_text())
        if detected == False:
            print("false")
            message = Label(top_frame, text="Failed to Detect Language.").pack(side='left', padx=5)
            select_message.pack(side='left', padx=5)
            dropdown.pack(side='left', padx=5)

            Button(top_frame, text="Confirm", command=lambda: text_model.set_src_language(clicked)).pack(side='right', padx=5)
        else:
            detected_label = Label(top_frame, text="Language Detected: {}".format(lang_codes[detected]))
            detected_label.pack(side='left', padx=5)

            confirm_update = Button(top_frame, text="Confirm", command=lambda: text_model.set_src_language(clicked))

            confirm = Button(top_frame, text="Confirm", command=lambda: text_model.set_src_language(lang_codes[detected]))

            change = Button(top_frame, text="Change", command=lambda: 
                     {detected_label.pack_forget(), change.pack_forget(), confirm.pack_forget(), select_message.pack(side='left', padx=5), dropdown.pack(side='left', padx=5), confirm_update.pack(side='right', padx=5)})
            change.pack(side='right', padx=5)
            confirm.pack(side='right', padx=5)"""

        center.rowconfigure(0, minsize=450, weight=1)
        center.columnconfigure(1, weight=1) #, minsize=400,
        # txt_edit = tk.Text(center)

        b = Button(center, text="chance to edit text", command=lambda: {self.showpage(center, top_frame), b.destroy()})
        b.grid(row=0, column=0)
        """txt_edit = tk.Text(center)
        fr_buttons = tk.Frame(center, relief=tk.RAISED, bd=2)
        btn_open = tk.Button(fr_buttons, text="Save", command=lambda:text_model.set_text(txt_edit.get(1.0, tk.END)))
        btn_save = tk.Button(fr_buttons, text="Save As...", command=lambda:{self.showpreview(txt_edit), self.showlanguage(top_frame)})

        btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_save.grid(row=1, column=0, sticky="ew", padx=5)

        fr_buttons.grid(row=0, column=0, sticky="ns")
        txt_edit.grid(row=0, column=1, sticky="nsew")"""
        # txt_edit.rowconfigure(0, minsize=250, weight=1)

        
        """textfile = text_model.get_textfile()
        with open(textfile, 'r') as text:
            tx = text.read()
            txt_edit.insert(tk.END, tx)"""

        previous = Button(btm_frame, text ="Back",
                   command = lambda : controller.show_frame(upload_page.UploadPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text ="Next",
               command = lambda : controller.show_frame(translate_page.TranslatePage))
        next.pack(side='right', padx=8, pady=5)

    def showpage(self, center, top_frame):
        options = [
            "Language",
            "English",
            "French",
            "German"
        ]
        
        # datatype of menu text
        clicked = StringVar()
        
        # initial menu text
        clicked.set("Language")
        
        # Create Dropdown menu
        dropdown = OptionMenu(top_frame, clicked, *options)
        dropdown.config(width=7)

        lang_codes = { # include in text model
            "en": "English",
            "fr": "French",
            "de": "German"
        }
        select_message = Label(top_frame, text="Please Select:   ")
        detected = detection_text(text_model.get_text())
        print(text_model.get_text())
        if detected == False:
            print("false")
            message = Label(top_frame, text="Failed to Detect Language.").pack(side='left', padx=5)
            select_message.pack(side='left', padx=5)
            dropdown.pack(side='left', padx=5)

            Button(top_frame, text="Confirm", command=lambda: text_model.set_src_language(clicked)).pack(side='right', padx=5)
        else:
            detected_label = Label(top_frame, text="Language Detected: {}".format(lang_codes[detected]))
            detected_label.pack(side='left', padx=5)

            confirm_update = Button(top_frame, text="Confirm", command=lambda: text_model.set_src_language(clicked))

            confirm = Button(top_frame, text="Confirm", command=lambda: text_model.set_src_language(lang_codes[detected]))

            change = Button(top_frame, text="Change", command=lambda: 
                     {detected_label.pack_forget(), change.pack_forget(), confirm.pack_forget(), select_message.pack(side='left', padx=5), dropdown.pack(side='left', padx=5), confirm_update.pack(side='right', padx=5)})
            change.pack(side='right', padx=5)
            confirm.pack(side='right', padx=5)
        
        txt_edit = tk.Text(center)
        fr_buttons = tk.Frame(center, relief=tk.RAISED, bd=2)
        btn_open = tk.Button(fr_buttons, text="Save", command=lambda:text_model.set_text(txt_edit.get(1.0, tk.END)))
        btn_save = tk.Button(fr_buttons, text="Save As...", command=lambda:{self.showpreview(txt_edit), self.showlanguage(top_frame)})

        btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        btn_save.grid(row=1, column=0, sticky="ew", padx=5)

        fr_buttons.grid(row=0, column=0, sticky="ns")
        txt_edit.grid(row=0, column=1, sticky="nsew")

        textfile = text_model.get_textfile()
        with open(textfile, 'r') as text:
            tx = text.read()
            txt_edit.insert(tk.END, tx)

    """def showpreview(self, txt_edit):
        textfile = text_model.get_textfile()
        with open(textfile, 'r') as text:
            tx = text.read()
            txt_edit.insert(tk.END, tx)

    def showlanguage(self, top_frame):
        options = [
            "Language",
            "English",
            "French",
            "German"
        ]
        
        # datatype of menu text
        clicked = StringVar()
        
        # initial menu text
        clicked.set("Language")
        
        # Create Dropdown menu
        dropdown = OptionMenu(top_frame, clicked, *options)
        dropdown.config(width=7)

        lang_codes = { # include in text model
            "en": "English",
            "fr": "French",
            "de": "German"
        }
        select_message = Label(top_frame, text="Please Select:   ")
        detected = detection_text(text_model.get_text())
        if detected == False:
            print("false")
            message = Label(top_frame, text="Failed to Detect Language.").pack(side='left', padx=5)
            select_message.pack(side='left', padx=5)
            dropdown.pack(side='left', padx=5)

            Button(top_frame, text="Confirm", command=lambda: text_model.set_src_language(clicked)).pack(side='right', padx=5)
        else:
            detected_label = Label(top_frame, text="Language Detected: {}".format(lang_codes[detected]))
            detected_label.pack(side='left', padx=5)

            confirm_update = Button(top_frame, text="Confirm", command=lambda: text_model.set_src_language(clicked))

            confirm = Button(top_frame, text="Confirm", command=lambda: text_model.set_src_language(lang_codes[detected]))

            change = Button(top_frame, text="Change", command=lambda: 
                     {detected_label.pack_forget(), change.pack_forget(), confirm.pack_forget(), select_message.pack(side='left', padx=5), dropdown.pack(side='left', padx=5), confirm_update.pack(side='right', padx=5)})
            change.pack(side='right', padx=5)
            confirm.pack(side='right', padx=5)"""