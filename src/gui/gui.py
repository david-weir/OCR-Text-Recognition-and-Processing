from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from upload_page import *
from edit_page import *
from translate_page import *
from options_page import *

#https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
class OCRApp(Tk):
    
    def __init__(self, *args, **kwargs): # init for OCRApp

        Tk.__init__(self, *args, **kwargs) # init for Tk
        
        self.geometry('650x400') # set size and title of the gui
        self.title("OCR Text to Speech Reading Aid")
        
        # creating a container
        container = Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        # create an array for the frames
        self.frames = {}


        for F in (UploadPage, EditPage, TranslatePage, OptionsPage):
            frame = F(container, self) #create a container for each page 
            self.frames[F] = frame # add each frame into the array

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(UploadPage)


    def show_frame(self, cont): # raise the frame passed to the function
        frame = self.frames[cont]
        frame.tkraise()


app = OCRApp()
app.mainloop() # run the app

