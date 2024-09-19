# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : trackSelectGUI
# File name     : trackSelectGUI.py
# Purpose       : provides GUI to select the tracks in a MIDI file.
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : September 17th, 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
#from commons import *

import mido
import tkinter as tk
from tkinter import ttk



# =============================================================================
# Main code
# =============================================================================
def centerWindow(container) :
  
  # Ensure widgets are updated before calculating size
  container.update_idletasks()
  
  w = container.winfo_reqwidth()
  h = container.winfo_reqheight()

  screen_width = container.winfo_screenwidth()
  screen_height = container.winfo_screenheight()

  x = (screen_width - w) // 2
  y = (screen_height - h) // 2

  container.geometry(f"{w}x{h}+{x}+{y}")



midiFile = "./songs/Rachmaninoff_Piano_Concerto_No_3_Op_30_1st_Movement.mid"
#midiFile = "./songs/Rachmaninoff_Moment_Musical_Op_16_No_6.mid"
mid = mido.MidiFile(midiFile)


nTracks = len(mid.tracks)
nNotes = [0 for _ in range(nTracks)]

print(f"[DEBUG] Tracks: {nTracks}")

# Loop on the tracks, decode the MIDI messages
trackList = []
for (trackNumber, track) in enumerate(mid.tracks) :
  
  nNotes[trackNumber] = 0
  for msg in track :
  
    if ((msg.type == 'note_on') and (msg.velocity > 0)) :
      nNotes[trackNumber] += 1
      
  s = f"Track {trackNumber} ({nNotes[trackNumber]} notes)"
  trackList.append(f"{s : <35}{'' : >7}")






def show() :

  def on_quit() : 
    print("That's all folks.")
    root.destroy()

  def on_setLeft(event) : 
    print("To the left hand!")
    # trackLst.delete(0)  # Remove the current content
    # trackLst.insert(0, "aaa")  # Insert new content at the first index
    sel = trackLst.curselection()
    print(f"Sel = {sel}")



  def on_setRight(event) : 
    print("To the right hand!")

  def on_generate() :
    print("TODO")

  def on_downKey(event) :
    if not trackLst.curselection() :
      
      trackLst.selection_set(0)
      
      trackLst.activate(0)

      trackLst.focus_set()




  root = tk.Tk()
  root.title("Track selection")
  root.resizable(0, 0)

  content = ttk.Frame(root, padding = 20)

  choices = [f"{'Track 1 (5443 notes)' : <35}{'[LEFT]' : >7}",
            f"{'Track 2 (5443 notes)' : <35}{'[RIGHT]' : >7}",
            f"{'Track 3 (10 notes)' : <35}{'' : >7}",
            ]
  trackListVar = tk.StringVar(value = trackList)

  availableLbl = ttk.Label(content, text = "Available tracks:")
  trackLst = tk.Listbox(content, listvariable = trackListVar, width = 50, font = ("Consolas", 10))

  setLeftButton = ttk.Button(content, text = "Assign track to Left hand")
  setRightButton = ttk.Button(content, text = "Assign track to Right hand")

  generateButton = ttk.Button(content, text = "Generate", command = on_generate, default = "active")
  quitButton = ttk.Button(content, text = "Quit", command = on_quit)

  content.grid(column = 0, row = 0)

  availableLbl.grid(column = 0, row = 0, columnspan = 3, rowspan = 1, sticky = (tk.W))
  trackLst.grid(column = 0, row = 1, columnspan = 3, rowspan = 1)
  setLeftButton.grid(column = 0, row = 3, sticky = (tk.W, tk.N), pady = (10, 30))
  setRightButton.grid(column = 2, row = 3, sticky = (tk.E, tk.N), pady = (10, 30))
  quitButton.grid(column = 0, row = 4, sticky = (tk.W, tk.S))
  generateButton.grid(column = 2, row = 4, sticky = (tk.E, tk.S))


  # Bindings
  root.bind('<Escape>', lambda event: on_quit())
  root.bind("<Return>", lambda event = None : generateButton.invoke())
  root.bind('<Left>', on_setLeft)
  root.bind('<Right>', on_setRight)
  root.bind('<Down>', on_downKey)

  centerWindow(root)


  root.mainloop()



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  show()
