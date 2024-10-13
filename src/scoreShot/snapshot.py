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
# None.



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
    
    self.cursorRange = []           # Range of cursors (in the score) that is covered by this snapshot
    
    self.leftHandRectCoords = []    # Coordinates of the rectangles highlighting the left hand notes
    self.rightHandRectCoords = []   # Coordinates of the rectangles highlighting the right hand notes
    
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
      "dir"                   : self.dir,
      "file"                  : self.file,
      "index"                 : self.index,
      "displayName"           : self.displayName,
      "description"           : self.description,
      "cursorRange"           : self.cursorRange,
      "leftHandRectCoords"    : self.leftHandRectCoords,
      "rightHandRectCoords"   : self.rightHandRectCoords,
      "needsRework"           : self.needsRework,
      "fileMissing"           : self.fileMissing,
    } 
  


  # ---------------------------------------------------------------------------
  # METHOD Snapshot.fromDict()
  # ---------------------------------------------------------------------------
  def fromDict(self, data) :
    """
    Loads the content of the Snapshot class from a dictionary for easier 
    serialisation.
    """

    self.dir                  = data["dir"]
    self.file                 = data["file"]
    self.index                = data["index"]
    self.displayName          = data["displayName"]
    self.description          = data["description"]
    self.cursorRange          = data["cursorRange"]
    self.leftHandRectCoords   = data["leftHandRectCoords"]
    self.rightHandRectCoords  = data["rightHandRectCoords"]
    self.needsRework          = data["needsRework"]
    self.fileMissing          = data["fileMissing"]


  
# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'snapshot.py'")
