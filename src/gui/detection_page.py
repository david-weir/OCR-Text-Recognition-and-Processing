from tkinter import *
from tkinter.ttk import *
import tkinter as tk
#from src.detection import *
import edit_page
import upload_page

class DetectionPage(Frame):
    
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
        dropdown = OptionMenu(center, clicked, *options)
        dropdown.config(width=7)

        lang_codes = {
            "en": "English",
            "fr": "French",
            "de": "German"
        }

        detected = True #will replace with detection function
        if detected == False:
            message = Label(center, text="Failed to Detect Language.").place(relx=0.5, rely=0.4, anchor=CENTER)
            select_message = Label(center, text="Please Select:   ").place(relx=0.4, rely=0.5, anchor=CENTER)
            dropdown.place(relx=0.6, rely=0.5, anchor=CENTER)
            b = Button(center, text="Confirm").place(relx=0.5, rely=0.6, anchor=CENTER)
        else:
            a = Label(center, text="Language Detected: {}".format("French")).place(relx=0.5, rely=0.4, anchor=CENTER)
            b = Button(center, text="Confirm").place(relx=0.5, rely=0.5, anchor=CENTER)



        previous = Button(btm_frame, text="Back",
                   command = lambda : controller.show_frame(upload_page.UploadPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text="Next",
               command = lambda : controller.show_frame(edit_page.EditPage))
        next.pack(side='right', padx=8, pady=5)