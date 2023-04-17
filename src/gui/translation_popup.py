import tkinter as tk
from tkinter import *
from textModel import *

def confirm(clicked):
    lang_codes = {
        "English": "en",
        "French": "fr",
        "German": "de"
    }

    text_model.set_dst_language(lang_codes[clicked])

def select_translation():
    window = Toplevel()
    window.title("Select Language")
    window.geometry('400x200')
    options = [
        "English",
        "French",
        "German"
    ]

    lang_codes = { # include in text model
        "en": "English",
        "fr": "French",
        "de": "German"
    }

    detected = lang_codes[text_model.get_src_language()]
    options.remove(detected)
    
    # datatype of menu text
    clicked = StringVar()
    
    # initial menu text
    clicked.set("Language")
    
    # Create Dropdown menu
    dropdown = OptionMenu(window, clicked, *options)
    dropdown.config(width=7)

    Label(window, text=detected).place(relx=0.3, rely=0.4, anchor=CENTER)
    Label(window, text="To").place(relx=0.5, rely=0.4, anchor=CENTER)
    dropdown.place(relx=0.7, rely=0.4, anchor=CENTER)

    confirm_btn = Button(window, text="Confirm", command=lambda: {confirm(clicked.get()), window.destroy()}).place(relx=0.5, rely=0.6, anchor=CENTER)
    window.wait_window()
