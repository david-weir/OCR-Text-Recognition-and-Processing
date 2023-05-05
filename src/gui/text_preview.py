from tkinter import *
import tkinter as tk
from textModel import *

# save any changes made to the text
def save(text_editor):
    new_text = text_editor.get("1.0",END) # get all the text in the text box
    new_file = 'translated.txt'
    with open(new_file, 'w') as f:
        f.write(new_text) # write the changes into the updated file
        text_model.set_output_file(new_file)

# show popup window of the translated/summarised text
def view_new_version():
    window = tk.Toplevel()  # create window of the popup
    window.geometry('550x330')
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    # create the widgets for the window
    text_editor = tk.Text(window)
    side_menu = tk.Frame(window, relief=tk.RAISED, bd=2)
    save_button = tk.Button(side_menu, text="Save", command=lambda:save(text_editor))
    scroll = Scrollbar(window, command=text_editor.yview)
    text_editor.configure(yscrollcommand=scroll.set)

    with open('translated.txt', 'r') as text:
        tx = text.read() # load the textfile into the text box
        text_editor.insert(tk.END, tx)

    save_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    side_menu.grid(row=0, column=0, sticky="ns")
    text_editor.grid(row=0, column=1, sticky="nsew")
    scroll.grid(row=0, column=2, sticky='ns')
