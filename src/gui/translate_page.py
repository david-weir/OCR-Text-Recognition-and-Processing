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
        centre = tk.Frame(self, width=450, height=40, padx=3, pady=3)
        btm_frame = tk.Frame(self, width=450, height=45, pady=3)

        # layout all of the main containers

        top_frame.grid(row=0, sticky="ew")
        centre.grid(row=1, sticky="nsew")
        btm_frame.grid(row=3, sticky="ew")

        # create int variable that will be used in the checkbutton
        translate_opt = IntVar()
        summarise_opt = IntVar()

        # create checkbuttons to choose which output option you want
        Checkbutton(centre, text="Translate", variable=translate_opt, onvalue=1, offvalue=0).place(relx=0.5, rely=0.3, anchor=CENTER)
        Checkbutton(centre, text="Summarise", variable=summarise_opt, onvalue=1, offvalue=0).place(relx=0.5, rely=0.4, anchor=CENTER)

        # once options have been selected, confirm them
        Button(centre, text="Confirm", command= lambda: self.text_options(translate_opt, summarise_opt)).place(relx=0.5, rely=0.6, anchor=CENTER)

        # back / next page
        previous = Button(btm_frame, text ="Back",
                   command = lambda : controller.show_frame(edit_page.EditPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text ="Next",
               command = lambda : controller.show_frame(options_page.OptionsPage))
        next.pack(side='right', padx=8, pady=5)

    # translate / summarise based on the options picked
    def text_options(self, translate_opt, summarise_opt):
        # if user wants to translate and summarise
        if translate_opt.get() == 1 and summarise_opt.get() == 1:
            translation_possible = translation_popup.select_translation() # show popup to select target language
            file = text_model.get_textfile()
            
            if translation_possible:
                with open("translated.txt", 'w') as ft:
                    summarised = summarise.summarisation(file) # summarise the text first
                    print(summarised)
                    # translate the text and write the translated version to a file
                    ft.write(t.translate(text_model.get_src_language(), text_model.get_dst_language(), summarised))
                text_model.set_curr_language(text_model.get_dst_language())
                text_model.set_output_file("translated.txt")
                text_preview.view_new_version() # view the updated version of the text
            else:
                pass

        # if the user only wants to translate
        elif translate_opt.get() == 1:
            translation_possible = translation_popup.select_translation() # show popup to select target language
            
            file = text_model.get_textfile()
            if translation_possible:
                with open(file, 'r') as f:
                    with open("translated.txt", 'w') as ft:
                        ft.write(t.translate(text_model.get_src_language(), text_model.get_dst_language(), f.read()))
                text_model.set_curr_language(text_model.get_dst_language())
                text_model.set_output_file("translated.txt")
                text_preview.view_new_version() # view the updated version of the text
                    
            else:
                pass
        # if the user only wants to summarise
        elif summarise_opt.get() == 1:
            file = text_model.get_textfile()
            with open("translated.txt", 'w') as ft:
                ft.write(summarise.summarisation(file)) # write the summarised version to a file
            text_model.set_output_file("translated.txt")
            text_preview.view_new_version() # view the updated version of the text