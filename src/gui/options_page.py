from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import edit_page
import upload_page
import mp3player

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class OptionsPage(Frame):
    
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

        pdf_option = IntVar()
        mp3_option = IntVar()
        pdf_frame = tk.Frame(center, height=40)
        audio_frame = tk.Frame(center, height=40)

        Checkbutton(center, text="Convert to PDF", variable=pdf_option, onvalue=1, offvalue=0).place(relx=0.5, rely=0.3, anchor=CENTER)
        Checkbutton(center, text="Convert to MP3", variable=mp3_option, onvalue=1, offvalue=0).place(relx=0.5, rely=0.4, anchor=CENTER)

        def show_options_frame():
            if pdf_option.get() == 1 and not bool(pdf_frame.winfo_ismapped()):
                pdf_frame.pack(side='bottom', fill='both')
                
                pdf_filename = StringVar()
                name_label = Label(pdf_frame, text='PDF filename:')
                name_label.pack(side='left')
                Entry(pdf_frame, textvariable=pdf_filename).pack(side='left', padx=5)

                Button(pdf_frame, text="Download").pack(side='right', padx=5)

            if mp3_option.get() == 1 and not bool(audio_frame.winfo_ismapped()):
                audio_frame.pack(side='bottom', fill='both')
                
                audio_filename = StringVar()
                audio_name_label = Label(audio_frame, text='mp3 filename:')
                audio_name_label.pack(side='left')
                Entry(audio_frame, textvariable=audio_filename).pack(side='left', padx=5)

                Button(audio_frame, text="Download").pack(side='right', padx=5)
                Button(audio_frame, text="Play", command=lambda: mp3player.popup_window()).pack(side='right', padx=5)
        
        Button(center, text="Confirm", command= lambda: show_options_frame()).place(relx=0.5, rely=0.6, anchor=CENTER)


        previous = Button(btm_frame, text="Back",
                   command = lambda : controller.show_frame(edit_page.EditPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text="Next",
               command = lambda : controller.show_frame(upload_page.UploadPage))
        next.pack(side='right', padx=8, pady=5)