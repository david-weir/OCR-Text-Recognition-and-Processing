import tkinter as tk
from tkinter import *
from textModel import *
import ui_messages

def on_close(selected, window):
    lang_codes = text_model.get_language_dict()
    text_model.set_dst_language(lang_codes[selected.get()])

    window.destroy()

# create a popup window to select the target translation language
def select_translation():
    window = Toplevel()
    window.title("Select Language")
    window.geometry('400x200')
    
    # translation options
    options = [
        "English",
        "French",
        "German"
    ]

    lang_codes = text_model.get_language_dict()

    try:
        detected = lang_codes[text_model.get_src_language()]
        options.remove(detected) # only show possible destination languages

        selected = StringVar() # the variable that will hold the language selected
        selected.set("Language") # initial value of the dropdown
        
        # Create Dropdown menu
        dropdown = OptionMenu(window, selected, *options)
        dropdown.config(width=7)

        # shows: {source language} to [dropdown options]
        Label(window, text=detected).place(relx=0.3, rely=0.4, anchor=CENTER)
        Label(window, text="To").place(relx=0.5, rely=0.4, anchor=CENTER)
        dropdown.place(relx=0.7, rely=0.4, anchor=CENTER)

        # on confirm, close the popup and set the destination language
        Button(window, text="Confirm", command=lambda: on_close(selected, window)).place(relx=0.5, rely=0.6, anchor=CENTER)
        window.wait_window()
        return True
    
    except KeyError: # if the language is not in the supported languages dictionary
        Label(window, text=ui_messages.translation_popup, wraplength=350).pack(anchor=CENTER)
        window.wait_window()
        return False

    # window.wait_window() # wait for the window to close before moving onto the next step -> translation
