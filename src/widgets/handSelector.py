# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : handSelector
# File name     : handSelector.py
# File type     : Python script (Python 3)
# Purpose       : 
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Saturday, 09 November 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from src.commons import *

import src.text as text
import src.widgets.widget as widget

from enum import Enum
import pygame



# =============================================================================
# Constants pool
# =============================================================================
class Msg(Enum) :
  SET_TO_LEFT_HAND  = 1
  SET_TO_RIGHT_HAND = 2



# =============================================================================
# Main code
# =============================================================================
class HandSelector(widget.Widget) :

  """
  HANDSELECTOR object
  
  The HandSelector object shows the widget that selects the active hand.
  By default, right and left hand are active.

  Using the widget, you can indicate to practice with single hand.

  The HandSelector class derives from the Widget class.
  """

  def __init__(self, top, loc) :
    
    # Call the Widget init method
    super().__init__(top, loc)
    
    # Name of the widget
    self.name = "hand selector"

    self.loc = (1312, 470)  # Coordinates of the up right corner 
    self.xMin = self.loc[0] - (5*5*2) - (5*2)   # 5 chars, 5 horiz pixel per char, 1 pixel has size 2
    self.xMax = self.loc[0]
    self.yMin = self.loc[1]
    self.yMax = self.loc[1] + (7*2) + 2 + 2

    self.sel = "L"
    self.visible = True

    self.msgQueueIn = []
    self.msgQueueOut = []



  # ---------------------------------------------------------------------------
  # METHOD: HandSelector.uiEvent()
  # ---------------------------------------------------------------------------
  def uiEvent(self, pygameEvent) -> None :
    """
    This function is called by the top level and passes all the keyboard/mouse
    interactions to the widget.
    """
    
    # Keyboard events
    if (pygameEvent.type in (pygame.KEYUP, pygame.KEYDOWN)) :
      keys      = pygame.key.get_pressed()
      ctrlKey   = pygameEvent.mod & pygame.KMOD_CTRL
      altKey    = pygameEvent.mod & pygame.KMOD_ALT
      shiftKey  = pygameEvent.mod & pygame.KMOD_SHIFT
      altGrKey  = pygameEvent.mod & pygame.KMOD_META
      
      # Simple keypresses (no modifiers)
      if not(ctrlKey | shiftKey | altKey | altGrKey) :
        
        # TAB: highlight the next note above for fingersatz edition
        if keys[pygame.K_TAB] :
          print(f"[DEBUG] Fast fingersatz editing with 'tab' will be available soon!")



      # Ctrl-modified keypress
      elif (ctrlKey and not(shiftKey | altKey | altGrKey)) :
        pass


      # Shift-modified keypress
      elif (shiftKey and not(ctrlKey | altKey | altGrKey)) :
        
        # TAB: highlight the next note above for fingersatz edition
        if keys[pygame.K_TAB] :
          print(f"[DEBUG] Fast fingersatz editing with 'tab' will be available soon!")


      # -----------------------------------------------
        # Maj + tab: highlight the note before for editing
        # -----------------------------------------------
        if (keys[pygame.K_TAB] and shiftKey) :
          print(f"[DEBUG] Fast fingersatz editing with 'tab' will be available soon!")
          # fingerSelWidget.keyPress(keys)




  # ---------------------------------------------------------------------------
  # METHOD Database.setScreen()
  # ---------------------------------------------------------------------------
  def setScreen(self, screenObj) :
    """
    Creates an internal copy of the Pygame screen parameters.
    Required to draw and interact with the widget.
    """

    self.screen = screenObj
    


  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.render()
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Renders the widget.
    Must be called at every frame.
    """

    if (self.visible) :

      R = (226, 129, 131)
      G = (129, 226, 129)
      
      if (self.sel == "L") :
        colorSpec  = "rnnnn"
        formatSpec = "_    "
      else :
        colorSpec  = "nnnng"
        formatSpec = "    _"

      text.renderPlus(
        self.screen, 
        "L - R", 
        colorSpec, {"r": R, "g": G, "n": GUI_TEXT_COLOR}, 
        formatSpec,
        (1312, 470),
        2,
        justify = text.RIGHT_JUSTIFY
      )



  # ---------------------------------------------------------------------------
  # METHOD HandSelector.clickDown(mouse coordinates)
  # ---------------------------------------------------------------------------
  def clickDown(self, coord) :
    """
    Handles a click on the widget.
    """
    
    x = coord[0]; y = coord[1]
    
    xMin_L = self.xMin - 2
    xMax_L = self.xMin + (5*2) + 2
    yMin_L = self.yMin - 2
    yMax_L = self.yMax + 2

    xMin_R = self.xMax - 2 - (5*2) - 2
    xMax_R = self.xMax
    yMin_R = self.yMin - 2
    yMax_R = self.yMax + 2

    if ((x >= xMin_L) and (x <= xMax_L) and (y >= yMin_L) and (y <= yMax_L)) :
      self.sel = "L"
      self.msgQueueOut.append(Msg.SET_TO_LEFT_HAND)

    elif ((x >= xMin_R) and (x <= xMax_R) and (y >= yMin_R) and (y <= yMax_R)) :
      self.sel = "R"
      self.msgQueueOut.append(Msg.SET_TO_RIGHT_HAND)



  # ---------------------------------------------------------------------------
  # METHOD HandSelector.rightClickDown(mouse coordinates)
  # ---------------------------------------------------------------------------
  def rightClickDown(self, coord) :
    """
    Handles a right click on the widget.
    """
    
    x = coord[0]; y = coord[1]
    
    if (self.sel == "L") :
      self.sel = "R"
      self.msgQueueOut.append(Msg.SET_TO_RIGHT_HAND)

    elif (self.sel == "R") :
      self.sel = "L"
      self.msgQueueOut.append(Msg.SET_TO_LEFT_HAND)


    
# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'handSelector.py'")




