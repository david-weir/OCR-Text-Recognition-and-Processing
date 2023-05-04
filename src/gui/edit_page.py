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

        self.show_first_frame(center, top_frame)

        previous = Button(btm_frame, text ="Back",
                   command = lambda : controller.show_frame(upload_page.UploadPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text ="Next",
               command = lambda : {controller.show_frame(translate_page.TranslatePage), self.reset_page(top_frame, center)})
        next.pack(side='right', padx=8, pady=5)

    # tie first frame to a function so it can be displayed again after leaving the page
    def show_first_frame(self, center, top_frame):
        message = tk.Label(center, text=ui_messages.edit_page, wraplength=450)
        b = Button(center, text="Edit", command=lambda: {b.pack_forget(), message.pack_forget(), self.showpage(center, top_frame)})
        message.pack(expand=True)
        b.pack(expand=True)

    # once edit button has been clicked, display text box and language choice
    def showpage(self, center, top_frame):
        options = [ # options for the dropdown menu
            "Language",
            "English",
            "French",
            "German"
        ]
        
        # datatype of menu text
        clicked = StringVar()
        clicked.set("Language") # set an initial value for the dropdown menu 
        
        # create dropdown menu
        dropdown = OptionMenu(top_frame, clicked, *options)
        dropdown.config(width=7)

        # get the dictionary that maps the language name to code, vice versa
        lang_codes = text_model.get_language_dict()

        select_message = Label(top_frame, text="Please Select:   ")
        detected = text_model.get_src_language()
        
        # check if language detection was successful
        if detected == False: # if not, as user to manually select the language
            Label(top_frame, text="Failed to Detect Language.").pack(side='left', padx=5)
            select_message.pack(side='left', padx=5)
            dropdown.pack(side='left', padx=5) # display dropdown menu of languages

            Button(top_frame, text="Confirm", command=lambda: text_model.update_src_language(lang_codes[clicked.get()])).pack(side='right', padx=5)
        
        else: # if it has detected a language
            detected_label = Label(top_frame, text="Language Detected: {}".format(lang_codes[detected]))
            detected_label.pack(side='left', padx=5)

            confirm = Button(top_frame, text="Confirm", command=lambda: text_model.update_src_language(lang_codes[clicked.get()]))

            change = Button(top_frame, text="Change", command=lambda: # if the language it has detected is incorrect -> display the dropdown
                     {detected_label.pack_forget(), change.pack_forget(), select_message.pack(side='left', padx=5), dropdown.pack(side='left', padx=5), confirm.pack(side='right', padx=5)})
            change.pack(side='right', padx=5)

        # create the widgets for the frame
        txt_edit = tk.Text(center, highlightthickness=0)
        side_menu = tk.Frame(center, relief=tk.RAISED, bd=2)
        save_button = tk.Button(side_menu, text="Save", command=lambda:self.save(txt_edit))
        scroll = Scrollbar(center, command=txt_edit.yview) # add a scrollbar to the textbox going down
        txt_edit.configure(yscrollcommand=scroll.set)

        save_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        side_menu.grid(row=0, column=0, sticky="ns")
        txt_edit.grid(row=0, column=1, sticky="nsew")
        scroll.grid(row=0, column=2, sticky='ns')

        textfile = text_model.get_textfile()
        with open(textfile, 'r') as text: # open the textfile in the text box
            tx = text.read()
            txt_edit.insert(tk.END, tx)

    # update the text file with any changes made
    def save(self, txt_edit):
        new_text = txt_edit.get("1.0",END)
        new_file = 'output.txt'
        with open(new_file, 'w') as f:
            f.write(new_text)
            text_model.set_textfile(new_file)

    # when you leave the frame, delete the textbox and show the original frame again
    def reset_page(self, top_frame, center):
        for widget in top_frame.winfo_children():
            widget.destroy()
        for widget in center.winfo_children():
            widget.destroy()

        self.show_first_frame(center, top_frame)
