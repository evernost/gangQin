# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : ProgressBar
# File name     : ProgressBar.py
# Purpose       : provides a progress bar widget
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

import pygame
import fontUtils as fu



# =============================================================================
# Constants pool
# =============================================================================
PROGRESSBAR_MODE_BAR = 0
PROGRESSBAR_MODE_DOT = 1



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")



# =============================================================================
# Main code
# =============================================================================

class ProgressBar :

  def __init__(self, loc, size, thickness = 2) :
    (self.locX, self.locY) = loc
    (self.sizeX, self.sizeY) = size
    self.visible = False
    
    self.mode = PROGRESSBAR_MODE_BAR
    
    self.thickness = thickness




class CursorProgressBar(ProgressBar) :

  def __init__(self, loc, size, thickness = 2) :
    super().__init__(loc, size, thickness)
    

    self.showMarker = True
    self.showBookmarks = True
    self.showLoop = False
    
    self.bookmarks = []



class LoopProgressBar(ProgressBar) :

  def __init__(self, loc, size, thickness = 2) :
    super().__init__(loc, size, thickness)
    

    self.loopStartCursor = -1
    self.loopEndCursor = -1


