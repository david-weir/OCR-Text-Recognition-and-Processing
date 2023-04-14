from tkinter import *
import tkinter as tk
from textModel import *

def view_new_version():
    window = tk.Toplevel() 
    window.geometry('400x300')
    window.grid_rowconfigure(1, weight=1)
    window.grid_columnconfigure(0, weight=1)

    # create all of the main containers
    top_frame = tk.Frame(window, width=450, height=50, pady=3)
    center = tk.Frame(window, width=450, height=40, padx=3, pady=3)
    btm_frame = tk.Frame(window, width=450, height=45, pady=3)

    # layout all of the main containers

    top_frame.grid(row=0, sticky="ew")
    center.grid(row=1, sticky="nsew")
    btm_frame.grid(row=3, sticky="ew")

    center.rowconfigure(0, minsize=250, weight=1)
    center.columnconfigure(1, weight=1)

    txt_edit = tk.Text(center)
    fr_buttons = tk.Frame(center, relief=tk.RAISED, bd=2)
    btn_open = tk.Button(fr_buttons, text="Save", command=lambda:text_model.set_text(txt_edit.get(1.0, tk.END)))
    scroll = Scrollbar(center, command=txt_edit.yview)
    txt_edit.configure(yscrollcommand=scroll.set)

    with open('translated.txt', 'r') as text:
        tx = text.read()
        txt_edit.insert(tk.END, tx)

    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")
    scroll.grid(row=0, column=2, sticky='ns')

    # next = Button(btm_frame, text ="Next",
    #         command = lambda : pass)
    # next.pack(side='right', padx=8, pady=5)