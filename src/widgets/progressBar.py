# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : ProgressBar
# File name     : ProgressBar.py
# File type     : Python script (Python 3)
# Purpose       : represents the current location in the score visually
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project specific constants
from src.commons import *
import src.text as text
import src.widgets.widget as widget

# Standard libraries
from enum import Enum
import pygame



# =============================================================================
# CONSTANTS
# =============================================================================
class Mode(Enum) :
  BAR = 0
  DOT = 1



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class ProgressBar(widget.Widget) :

  """
  PROGRESS_BAR object
  
  Description is TODO.

  The ProgressBar class derives from the Widget class.
  """

  def __init__(self, top) :
    
    # Call the Widget init method
    super().__init__(top, loc = WIDGET_LOC_UNDEFINED)
    
    # Name of the widget
    self.name = "progress bar"
    
    self.enabled = False

  
  
  # ---------------------------------------------------------------------------
  # METHOD: Keyboard.render()
  # ---------------------------------------------------------------------------
  def render(self) -> None :
    """
    Renders the widget on screen.
    """

    if self.enabled :
      text.render(self.top.screen, f"BPM:{self.bpm} - {self.num}/{self.denom} - {self.counter}", (950, 470), 2, GUI_TEXT_COLOR)
  
    





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



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'handSelector.py'")