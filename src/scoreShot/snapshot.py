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
    
    self.displayRectLeftHand = []   # Display rectangles' coordinates for the left hand
    self.displayRectRightHand = []  # Display rectangles' coordinates for the right hand
    
    self.needsRework = False        # Set to True if any issue has been reported in the player or in gangQin
    self.fileMissing = False        # Set to True if the image file could not be found


  
# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'snapshot.py'")
