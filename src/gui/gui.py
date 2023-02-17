from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from upload_page import *
from detection_page import *
from edit_page import *
from translate_page import *
from options_page import *

class OCRApp(Tk):
    
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        
        # __init__ function for class Tk
        Tk.__init__(self, *args, **kwargs)
        
        self.geometry('500x400')
        self.title("OCR Text to Speech Reading Aid")
        
        # creating a container
        container = Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (UploadPage, DetectionPage, EditPage, TranslatePage, OptionsPage):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(UploadPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Driver Code
app = OCRApp()
app.mainloop()

