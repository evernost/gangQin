# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : widget
# File name     : widget.py
# File type     : Python script (Python 3)
# Purpose       : widget parent class
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Saturday, 5 April 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs 
# =============================================================================
# Project specific constants
from commons import *









# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Widget :

  """
  Widget class definition.
  The widget class contains pure functions that need to be overriden:
  - TODO
  - TODO
  """
  
  
  
  # ---------------------------------------------------------------------------
  # METHOD: Widget.__init__
  # ---------------------------------------------------------------------------
  def __init__(self, top, loc = (0, 0)) :
    """
    Initialisation method definition.
    """
    
    # Reference to the top level app
    self.top = top
    
    # Position in the top level app
    self.loc = loc

    # List of pygame keyboard/mouse event the widget must react to
    self.uiSensivityList = []



  # ---------------------------------------------------------------------------
  # METHOD: Widget.uiEvent()
  # ---------------------------------------------------------------------------
  def uiEvent(self, pygameEvent) :
    """
    This function is called every time a pygame event listed in 'uiSensitivityList'
    happens.
    """
    
    if pygameEvent in self.uiSensivityList :
      pass
    


  # ---------------------------------------------------------------------------
  # METHOD: Widget.render()
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Renders the widget on screen.
    This function is called at every frame of the top level application.
    """
    
    pass
    



