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

  leftTrack = -1; rightTrack = -1

  def on_quit() : 
    root.destroy()

  def on_setLeft(event) : 
    ret = trackLst.curselection()

    if (len(ret) > 0) :
      
      # Verify that left hand is not already assigned
      
      (sel, *rem) = ret
      trackLst.delete(sel)
      s = f"Track {sel} ({nNotes[sel]} notes)"
      trackLst.insert(sel, f"{s : <35}{'[LEFT]' : >7}")
      trackLst.selection_set(sel)
      trackLst.activate(sel)





  def on_setRight(event) : 
    print("To the right hand!")
    sel = trackLst.curselection()
    print(f"Sel = {sel}")

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

  availableLbl = ttk.Label(content, text = "Available tracks:")
  trackListVar = tk.StringVar(value = trackList)
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
