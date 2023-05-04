import tkinter as tk
from tkinter import *
from pygame import mixer
from textModel import *
import shutil

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import convert

# global variables
paused = False
playing = False

# on play, begin from first track
def begin_play(dictionary, track_list, window):
    global playing
    playing = True # set the global variable to true
    track = track_list.get(0) # get the first track, load it and play it
    mixer.music.load(dictionary[track])
    mixer.music.play()

    track_list.activate(0)
    track_list.selection_set(0, last=None)
    play_all(track_list, dictionary, window) # once first track finishes, move on to the next

# load a new track after the current track ends
def play_all(track_list, dictionary, window):
    global playing
    while playing:
        if not mixer.music.get_busy() and not paused: # if there isnt currently a track playing, or it isnt paused
            play_next_track(track_list, dictionary)
        window.update() # update window to see the new track activated

# play the track that follows the current track
def play_next_track(track_list, dictionary):
    track_index = track_list.curselection()[0]+1
    if track_index < len(dictionary): # if the current track is not the last track
        next_track = track_list.get(track_index) # get the track with index of the cur track plus one
        
        mixer.music.load(dictionary[next_track])
        mixer.music.play()

        track_list.selection_clear(0, tk.END) # show that the new track is playing
        track_list.activate(track_index)
        track_list.selection_set(track_index, last=None)

# on skip, play the next track
def skip(track_list, dictionary):
    mixer.music.stop()
    play_next_track(track_list, dictionary)

# on the back button, play the track before the current track
def previous(track_list, dictionary):
    mixer.music.stop()
    track_index = track_list.curselection()[0]
    previous_track = dictionary[track_index]
    print(previous_track)
    if track_index >= 0 and track_index < len(dictionary): # make sure we arent going back past the first track
        mixer.music.load(dictionary[previous_track])
        mixer.music.play()

        track_list.selection_clear(0, tk.END)
        track_list.activate(track_index)
        track_list.selection_set(track_index, last=None)

# pause and unpause the track playing
def pause():
    global paused
    if not paused:
        mixer.music.pause()
        paused = True
    else:
        mixer.music.unpause()
        paused = False

# click on a track from the listbox to play it
def select_track(track_list, dictionary, window):  
    global playing
    
    track_index = track_list.curselection()[0]
    mixer.music.stop()

    track = track_list.get(track_index)
    track_list.selection_clear(ACTIVE)
    mixer.music.load(dictionary[track])
    mixer.music.play()

    if not playing: # if it hasnt been set to play tracks one after the other
        play_all(track_list, dictionary, window)

# stop the recording from playing when closing the window
def quit_mp3player():
    global playing
    playing = False
    mixer.music.stop()

# delete the temporary folder storing the split up mp3 recording
def delete_folder():
    directory = 'mp3_segments'
    current_dir = os.getcwd()

    path = os.path.join(current_dir, directory)
    shutil.rmtree(path)

# create the split up mp3 recordings
def create_mp3s(file, track_list):
    dictionary = {}
    try: # create a dictionary for the recordings
        os.mkdir('mp3_segments')
    except OSError:
        delete_folder()
        os.mkdir('mp3_segments')

    mp3 = text_model.get_output_file() # get the file to be converted to mp3
    tracks = convert.split_txtfile(mp3, 'mp3_segments') # split the textfile and place them in the folder
    for track in tracks:
        rec = convert.download_mp3(text_model.get_curr_language(), track) # convert each chunk of text into mp3
        if file: # if the user passed a filename to the player
            stripped_name = rec.replace("mp3_segments/", "").replace(".mp3", "")
            name = "{} - {}".format(file, stripped_name)
            track_list.insert(END, name) # save the file name and file path into the dictionary
            dictionary[name] = rec
        else:
            stripped_name = rec.replace("mp3_segments/", "").replace(".mp3", "")
            track_list.insert(END, stripped_name)
            dictionary[stripped_name] = rec

    return dictionary # dictionary shows file name and path

# tasks for when the window is being closed
def closing(window):
    quit_mp3player()
    delete_folder()
    window.destroy()

# create popup window of the mp3 player
def popup_window(file):
    window = Toplevel()
    window.title("MP3 player")
    mixer.init()

    # create the list box to show all the possible tracks
    track_list = Listbox(window, bg='black', fg='white', width=50, selectbackground='green', selectforeground='black')
    track_list.pack(pady=20, padx=20)

    dictionary = create_mp3s(file, track_list)

    # image files for the buttons
    rewind_btn = PhotoImage(file='images/back.png') 
    pause_btn = PhotoImage(file='images/pause.png')
    skip_btn = PhotoImage(file='images/skip.png')
    play_btn = PhotoImage(file='images/play.png')

    controls = Frame(window) # frame to store the buttons
    controls.pack()

    # create label for each button with the image as the label
    rewind_button = Label(controls, image=rewind_btn, borderwidth=0, highlightthickness=0)
    skip_button = Label(controls, image=skip_btn, borderwidth=0, highlightthickness=0)
    pause_button = Label(controls, image=pause_btn, borderwidth=0, highlightthickness=0)
    play_button = Label(controls, image=play_btn, borderwidth=0, highlightthickness=0)

    rewind_button.image = rewind_btn
    skip_button.image = skip_btn
    pause_button.image = pause_btn
    play_button.image = play_btn

    # bind functions to the different elements of the program
    track_list.bind("<<ListboxSelect>>", lambda x: select_track(track_list, dictionary, window))
    rewind_button.bind('<Button>', lambda x: previous(track_list, dictionary))
    skip_button.bind('<Button>', lambda x: skip(track_list, dictionary))
    pause_button.bind('<Button>', lambda x: pause())
    play_button.bind('<Button>', lambda x: begin_play(dictionary, track_list, window))

    # place the images inside the controls frame
    rewind_button.grid(row=0, column=0, padx=10)
    play_button.grid(row=0, column=1, padx=10)
    pause_button.grid(row=0, column=2, padx=10)
    skip_button.grid(row=0, column=3, padx=10)

    # when clicking x on the wondow, delete the window and everything in it
    window.protocol("WM_DELETE_WINDOW", lambda : closing(window))