# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : reportIssueGUI
# File name     : reportIssueGUI.py
# File type     : Python script (Python 3)
# Purpose       : provides GUI to report an issue in the score.
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Saturday, 24 May 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
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
class ReportIssueGUI :

  """
  REPORT_ISSUE_GUI object

  This object shows a GUI inviting the user to report something wrong in the 
  score.
  The issue is reported in the own database of the song, making the information
  available across the different tools (player, capture, fusion)

  List of possible reports:
  1 - Score: note with incorrect pitch
  2 - Score: missing note
  3 - Score: note in excess (exists in the database, but does not exist in the score)
  4 - Score: note misplaced in time
  5 - PlayGlow: not placed accurately
  6 - PlayGlow: missing
  7 - Fingersatz: value is dubious
  8 - Other 

  See the unit tests for a quick demo.
  """

  def __init__(self) :
    
    # Initialise attributes
    # None.
    
    # Initialise display
    self.root = None



  # # ---------------------------------------------------------------------------
  # # METHOD TrackSelectionGUI.load()
  # # ---------------------------------------------------------------------------
  # def load(self, midiFile: str) :
  #   """
  #   Reads the MIDI file and initialises the GUI.
  #   """

  #   self.midiFile = midiFile

  #   # Read content of the MIDI file
  #   midiObj = mido.MidiFile(midiFile)
  #   self.nTracks = len(midiObj.tracks)
  #   self.tracks = [Track() for _ in range(self.nTracks)]

  #   # Loop on the tracks
  #   for (i, track) in enumerate(midiObj.tracks) :
      
  #     # Read and limit the name of the track
  #     trackName = track.name.split("\x00")[0]
  #     if (len(trackName) == 0) :
  #       trackName = "*NO NAME*"
  #     elif (len(trackName) > MAX_TRACK_NAME_LENGTH) :
  #       trackName = "'" + trackName[0:(MAX_TRACK_NAME_LENGTH-3)] + "...'"
  #     else :
  #       trackName = "'" + trackName + "'"

  #     # Count the notes in the track
  #     noteCount = 0
  #     for msg in track :
  #       if ((msg.type == 'note_on') and (msg.velocity > 0)) :
  #         noteCount += 1

  #     # Assign to the Track
  #     self.tracks[i].name = trackName
  #     self.tracks[i].noteCount = noteCount
  #     self.tracks[i].panning = ""

  #     if ASSIGN_DEFAULT :
  #       if (i == 0) :
  #         self.tracks[i].panning = "R"
  #       elif (i == 1) :
  #         self.tracks[i].panning = "L"

  #     # Add the track to the 'trackList' widget
  #     self.displayTrackList.append(self._generateListboxString(i))



  # ---------------------------------------------------------------------------
  # METHOD reportIssueGUI.show()
  # ---------------------------------------------------------------------------
  def show(self) :
    """
    Shows the issue report GUI.
    """
    
    self.root = tk.Tk()
    self.root.title("Report an issue")
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

    return None



  # ---------------------------------------------------------------------------
  # METHOD reportIssueGUI._centerWindow()
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
  # METHOD reportIssueGUI.CLBK_onQuit()
  # ---------------------------------------------------------------------------
  def CLBK_onQuit(self, event = None) :
    print("[INFO] reportIssueGUI: user cancelled")
    exit()




  # ---------------------------------------------------------------------------
  # METHOD reportIssueGUI.CLBK_onReport()
  # ---------------------------------------------------------------------------
  def CLBK_onReport(self, event = None) :
    self.root.destroy()



# =============================================================================
# UTILITIES
# =============================================================================

# Factory function
def new() :
  return ReportIssueGUI()



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  print("[INFO] Library 'ReportIssueGUI' called as main: running unit tests...")
  
  gui = new()
  
