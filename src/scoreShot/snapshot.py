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




# =============================================================================
# Constants pool
# =============================================================================




# =============================================================================
# Main code
# =============================================================================
class Snapshot :
  def __init__(self, name, index) :
    
    self.file = ""                  # Name of the underlying snapshot image file
    self.index = 0
    
    self.description = ""           # Description string of the snapshot (page number in the original score, etc.)
    
    self.cursorRange = []           # Range of cursors (in the score) that is covered by this snapshot
    
    self.displayRectLeftHand = []   # Display rectangles' coordinates for the left hand
    self.displayRectRightHand = []  # Display rectangles' coordinates for the right hand
    
    self.hasIssue = False           # Set to True if any issue has been reported in the player or in gangQin
  
  
  
  