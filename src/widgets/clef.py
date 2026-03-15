# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : clef
# File name     : clef.py
# File type     : Python script (Python 3)
# Purpose       : provides a mini clef to display the key and a few notes
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project specific constants
from src.commons import *
import src.widgets.widget as widget



# Standard libraries
import pygame



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# Main code
# =============================================================================
class Clef(widget.Widget) :

  def __init__(self, loc) :
    (self.locX, self.locY) = loc
    self.visible = False
    

# --------------------------
# /!\ UNDER CONSTRUCTION /!\
# --------------------------




# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")