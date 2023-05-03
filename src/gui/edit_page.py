from calendar import c
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import translate_page
import upload_page
from textModel import *
import ui_messages

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

        center.rowconfigure(0, minsize=250, weight=1)
        center.columnconfigure(1, weight=1)

        # message = tk.Label(center, text=ui_messages.edit_page, wraplength=450)
        # b = Button(center, text="Edit", command=lambda: {b.destroy(), message.destroy(), self.showpage(center, top_frame)})
        # message.pack(expand=True)
        # b.pack(expand=True)
        # options = [
        #     "Language",
        #     "English",
        #     "French",
        #     "German"
        # ]
        
        # # datatype of menu text
        # clicked = StringVar()
        # dropdown = OptionMenu(top_frame, clicked, *options)
        # if not bool(message.winfo_ismapped()):
        self.show_first_frame(center, top_frame)
            # self.update()


        previous = Button(btm_frame, text ="Back",
                   command = lambda : controller.show_frame(upload_page.UploadPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text ="Next",
               command = lambda : {controller.show_frame(translate_page.TranslatePage), self.reset_page(top_frame, center)})
        next.pack(side='right', padx=8, pady=5)

    def show_first_frame(self, center, top_frame):
        message = tk.Label(center, text=ui_messages.edit_page, wraplength=450)
        b = Button(center, text="Edit", command=lambda: {b.pack_forget(), message.pack_forget(), self.showpage(center, top_frame)})
        message.pack(expand=True)
        b.pack(expand=True)

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
        lang_codes2 = {
            "English": "en",
            "French": "fr",
            "German": "de"
        }
        select_message = Label(top_frame, text="Please Select:   ")
        detected = text_model.get_src_language()
        
        if detected == False:
            print("false")
            message = Label(top_frame, text="Failed to Detect Language.").pack(side='left', padx=5)
            select_message.pack(side='left', padx=5)
            dropdown.pack(side='left', padx=5)

            Button(top_frame, text="Confirm", command=lambda: text_model.update_src_language(lang_codes2[clicked])).pack(side='right', padx=5)
        else:
            detected_label = Label(top_frame, text="Language Detected: {}".format(lang_codes[detected]))
            detected_label.pack(side='left', padx=5)

            confirm_update = Button(top_frame, text="Confirm", command=lambda: text_model.update_src_language(lang_codes2[clicked]))

            confirm = Button(top_frame, text="Confirm", command=lambda: text_model.update_src_language(detected))

            change = Button(top_frame, text="Change", command=lambda: 
                     {detected_label.pack_forget(), change.pack_forget(), confirm.pack_forget(), select_message.pack(side='left', padx=5), dropdown.pack(side='left', padx=5), confirm_update.pack(side='right', padx=5)})
            change.pack(side='right', padx=5)
            confirm.pack(side='right', padx=5)
        
        txt_edit = tk.Text(center)
        fr_buttons = tk.Frame(center, relief=tk.RAISED, bd=2)
        btn_open = tk.Button(fr_buttons, text="Save", command=lambda:text_model.set_text(txt_edit.get(1.0, tk.END)))
        scroll = Scrollbar(center, command=txt_edit.yview)
        txt_edit.configure(yscrollcommand=scroll.set)

        btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        fr_buttons.grid(row=0, column=0, sticky="ns")
        txt_edit.grid(row=0, column=1, sticky="nsew")
        scroll.grid(row=0, column=2, sticky='ns')

        textfile = text_model.get_textfile()
        with open(textfile, 'r') as text:
            tx = text.read()
            txt_edit.insert(tk.END, tx)

    def reset_page(self, top_frame, center):
        for widget in top_frame.winfo_children():
            widget.destroy()
        for widget in center.winfo_children():
            widget.destroy()

        self.show_first_frame(center, top_frame)
