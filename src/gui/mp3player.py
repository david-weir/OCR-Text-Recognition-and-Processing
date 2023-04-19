import tkinter as tk
from tkinter import *
from pygame import mixer
from textModel import *
import shutil

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import convert

paused = False
current_track = 0
playing = True

def play(index, playlist):
    global current_track
    current_track = index
    mixer.music.load(playlist[current_track])
    mixer.music.play()

def play_next_track(track_list, playlist):
    global current_track
    current_track += 1

    if current_track < len(playlist):
        mixer.music.load(playlist[current_track])
        mixer.music.play()

    track_list.selection_clear(0, tk.END)
    track_list.activate(current_track)
    track_list.selection_set(current_track, last=None)

def skip(track_list, playlist):
    global current_track
    mixer.music.stop()

    play_next_track(track_list, playlist)

def previous(track_list, playlist):
    mixer.music.stop()
    global current_track
    current_track -= 1

    if current_track >= 0 and current_track < len(playlist):
        mixer.music.load(playlist[current_track])
        mixer.music.play()

    track_list.selection_clear(0, tk.END)
    track_list.activate(current_track)
    track_list.selection_set(current_track, last=None)

def pause():
    global paused
    if not paused:
        mixer.music.pause()
        paused = True
    else:
        mixer.music.unpause()
        paused = False

def select_track(track_list, playlist):  
    track = track_list.curselection()[0]
    if track:
        mixer.music.stop()
        play(track, playlist)

def stop(track_list):
    mixer.music.stop()
    track_list.selection_clear(ACTIVE)

def quit_mp3player():
    global playing
    playing = False
    mixer.music.stop()

def create_mp3s(file, track_list):
    playlist = []

    os.mkdir('mp3_segments')

    mp3 = text_model.get_output_file()
    tracks = convert.split_txtfile(mp3)
    for track in tracks:
        rec = convert.download_split_mp3(text_model.get_curr_language(), track, "mp3_segments") #language
        if file:
            stripped_name = rec.replace("mp3_segments/", "").replace(".mp3", "")
            name = "{} - {}".format(file, stripped_name)
            track_list.insert(END, name)
        else:
            stripped_name = rec.replace("mp3_segments/", "").replace(".mp3", "")
            track_list.insert(END, stripped_name)
        playlist.append(rec)

    return playlist

def delete_folder():
    directory = 'mp3_segments'
    current_dir = os.getcwd()

    path = os.path.join(current_dir, directory)
    shutil.rmtree(path)

def popup_window(file):
    window = Toplevel()
    window.title("MP3 player")
    mixer.init()
    track_list = Listbox(window, bg='black', fg='white', width=50, selectbackground='green', selectforeground='black')

    playlist = create_mp3s(file, track_list)

    track_list.pack(pady=20, padx=20)
    track_list.bind("<<ListboxSelect>>", lambda x: select_track(track_list=track_list, playlist=playlist))

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

    rewind_button.bind('<Button>', lambda x: previous(track_list, playlist))
    skip_button.bind('<Button>', lambda x: skip(track_list, playlist))
    pause_button.bind('<Button>', lambda x: pause())

    rewind_button.grid(row=0, column=0, padx=10)
    skip_button.grid(row=0, column=2, padx=10)
    pause_button.grid(row=0, column=1, padx=10)

    button_close = tk.Button(window, text="Close", command= lambda: {quit_mp3player(), delete_folder(), window.destroy()})
    button_close.pack(pady=10)

    mixer.music.load(playlist[current_track])
    mixer.music.play()

    track_list.activate(current_track)
    track_list.selection_set(current_track, last=None)

    while playing == True:
        if not mixer.music.get_busy() and not paused:
            play_next_track(track_list, playlist)
        window.update()