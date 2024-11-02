# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : snapshot
# File name     : snapshot.py
# Purpose       : snapshot object definition
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Friday, 04 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================



# =============================================================================
# External libs 
# =============================================================================
import src.widgets.playGlow as playGlow



# =============================================================================
# Constants pool
# =============================================================================
# None.



# =============================================================================
# Main code
# =============================================================================
class Snapshot :
  def __init__(self) :
    
    self.dir = ""                   # Directory of the snapshot
    self.file = ""                  # Name of the actual snapshot image file
    self.index = 0                  # Index of the image in the database
    
    self.displayName = ""           # String to display in the GUI listbox

    self.description = ""           # Description string of the snapshot (page number in the original score, any comment, etc.)
    
    self.cursorMin  = -1            # Min. cursor value covered by this snapshot
    self.cursorMax  = -1            # Max. cursor value covered by this snapshot
    
    self.playGlowsLeft = {}         # List of tuples with the coordinates of the rectangles highlighting the left hand notes (one per cursor value)
    self.playGlowsRight = {}        # List of tuples with the coordinates of the rectangles highlighting the right hand notes (one per cursor value)
    
    self.rulerLeftHand = (-1, -1, -1, -1)
    self.rulerRightHand = (-1, -1, -1, -1)

    self.needsRework = False        # Set to True if any issue has been reported in the player or in gangQin
    self.fileMissing = False        # Set to True if the image file could not be found



  # ---------------------------------------------------------------------------
  # METHOD Snapshot.toDict()
  # ---------------------------------------------------------------------------
  def toDict(self) :
    """
    Converts the content of the Snapshot class to a dictionary for easier 
    serialisation.
    """

    return {
      "dir"             : self.dir,
      "file"            : self.file,
      "index"           : self.index,
      "displayName"     : self.displayName,
      "description"     : self.description,
      "cursorMin"       : self.cursorMin,
      "cursorMax"       : self.cursorMax,
      "playGlowsLeft"   : self.playGlowsLeft,
      "playGlowsRight"  : self.playGlowsRight,
      "needsRework"     : self.needsRework,
      "fileMissing"     : self.fileMissing,
    } 
  


  # ---------------------------------------------------------------------------
  # METHOD Snapshot.fromDict()
  # ---------------------------------------------------------------------------
  def fromDict(self, data) :
    """
    Loads the content of the Snapshot class from a dictionary for easier 
    serialisation.
    """

    self.dir            = data["dir"]
    self.file           = data["file"]
    self.index          = data["index"]
    self.displayName    = data["displayName"]
    self.description    = data["description"]
    self.cursorMin      = data["cursorMin"]
    self.cursorMax      = data["cursorMax"]
    self.playGlowsLeft  = data["playGlowsLeft"]
    self.playGlowsRight = data["playGlowsRight"]
    self.needsRework    = data["needsRework"]
    self.fileMissing    = data["fileMissing"]



  # ---------------------------------------------------------------------------
  # METHOD Snapshot.getPlayGlowAtCursor()
  # ---------------------------------------------------------------------------
  def getPlayGlowAtCursor(self, cursor) :
    """
    Returns the playGlow coordinates (left and right hand) at a given cursor.
    Returns None if no playGlow has been declared yet.
    """

    query = str(cursor)
    output = []

    if (query in self.playGlowsLeft) :
      p = playGlow.PlayGlow()
      p.hand = "L"
      p.load(self.playGlowsLeft[query])
      output.append(p)
    
    if (query in self.playGlowsRight) :
      p = playGlow.PlayGlow()
      p.hand = "R"
      p.load(self.playGlowsRight[query])
      output.append(p)
    
    return output



  # ---------------------------------------------------------------------------
  # METHOD Snapshot.setPlayGlowAtCursor()
  # ---------------------------------------------------------------------------
  def setPlayGlowAtCursor(self, cursor, playGlowObj) :
    """
    Sets the playglow attribute of the snapshot at a specific cursor.
    Automatically assigns it to the left or right hand.
    Note: the function overrides any playglow that has already been set.
    """

    # Snapshot with uninitialised cursors
    if ((self.cursorMin == -1) and (self.cursorMax == -1)) :
      self.cursorMin = cursor
      self.cursorMax = cursor

    if (cursor > self.cursorMax) :
      self.cursorMax = cursor

    if (cursor < self.cursorMin) :
      self.cursorMin = cursor

    print(f"[DEBUG] Assigning playglow to the db; new range: {self.cursorMin} -> {self.cursorMax}")

    insertLoc = str(cursor)
    if (playGlowObj.hand == "L") :
      self.playGlowsLeft[insertLoc] = playGlowObj.toTuple()

    elif (playGlowObj.hand == "R") :
      self.playGlowsRight[insertLoc] = playGlowObj.toTuple()

    else : 
      print("[DEBUG] Snapshot.setPlayGlowAtCursor(): invalid 'hand' attribute. Defaulting to left hand.")



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'snapshot.py'")
