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
# EXTERNALS
# =============================================================================
# Project libraries
from src.commons import *

# Standard libraries
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
      ctrlKey   = pygameEvent.mod & pygame.KMOD_CTRL
      altKey    = pygameEvent.mod & pygame.KMOD_ALT
      shiftKey  = pygameEvent.mod & pygame.KMOD_SHIFT
      altGrKey  = pygameEvent.mod & pygame.KMOD_META
      key       = pygameEvent.key
      
      # Simple keypresses (no modifiers)
      if not(ctrlKey | shiftKey | altKey | altGrKey) :
        self._onKeyEvent(key, pygameEvent.type)

      # Ctrl-modified keypress
      elif (ctrlKey and not(shiftKey | altKey | altGrKey)) :
        self._onKeyEvent(key, pygameEvent.type, modifier = "ctrl")

      # Shift-modified keypress
      elif (shiftKey and not(ctrlKey | altKey | altGrKey)) :
        self._onKeyEvent(key, pygameEvent.type, modifier = "shift")

      # Alt-modified keypress
      elif (altKey and not(ctrlKey | shiftKey | altGrKey)) :
        self._onKeyEvent(key, pygameEvent.type, modifier = "alt")

      # AltGr-modified keypress
      elif (altGrKey and not(ctrlKey | shiftKey | altKey)) :
        self._onKeyEvent(key, pygameEvent.type, modifier = "altgr")



    # MOUSE EVENTS
    elif (pygameEvent.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP]) :
      self._onMouseEvent(pygameEvent.button, pygameEvent.type)
      


  # ---------------------------------------------------------------------------
  # METHOD: Widget.render()                                          [ABSTRACT]
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Renders the widget on screen.
    This function is called at every frame of the top level application.

    This function must be overriden with the specific code of the widget.
    """
    
    pass
    


  # ---------------------------------------------------------------------------
  # METHOD: Widget._onKeyEvent()                                      [PRIVATE]
  # ---------------------------------------------------------------------------
  def _onKeyEvent(self, key, type, modifier = "") :
    """
    Function is triggered by a keypress.
    
    This function must be overriden with the specific code of the widget.
    """

    # SAMPLE CODE
    # if (type == pygame.KEYDOWN) :
    #   if (key == pygame.K_q) :
    #     print("[DEBUG] Widget._onKeyEvent(): 'Q' was pressed!")

    pass



  # ---------------------------------------------------------------------------
  # METHOD: Widget._onMouseEvent()                                    [PRIVATE]
  # ---------------------------------------------------------------------------
  def _onMouseEvent(self, button, type) :
    """
    Function is triggered by a keypress.
    
    This function must be overriden with the specific code of the widget.
    """
    
    # SAMPLE CODE
    # if (type == pygame.MOUSEBUTTONDOWN) :
    #   if (button == MOUSE_SCROLL_UP) :    
    #     print("[DEBUG] Widget._onMouseEvent(): scroll up!")

    pass

  