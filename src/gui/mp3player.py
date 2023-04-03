import tkinter as tk
from tkinter import *
from pygame import mixer, event, time
import tkinter.font as font
from tkinter import filedialog
from textModel import *
from pathlib import Path
from mutagen.mp3 import MP3
from pydub import AudioSegment

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import convert


"""def play(track_list):

    song = track_list.get(ACTIVE)
    track = str(Path.cwd()) + "/" + song

    mixer.music.load(track)
    mixer.music.play(loops=0)
    next = track_list.curselection()[0]+1
    mixer.music.queue(str(Path.cwd()) + "/" + track_list.get(next))
    # mixer.music.set_endevent(song.SONG_END)

global paused
paused = False
current_song = 0
playing = True

def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		mixer.music.unpause()
		paused = False
	else:
		mixer.music.pause()
		paused = True

def stop(track_list):
    mixer.music.stop()
    track_list.selection_clear(ACTIVE)

def skip_track(track_list):
    # Get the current song tuple number
    next_one = track_list.curselection() 
    # Add one to the current song number
    next_one = next_one[0]+1
    #Grab song title from playlist
    # add directory structure and mp3 to song title
    path = str(Path.cwd()) + "/" + track_list.get(next_one)
    # Load and play song
    mixer.music.load(path)
    mixer.music.play(loops=0)

    track_list.selection_clear(0, END)
    track_list.activate(next_one)
    track_list.selection_set(next_one, last=None)
    # skipped = True

def previous_track(track_list):
    # Get the current song tuple number
    prev_one = track_list.curselection() 
    # Add one to the current song number
    prev_one = prev_one[0]-1
    #Grab song title from playlist
    # add directory structure and mp3 to song title
    path = str(Path.cwd()) + "/" + track_list.get(prev_one)
    # Load and play song
    mixer.music.load(path)
    mixer.music.play(loops=0)

    track_list.selection_clear(0, END)
    track_list.activate(prev_one)
    track_list.selection_set(prev_one, last=None)"""

paused = False
current_track = 0
playing = True

def play(index, playlist):
    global current_track
    current_track = index
    # Load and play the selected song
    mixer.music.load(playlist[current_track])
    mixer.music.play()

# Define a function to play the next song in the playlist
def play_next_track(track_list, playlist):
    global current_track
    current_track += 1
    if current_track >= len(playlist):
        # Restart the playlist if we've reached the end
        current_track = 0
    # Load and play the next song
    mixer.music.load(playlist[current_track])
    mixer.music.play()

    track_list.selection_clear(0, tk.END)
    track_list.activate(current_track)
    track_list.selection_set(current_track, last=None)

# Define a function to skip to the next song in the playlist
def skip(track_list, playlist):
    # Stop the current song
    mixer.music.stop()
    # Play the next song in the playlist
    play_next_track(track_list, playlist)

# Define a function to go back to the previous song in the playlist
def previous(track_list, playlist):
    # Stop the current song
    mixer.music.stop()
    # Go back to the previous song in the playlist
    global current_track
    current_track -= 1
    """change this"""
    if current_track < 0:
        # Go to the last song in the playlist if we're at the beginning
        current_track = len(playlist) - 1
    # Load and play the previous song
    mixer.music.load(playlist[current_track])
    mixer.music.play()

    track_list.selection_clear(0, tk.END)
    track_list.activate(current_track)
    track_list.selection_set(current_track, last=None)

# Define a function to pause the current song
def pause():
    global paused
    if not paused:
        mixer.music.pause()
        paused = True
    else:
        mixer.music.unpause()
        paused = False

def select_track(track_list, playlist): # event, 
    selection = track_list.curselection()
    if selection:
        # Stop the current song
        mixer.music.stop()
        # Play the selected song
        play(selection[0], playlist)

def stop(track_list):
    mixer.music.stop()
    track_list.selection_clear(ACTIVE)

def quit_mp3player():
    global playing
    playing = False
    mixer.music.stop()

def popup_window(file):
    window = Toplevel()
    mixer.init()
    # global playing
    track_list = Listbox(window, bg='black', fg='white', width=60, selectbackground='green', selectforeground='black')

    playlist = []
    mp3 = text_model.get_textfile()
    tracks = convert.split_txtfile(mp3)
    for track in tracks:
        rec = convert.download_mp3("en", track) #language
        track_list.insert(END, rec)
        playlist.append(rec)

    track_list.pack(pady=20)
    track_list.bind("<<ListboxSelect>>", lambda x: select_track(track_list=track_list, playlist=playlist))

    rewind_btn = PhotoImage(file='images/rewind.png') #, height=30, width=30
    play_btn = PhotoImage(file='images/play.png')
    pause_btn = PhotoImage(file='images/pause.png')
    stop_btn = PhotoImage(file='images/stop.png')
    skip_btn = PhotoImage(file='images/skip.png')

    controls = Frame(window)
    controls.pack()

    rewind_button = Label(controls, image=rewind_btn, borderwidth=0, highlightthickness=0)
    skip_button = Label(controls, image=skip_btn, borderwidth=0, highlightthickness=0)
    play_button = Label(controls, image=play_btn, borderwidth=0, highlightthickness=0)
    pause_button = Label(controls, image=pause_btn, borderwidth=0, highlightthickness=0)
    stop_button =  Label(controls, image=stop_btn, borderwidth=0, highlightthickness=0)

    rewind_button.image = rewind_btn
    skip_button.image = skip_btn
    play_button.image = play_btn
    pause_button.image = pause_btn
    stop_button.image = stop_btn

    rewind_button.bind('<Button>', lambda x: previous(track_list, playlist))
    skip_button.bind('<Button>', lambda x: skip(track_list, playlist))
    # play_button.bind('<Button>', lambda x: play(track_list))
    pause_button.bind('<Button>', lambda x: pause) # isnt working for some reason
    stop_button.bind('<Button>', lambda x: stop(track_list)) # doesnt do anything

    rewind_button.grid(row=0, column=0, padx=10)
    skip_button.grid(row=0, column=1, padx=10)
    play_button.grid(row=0, column=2, padx=10)
    pause_button.grid(row=0, column=3, padx=10)
    stop_button.grid(row=0, column=4, padx=10)

    current_track_label = tk.Label(controls, text="Current Song: " + playlist[current_track])
    current_track_label.grid(row=1, column=0)

    button_close = tk.Button(window, text="Close", command= lambda: {quit_mp3player(), window.destroy()})
    button_close.pack(fill='x')

    """move into start playing function?"""
    mixer.music.load(playlist[current_track])
    mixer.music.play()

    track_list.activate(current_track)
    track_list.selection_set(current_track, last=None)

    while playing == True:
        # Check if the current song has finished playing
        if not mixer.music.get_busy() and not paused:
            # Play the next song in the playlist
            play_next_track(track_list, playlist)
        # Update the current song label
        current_track_label.config(text="Currently Playing: " + playlist[current_track])
        # Update the GUI
        window.update()
