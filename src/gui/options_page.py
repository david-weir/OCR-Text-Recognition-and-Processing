from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import edit_page
import upload_page
import mp3player

from textModel import *

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import convert

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

        # create int variable that will be used in the checkbutton
        pdf_option = IntVar()
        mp3_option = IntVar()

        pdf_frame = tk.Frame(center, height=40) # create frames for each output option
        audio_frame = tk.Frame(center, height=40)

        # create checkbuttons to choose which output option you want
        Checkbutton(center, text="Convert to PDF", variable=pdf_option, onvalue=1, offvalue=0).place(relx=0.5, rely=0.3, anchor=CENTER)
        Checkbutton(center, text="Convert to MP3", variable=mp3_option, onvalue=1, offvalue=0).place(relx=0.5, rely=0.4, anchor=CENTER)

        # function to display the options frames
        def show_options_frame():
            # if 'convert to pdf' has been selected and the frame isnt already present
            if pdf_option.get() == 1 and not bool(pdf_frame.winfo_ismapped()):
                pdf_frame.pack(side='bottom', fill='both')
                
                pdf_filename = StringVar()
                name_label = Label(pdf_frame, text='PDF filename:')
                name_label.pack(side='left')
                Entry(pdf_frame, textvariable=pdf_filename).pack(side='left', padx=5) # entry textbox to put in the name of the pdf

                Button(pdf_frame, text="Download", command=lambda: convert.convert_to_pdf(text_model.get_output_file(), pdf_filename.get())).pack(side='right', padx=5) # download the pdf

            # if 'convert to mp3' has been selected and the frame isnt already present
            if mp3_option.get() == 1 and not bool(audio_frame.winfo_ismapped()):
                audio_frame.pack(side='bottom', fill='both')
                
                audio_filename = StringVar()
                audio_name_label = Label(audio_frame, text='mp3 filename:')
                audio_name_label.pack(side='left')
                Entry(audio_frame, textvariable=audio_filename).pack(side='left', padx=5) # enter name for the mp3 recording

                # download the mp3 of the textfile
                Button(audio_frame, text="Download", command=lambda: convert.download_mp3(text_model.get_curr_language(), text_model.get_output_file())).pack(side='right', padx=5)
                # display the mp3 in the mp3 player, but do not download it
                Button(audio_frame, text="Play", command=lambda: mp3player.popup_window(audio_filename.get())).pack(side='right', padx=5)
        
        # once pdf or mp3 options have been selected, confirm to display the respective frames
        Button(center, text="Confirm", command= lambda: show_options_frame()).place(relx=0.5, rely=0.6, anchor=CENTER)


        previous = Button(btm_frame, text="Back",
                   command = lambda : controller.show_frame(edit_page.EditPage))
        previous.pack(side='left', padx=8, pady=5)

        next = Button(btm_frame, text="Finish",
               command = lambda : {controller.show_frame(upload_page.UploadPage), text_model.reset(), self.delete_tmp_files()})
        next.pack(side='right', padx=8, pady=5)

    # function to delete the temporary files that have been created in the process
    def delete_tmp_files(self):
        os.remove('output.txt') # delete the file original text file created
        if os.path.exists('translated.txt'): # delete the translated/summarised textfile if there is one
            os.remove('translated.txt')