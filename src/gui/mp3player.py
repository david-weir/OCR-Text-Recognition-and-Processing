import tkinter as tk
from tkinter import *
from pygame import mixer, event, time
import tkinter.font as font
from tkinter import filedialog
from textModel import *
from pathlib import Path


# global skipped
# skipped = False

def play(track_list):
    # path = str(Path.cwd()) + "/" + track_list.get(ACTIVE)
    # global skipped
    # current = track_list.curselection()
    # curr = current
    # print(current, current[0])
    # mixer.music.load(path)
    # mixer.music.play(loops=0)
    # while mixer.music.get_busy():   
    #    time.Clock().tick(1)
    # for track in range(current[0]+1, track_list.size()):
    #     if skipped == True:
    #         break
    #     path = str(Path.cwd()) + "/" + track_list.get(track)
    #     print(path, track)
    #     mixer.music.load(path)
    #     mixer.music.play(loops=0)
    #     # # curr = curr[0]+1
    #     while mixer.music.get_busy():   
    #         time.Clock().tick(1)
    #     skip_track(track_list)
    # skipped = False
    # mixer.music.set_endevent(path.SONG_END)
    song = track_list.get(ACTIVE)
    track = str(Path.cwd()) + "/" + song

    mixer.music.load(track)
    mixer.music.play(loops=0)
    next = track_list.curselection()[0]+1
    mixer.music.queue(str(Path.cwd()) + "/" + track_list.get(next))
    # mixer.music.set_endevent(song.SONG_END)

global paused
paused = False

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
    track_list.selection_set(prev_one, last=None)

# def check_music():
#     """
#     Listens to END_MUSIC event and triggers next song to play if current 
#     song has finished
#     :return: None
#     """
#     for event in event.get():
#         if event.type == self.SONG_END:
#             self.next_song()

def popup_window():
    window = Toplevel()
    mixer.init()

    track_list = Listbox(window, bg='black', fg='white', width=60, selectbackground='green', selectforeground='black')
    track_list.pack(pady=20)
    track_list.insert(END, "test.mp3")
    track_list.insert(END, "speech.mp3")

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

    rewind_button.bind('<Button>', lambda x: previous_track(track_list))
    skip_button.bind('<Button>', lambda x: skip_track(track_list))
    play_button.bind('<Button>', lambda x: play(track_list))
    pause_button.bind('<Button>', lambda x: pause(paused))
    stop_button.bind('<Button>', lambda x: stop(track_list))

    rewind_button.grid(row=0, column=0, padx=10)
    skip_button.grid(row=0, column=1, padx=10)
    play_button.grid(row=0, column=2, padx=10)
    pause_button.grid(row=0, column=3, padx=10)
    stop_button.grid(row=0, column=4, padx=10)

    button_close = tk.Button(window, text="Close", command=window.destroy)
    button_close.pack(fill='x')
