# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : trackSelectionGUI
# File name     : trackSelectionGUI.py
# File type     : Python script (Python 3)
# Purpose       : provides GUI to select the tracks in a MIDI file.
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Tuesday, 17 September 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
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
def new() :
  return TrackSelectionGUI()



class Track :
  def __init__(self):
    self.name = ""
    self.nNotes = 0



class TrackSelectionGUI :

  """
  TODO
  """

  def __init__(self) :
    self.midiFile = ""
    self.nTracks = 0
    self.midiTracks = []
    
    self.leftTrack = -1
    self.rightTrack = -1

    self.root = None
    
    


  # ---------------------------------------------------------------------------
  # METHOD trackSelectionGUI.load(midiFile)
  # ---------------------------------------------------------------------------
  def load(self, midiFile) :
    """
    Reads the MIDI file and initialises the GUI.
    """

    self.midiFile = midiFile

    midiObj = mido.MidiFile(midiFile)
    self.nTracks = len(midiObj.tracks)
    print(f"[INFO] Found tracks: {self.nTracks}")

    self.tracks = [Track() for _ in range(self.nTracks)]

    # Loop on the tracks, decode the MIDI messages
    self.displayTrackList = []
    for (i, track) in enumerate(midiObj.tracks) :

      # Read the notes
      self.tracks[i].nNotes = 0
      for msg in track :
        if ((msg.type == 'note_on') and (msg.velocity > 0)) :
          self.tracks[i].nNotes += 1

      # Read the name of the track
      sName = track.name.split("\x00")[0]
      # self.tracks[i].name = track.name.split("\x00")[0]

      if (len(sName) > MAX_TRACK_NAME_LENGTH) :
        self.tracks[i].name = sName[0:(MAX_TRACK_NAME_LENGTH-3)] + "..."
      else :
        self.tracks[i].name = sName
      
      # Add the track to the 'trackList' widget
      s = f"Track {i} - {self.tracks[i].name} ({self.tracks[i].nNotes} notes)"
      self.displayTrackList.append(f"{s : <35}{'' : >7}")



  # ---------------------------------------------------------------------------
  # METHOD trackSelectionGUI.show()
  # ---------------------------------------------------------------------------
  def show(self) :
    """
    Shows the track selection GUI.
    Returns the index of the selected MIDI tracks upon exiting.
    """
    
    self.root = tk.Tk()
    self.root.title("Track selection")
    self.root.resizable(0, 0)

    content = ttk.Frame(self.root, padding = 20)

    availableLbl = ttk.Label(content, text = "Available tracks:")
    trackListVar = tk.StringVar(value = self.displayTrackList)
    self.trackListWidget = tk.Listbox(content, listvariable = trackListVar, width = 50, font = ("Consolas", 10))

    setLeftButton = ttk.Button(content, text = "Assign track to Left hand", command = self.CLBK_onLeftKey)
    setRightButton = ttk.Button(content, text = "Assign track to Right hand", command = self.CLBK_onRightKey)

    generateButton = ttk.Button(content, text = "Generate", command = self.CLBK_onGenerate, default = "active")
    quitButton = ttk.Button(content, text = "Quit", command = self.CLBK_onQuit)

    content.grid(column = 0, row = 0)

    availableLbl.grid(column = 0, row = 0, columnspan = 3, rowspan = 1, sticky = (tk.W))
    self.trackListWidget.grid(column = 0, row = 1, columnspan = 3, rowspan = 1)
    setLeftButton.grid(column = 0, row = 3, sticky = (tk.W, tk.N), pady = (10, 30))
    setRightButton.grid(column = 2, row = 3, sticky = (tk.E, tk.N), pady = (10, 30))
    quitButton.grid(column = 0, row = 4, sticky = (tk.W, tk.S))
    generateButton.grid(column = 2, row = 4, sticky = (tk.E, tk.S))


    # Bindings
    self.root.bind('<Escape>',  self.CLBK_onQuit)
    self.root.bind("<Return>",  self.CLBK_onGenerate)
    self.root.bind('<Left>',    self.CLBK_onLeftKey)
    self.root.bind('<Right>',   self.CLBK_onRightKey)
    self.root.bind('<Down>',    self.CLBK_onDownKey)
    self.root.bind('<q>',       self.CLBK_onQuit)

    self.centerWindow()
    self.root.mainloop()

    return (self.leftTrack, self.rightTrack)



  # ---------------------------------------------------------------------------
  # METHOD trackSelectionGUI.centerWindow()
  # ---------------------------------------------------------------------------
  def centerWindow(self) :
    """
    Centers the GUI on screen.
    """
    
    self.root.update_idletasks()
    
    w = self.root.winfo_reqwidth()
    h = self.root.winfo_reqheight()

    screen_width = self.root.winfo_screenwidth()
    screen_height = self.root.winfo_screenheight()

    x = (screen_width - w) // 2
    y = (screen_height - h) // 2

    self.root.geometry(f"{w}x{h}+{x}+{y}")



  # ---------------------------------------------------------------------------
  # METHOD trackSelectionGUI.CLBK_onQuit()
  # ---------------------------------------------------------------------------
  def CLBK_onQuit(self, event = None) :
    exit()

  # ---------------------------------------------------------------------------
  # METHOD trackSelectionGUI.CLBK_onLeftKey()
  # ---------------------------------------------------------------------------
  def CLBK_onLeftKey(self, event = None) : 
    ret = self.trackListWidget.curselection()
    if (len(ret) > 0) :
      
      (sel, *rem) = ret
      
      # Edit the 'new' left hand
      self.trackListWidget.delete(sel)
      s = f"Track {sel} - {self.tracks[sel].name} ({self.tracks[sel].nNotes} notes)"
      self.trackListWidget.insert(sel, f"{s : <35}{'[LEFT]' : >7}")
      self.trackListWidget.selection_set(sel)
      self.trackListWidget.activate(sel)

      # Edit the previous left hand if it was already assigned
      if (self.leftTrack != -1) :
        self.trackListWidget.delete(self.leftTrack)
        s = f"Track {self.leftTrack} - {self.tracks[self.leftTrack].name} ({self.tracks[self.leftTrack].nNotes} notes)"
        self.trackListWidget.insert(self.leftTrack, f"{s : <35}{'' : >7}")
        
      self.leftTrack = sel

    else : 
      print(f"Please select a track before assigning.")

  # ---------------------------------------------------------------------------
  # METHOD trackSelectionGUI.CLBK_onRightKey()
  # ---------------------------------------------------------------------------
  def CLBK_onRightKey(self, event = None) :
    ret = self.trackListWidget.curselection()

    # If something is selected
    if (len(ret) > 0) :
      
      (sel, *rem) = ret
      
      # Edit the 'new' right hand
      self.trackListWidget.delete(sel)
      s = f"Track {sel} - {self.tracks[sel].name} ({self.tracks[sel].nNotes} notes)"
      self.trackListWidget.insert(sel, f"{s : <35}{'[RIGHT]' : >7}")
      self.trackListWidget.selection_set(sel)
      self.trackListWidget.activate(sel)

      # Edit the previous right hand if it was already assigned
      if (self.rightTrack != -1) :
        self.trackListWidget.delete(self.rightTrack)
        s = f"Track {self.rightTrack} - {self.tracks[self.rightTrack].name} ({self.tracks[self.rightTrack].nNotes} notes)"
        self.trackListWidget.insert(self.rightTrack, f"{s : <35}{'' : >7}")
        
      self.rightTrack = sel

    else : 
      print(f"Please select a track before assigning.")

  # ---------------------------------------------------------------------------
  # METHOD trackSelectionGUI.CLBK_onGenerate()
  # ---------------------------------------------------------------------------
  def CLBK_onDownKey(self, event = None) :
    if not(self.trackListWidget.curselection()) :
      self.trackListWidget.selection_set(0)
      self.trackListWidget.activate(0)
      self.trackListWidget.focus_set()

  # ---------------------------------------------------------------------------
  # METHOD trackSelectionGUI.CLBK_onGenerate()
  # ---------------------------------------------------------------------------
  def CLBK_onGenerate(self, event = None) :
    self.root.destroy()



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  gui = new()
  gui.load("./songs/Rachmaninoff_Piano_Concerto_No_3_Op_30_1st_Movement.mid")
  midiTracks = gui.show()
  print(f"MIDI tracks: {midiTracks}")
