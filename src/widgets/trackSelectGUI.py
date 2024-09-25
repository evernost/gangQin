# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : trackSelectGUI
# File name     : trackSelectGUI.py
# Purpose       : provides GUI to select the tracks in a MIDI file.
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Tuesday, 17 September 2024
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
# Constants pool
# =============================================================================
MAX_TRACK_NAME_LENGTH = 10



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


class Track:
  def __init__(self):
    self.name = ""
    self.nNotes = 0
    


nTracks = len(mid.tracks)
print(f"[DEBUG] Tracks: {nTracks}")


tracks = [Track() for _ in range(nTracks)]



# Loop on the tracks, decode the MIDI messages
trackList = []
for (i, track) in enumerate(mid.tracks) :

  # Read the notes
  tracks[i].nNotes = 0
  for msg in track :
    if ((msg.type == 'note_on') and (msg.velocity > 0)) :
      tracks[i].nNotes += 1

  # Read the name of the track
  tracks[i].name = track.name.split("\x00")[0]    
  if (len(tracks[i].name) > MAX_TRACK_NAME_LENGTH) :
    sName = tracks[i].name[0:(MAX_TRACK_NAME_LENGTH-3)] + "..."
  else :
    sName = tracks[i].name
  
  # Add the track to the 'trackList' widget
  s = f"Track {i} - {sName} ({tracks[i].nNotes} notes)"
  trackList.append(f"{s : <35}{'' : >7}")





def show() :

  global leftTrack; global rightTrack
  leftTrack = -1; rightTrack = -1

  def on_quit() : 
    root.destroy()

  def on_setLeft(event = None) : 
    global leftTrack
    ret = trackLst.curselection()

    # If something is selected
    if (len(ret) > 0) :
      
      (sel, *rem) = ret
      
      # Edit the 'new' left hand
      trackLst.delete(sel)
      s = f"Track {sel} ({tracks[sel].nNotes} notes)"
      trackLst.insert(sel, f"{s : <35}{'[LEFT]' : >7}")
      trackLst.selection_set(sel)
      trackLst.activate(sel)

      # Verify that left hand is not already assigned
      if (leftTrack != -1) :
        # Edit the 'old' left hand
        trackLst.delete(leftTrack)
        s = f"Track {leftTrack} ({tracks[sel].nNotes} notes)"
        trackLst.insert(leftTrack, f"{s : <35}{'' : >7}")
        
      leftTrack = sel

    else : 
      print(f"Please select the track you want to assign to the left hand.")



  def on_setRight(event = None) : 
    global rightTrack
    
    ret = trackLst.curselection()

    # If something is selected
    if (len(ret) > 0) :
      
      (sel, *rem) = ret
      
      # Edit the 'new' left hand
      trackLst.delete(sel)
      s = f"Track {sel} ({tracks[sel].nNotes} notes)"
      trackLst.insert(sel, f"{s : <35}{'[RIGHT]' : >7}")
      trackLst.selection_set(sel)
      trackLst.activate(sel)

      # Verify that left hand is not already assigned
      if (rightTrack != -1) :
        # Edit the 'old' left hand
        trackLst.delete(rightTrack)
        s = f"Track {rightTrack} ({tracks[sel].nNotes} notes)"
        trackLst.insert(rightTrack, f"{s : <35}{'' : >7}")
        
      rightTrack = sel

    else : 
      print(f"Please select the track you want to assign to the right hand.")

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

  setLeftButton = ttk.Button(content, text = "Assign track to Left hand", command = on_setLeft)
  setRightButton = ttk.Button(content, text = "Assign track to Right hand", command = on_setRight)

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
