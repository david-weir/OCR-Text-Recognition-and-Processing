import tkinter as tk
from tkinter import *
from pygame import mixer
from textModel import *
import shutil

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import convert

paused = False
playing = False

def begin_play(dictionary, track_list, window):
    global playing
    playing = True
    track = track_list.get(0)
    mixer.music.load(dictionary[track])
    mixer.music.play()

    track_list.activate(0)
    track_list.selection_set(0, last=None)
    play_all(track_list, dictionary, window)

def play_all(track_list, dictionary, window):
    global playing
    while playing:
        if not mixer.music.get_busy() and not paused:
            play_next_track(track_list, dictionary)
        window.update()

def play_next_track(track_list, dictionary):
    track_index = track_list.curselection()[0]+1
    if track_index < len(dictionary):
        next_track = track_list.get(track_index)
        
        mixer.music.load(dictionary[next_track])
        mixer.music.play()

        track_list.selection_clear(0, tk.END)
        track_list.activate(track_index)
        track_list.selection_set(track_index, last=None)

def skip(track_list, dictionary):
    mixer.music.stop()
    play_next_track(track_list, dictionary)

def previous(track_list, dictionary):
    mixer.music.stop()
    track_index = track_list.curselection()[0]
    previous_track = dictionary[track_index]
    print(previous_track)
    if track_index >= 0 and track_index < len(dictionary):
        mixer.music.load(dictionary[previous_track])
        mixer.music.play()

        track_list.selection_clear(0, tk.END)
        track_list.activate(track_index)
        track_list.selection_set(track_index, last=None)

def pause():
    global paused
    if not paused:
        mixer.music.pause()
        paused = True
    else:
        mixer.music.unpause()
        paused = False

def select_track(track_list, dictionary):  
    track_index = track_list.curselection()[0]
    mixer.music.stop()

    track = track_list.get(track_index)
    track_list.selection_clear(ACTIVE)
    mixer.music.load(dictionary[track])
    mixer.music.play()

def stop(track_list):
    mixer.music.stop()
    track_list.selection_clear(ACTIVE)

def quit_mp3player():
    global playing
    playing = False
    mixer.music.stop()

def delete_folder():
    directory = 'mp3_segments'
    current_dir = os.getcwd()

    path = os.path.join(current_dir, directory)
    shutil.rmtree(path)

def create_mp3s(file, track_list):
    dictionary = {}
    try:
        os.mkdir('mp3_segments')
    except OSError:
        delete_folder()
        os.mkdir('mp3_segments')

    mp3 = text_model.get_output_file()
    tracks = convert.split_txtfile(mp3, 'mp3_segments')
    for track in tracks:
        rec = convert.download_mp3(text_model.get_curr_language(), track)
        if file:
            stripped_name = rec.replace("mp3_segments/", "").replace(".mp3", "")
            name = "{} - {}".format(file, stripped_name)
            track_list.insert(END, name)
            dictionary[name] = rec
        else:
            stripped_name = rec.replace("mp3_segments/", "").replace(".mp3", "")
            track_list.insert(END, stripped_name)
            dictionary[stripped_name] = rec

    return dictionary

def popup_window(file):
    window = Toplevel()
    window.title("MP3 player")
    mixer.init()
    track_list = Listbox(window, bg='black', fg='white', width=50, selectbackground='green', selectforeground='black')
    track_list.pack(pady=20, padx=20)

    dictionary = create_mp3s(file, track_list)

    rewind_btn = PhotoImage(file='images/rewind.png') 
    pause_btn = PhotoImage(file='images/pause.png')
    skip_btn = PhotoImage(file='images/skip.png')

    controls = Frame(window)
    controls.pack()

    rewind_button = Label(controls, image=rewind_btn, borderwidth=0, highlightthickness=0)
    skip_button = Label(controls, image=skip_btn, borderwidth=0, highlightthickness=0)
    pause_button = Label(controls, image=pause_btn, borderwidth=0, highlightthickness=0)

    rewind_button.image = rewind_btn
    skip_button.image = skip_btn
    pause_button.image = pause_btn

    track_list.bind("<<ListboxSelect>>", lambda x: select_track(track_list=track_list, dictionary=dictionary))
    rewind_button.bind('<Button>', lambda x: previous(track_list, dictionary))
    skip_button.bind('<Button>', lambda x: skip(track_list, dictionary))
    pause_button.bind('<Button>', lambda x: begin_play(dictionary, track_list, window))

    rewind_button.grid(row=0, column=0, padx=10)
    skip_button.grid(row=0, column=2, padx=10)
    pause_button.grid(row=0, column=1, padx=10)

    button_close = tk.Button(window, text="Close", command= lambda: {quit_mp3player(), delete_folder(), window.destroy()})
    button_close.pack(pady=10)