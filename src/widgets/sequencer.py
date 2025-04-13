# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : sequencer
# File name     : sequencer.py
# File type     : Python script (Python 3)
# Purpose       : controls the current location displayed in the score
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 14 April 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from src.commons import *

import src.widgets.widget as widget



# =============================================================================
# Constants pool
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Sequencer(widget.Widget) :

  """
  TODO: description

  
  - manages the loops 
  - reads arbiter decision
  - automatic play 


  """

  def __init__(self, top) :
    
    # Call the Widget init method
    super().__init__(top, loc = WIDGET_LOC_UNDEFINED)

    # Define the events the widgets must react to
    self.uiSensivityList = []




# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'score.py'")

