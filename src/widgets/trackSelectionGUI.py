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
# EXTERNAL LIBS
# =============================================================================
import mido
import tkinter as tk
from tkinter import ttk



# =============================================================================
# CONSTANTS
# =============================================================================
MAX_TRACK_NAME_LENGTH = 10

# Default channel assignment (should work for most MIDI files)
# When True:
# - channel 0 -> Right hand
# - channel 1 -> Left hand
ASSIGN_DEFAULT = True



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class TrackSelectionGUI :

  """
  TRACKSELECTIONGUI object

  Self-contained class containing all the necessary functions to show the MIDI
  Track selection GUI on screen.

  Call the app, it will return a dictionary with the tracks assignment upon
  exiting.

  See the unit tests for a quick demo.
  """

  def __init__(self) :
    
    # Initialise attributes
    self.midiFile = ""
    self.nTracks = 0
    self.tracks = []
    
    # Initialise display
    self.root = None
    self.displayTrackList = []



  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI.load()
  # ---------------------------------------------------------------------------
  def load(self, midiFile: str) :
    """
    Reads the MIDI file and initialises the GUI.
    """

    self.midiFile = midiFile

    # Read content of the MIDI file
    midiObj = mido.MidiFile(midiFile)
    self.nTracks = len(midiObj.tracks)
    self.tracks = [Track() for _ in range(self.nTracks)]

    # Loop on the tracks
    for (i, track) in enumerate(midiObj.tracks) :
      
      # Read and limit the name of the track
      trackName = track.name.split("\x00")[0]
      if (len(trackName) == 0) :
        trackName = "*NO NAME*"
      elif (len(trackName) > MAX_TRACK_NAME_LENGTH) :
        trackName = "'" + trackName[0:(MAX_TRACK_NAME_LENGTH-3)] + "...'"
      else :
        trackName = "'" + trackName + "'"

      # Count the notes in the track
      noteCount = 0
      for msg in track :
        if ((msg.type == 'note_on') and (msg.velocity > 0)) :
          noteCount += 1

      # Assign to the Track
      self.tracks[i].name = trackName
      self.tracks[i].noteCount = noteCount
      self.tracks[i].panning = ""

      if ASSIGN_DEFAULT :
        if (i == 0) :
          self.tracks[i].panning = "R"
        elif (i == 1) :
          self.tracks[i].panning = "L"

      # Add the track to the 'trackList' widget
      self.displayTrackList.append(self._generateListboxString(i))



  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI.show()
  # ---------------------------------------------------------------------------
  def show(self) :
    """
    Shows the track selection GUI.
    Returns the index of the selected MIDI tracks upon exiting.
    """
    
    self.root = tk.Tk()
    self.root.title("Select tracks")
    self.root.resizable(0, 0)

    # GUI content
    content = ttk.Frame(self.root, padding = 20)
    
    lblAvailable = ttk.Label(content, text = "Available tracks:")
    tmp = tk.StringVar(value = self.displayTrackList)
    self.lstboxTracks = tk.Listbox(content, listvariable = tmp, width = 50, font = ("Consolas", 10))

    btnSetLeft = ttk.Button(content, text = "Assign track to Left hand", command = self.CLBK_onLeftKey)
    btnSetRight = ttk.Button(content, text = "Assign track to Right hand", command = self.CLBK_onRightKey)

    btnGenerate = ttk.Button(content, text = "Generate", command = self.CLBK_onGenerate, default = "active")
    btnQuit = ttk.Button(content, text = "Quit", command = self.CLBK_onQuit)

    content.grid(column = 0, row = 0)

    lblAvailable.grid(column = 0, row = 0, columnspan = 3, rowspan = 1, sticky = (tk.W))
    self.lstboxTracks.grid(column = 0, row = 1, columnspan = 3, rowspan = 1)
    btnSetLeft.grid(column = 0, row = 3, sticky = (tk.W, tk.N), pady = (10, 30))
    btnSetRight.grid(column = 2, row = 3, sticky = (tk.E, tk.N), pady = (10, 30))
    btnGenerate.grid(column = 2, row = 4, sticky = (tk.E, tk.S))
    btnQuit.grid(column = 0, row = 4, sticky = (tk.W, tk.S))

    # Bindings
    self.root.bind('<Escape>',  self.CLBK_onQuit)
    self.root.bind("<Return>",  self.CLBK_onGenerate)
    self.root.bind('<Left>',    self.CLBK_onLeftKey)
    self.root.bind('<Right>',   self.CLBK_onRightKey)
    self.root.bind('<Down>',    self.CLBK_onDownKey)
    self.root.bind('<q>',       self.CLBK_onQuit)

    self.root.protocol("WM_DELETE_WINDOW", self.CLBK_onQuit)

    self._centerWindow()
    self.root.mainloop()

    return self.getTrackLinks()



  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI._centerWindow()
  # ---------------------------------------------------------------------------
  def _centerWindow(self) :
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
  # METHOD TrackSelectionGUI.CLBK_onQuit()
  # ---------------------------------------------------------------------------
  def CLBK_onQuit(self, event = None) :
    print("[INFO] User exit...")
    exit()

  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI.CLBK_onLeftKey()
  # ---------------------------------------------------------------------------
  def CLBK_onLeftKey(self, event = None) : 
    self._assignActiveTrack(hand = "L")

  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI.CLBK_onRightKey()
  # ---------------------------------------------------------------------------
  def CLBK_onRightKey(self, event = None) :
    self._assignActiveTrack(hand = "R")

  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI.CLBK_onDownKey()
  # ---------------------------------------------------------------------------
  def CLBK_onDownKey(self, event = None) :
    if not(self.lstboxTracks.curselection()) :
      self.lstboxTracks.selection_set(0)
      self.lstboxTracks.activate(0)
      self.lstboxTracks.focus_set()

  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI.CLBK_onGenerate()
  # ---------------------------------------------------------------------------
  def CLBK_onGenerate(self, event = None) :
    self.root.destroy()



  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI._assignActiveTrack()
  # ---------------------------------------------------------------------------
  def _assignActiveTrack(self, hand = "L") -> None :
    """
    Assigns a hand to the higlighted track in the listbox.
    """

    lstboxSel = self.lstboxTracks.curselection()
    
    # If at least one item is highlighted
    if (len(lstboxSel) > 0) :
      sel = lstboxSel[0]

      self.tracks[sel].panning = hand

      # Update the listbox
      self.lstboxTracks.delete(sel)
      self.lstboxTracks.insert(sel, self._generateListboxString(sel))
      self.lstboxTracks.selection_set(sel)
      self.lstboxTracks.activate(sel)

      # Clear info of any track with the same panning
      for i in range(self.nTracks) :
        if (i != sel) :
          if (self.tracks[i].panning == hand) :
            self.tracks[i].panning = ""
            self.lstboxTracks.delete(i)
            self.lstboxTracks.insert(i, self._generateListboxString(i))

    else : 
      print(f"[INFO] Please select a track before assigning.")



  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI._generateListboxString()
  # ---------------------------------------------------------------------------
  def _generateListboxString(self, index: int) -> str :
    """
    Generates the content of the string that goes at the given index in the 
    track selection listbox.
    """
    
    s = f"Track {index} - {self.tracks[index].name} ({self.tracks[index].noteCount} notes)"
    
    if (self.tracks[index].panning == "L") :
      s = f"{s : <35}{'[LEFT]' : >7}"
    elif (self.tracks[index].panning == "R") : 
      s = f"{s : <35}{'[RIGHT]' : >7}"
    else :
      s = f"{s : <35}{'' : >7}"
    
    return s



  # ---------------------------------------------------------------------------
  # METHOD TrackSelectionGUI.getTrackLinks()
  # ---------------------------------------------------------------------------
  def getTrackLinks(self) :
    """
    Generates a list corresponding to the track selection.

    The output consists in a list that has as many elements as there are 
    channels.
    The list is such that 
    - out[leftChannelIndex]     = 'L'
    - out[rightChannelIndex]    = 'R'
    - out[...anything else...]  = ''
    """
    
    out = [T.panning for T in self.tracks]
    return out




# =============================================================================
# UTILITIES
# =============================================================================
class Track :

  """
  Description is TODO
  """

  def __init__(self):
    self.name = ""
    self.noteCount = 0
    self.panning = ""



# Factory function
def new() :
  return TrackSelectionGUI()



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  print("[INFO] Library 'TrackSelectionGUI' called as main: running unit tests...")
  
  gui = new()
  gui.load("./songs/Rachmaninoff_Piano_Concerto_No_3_Op_30_1st_Movement.mid")
  midiTracks = gui.show()
  print(f"MIDI tracks selection: {midiTracks}")
