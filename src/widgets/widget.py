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
from src.commons import *


import pygame






# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Widget :

  """
  Widget class definition.
  The widget class contains pure functions that need to be overriden:
  - 'render': draws the widget's content on the screen
  - 'uiEvent': defines how the widget reacts to user inputs (click, keypress)

  This widget class itself does not do anything.

  Widgets implemented in the gangQin app suite (gangQin player, gangQin capture
  gangQin fusion) must inherit from this class.
  """
  
  def __init__(self, top, loc = WIDGET_LOC_UNDEFINED) :
    
    # Reference to the top level app
    self.top = top
    
    # Position in the top level app
    self.loc = loc

    # GUI interactions
    self.keyboardCtrlKey = False



  # ---------------------------------------------------------------------------
  # METHOD: Widget.uiEvent()
  # ---------------------------------------------------------------------------
  def uiEvent(self, pygameEvent) -> None :
    """
    This function is called every time a pygame UI event occurs (keyboard or mouse)
    """
    
    # KEYBOARD EVENTS
    if (pygameEvent.type in (pygame.KEYUP, pygame.KEYDOWN)) :
      keys      = pygame.key.get_pressed()
      ctrlKey   = pygameEvent.mod & pygame.KMOD_CTRL
      altKey    = pygameEvent.mod & pygame.KMOD_ALT
      shiftKey  = pygameEvent.mod & pygame.KMOD_SHIFT
      altGrKey  = pygameEvent.mod & pygame.KMOD_META
      
      # Simple keypresses (no modifiers)
      if not(ctrlKey | shiftKey | altKey | altGrKey) :
        pass

      # Ctrl-modified keypress
      elif (ctrlKey and not(shiftKey | altKey | altGrKey)) :
        pass

      # Shift-modified keypress
      elif (shiftKey and not(ctrlKey | altKey | altGrKey)) :
        pass

      # Alt-modified keypress
      elif (altKey and not(ctrlKey | shiftKey | altGrKey)) :
        pass

      # AltGr-modified keypress
      elif (altGrKey and not(ctrlKey | shiftKey | altKey)) :
        pass



    # MOUSE EVENTS
    elif (pygameEvent.type == pygame.MOUSEBUTTONDOWN) :
        
      # Left click
      if (pygameEvent.button == MOUSE_LEFT_CLICK) :
        pass
      
      # Scroll up
      elif (pygameEvent.button == MOUSE_SCROLL_UP) :
        pass

      # Scroll down
      elif (pygameEvent.button == MOUSE_SCROLL_DOWN) :
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
    



