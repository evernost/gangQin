# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : handSelector
# File name     : handSelector.py
# File type     : Python script (Python 3)
# Purpose       : shows the hand selector for the StaffScope editor
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Saturday, 09 November 2024
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
class Msg(Enum) :
  SET_TO_LEFT_HAND  = 1
  SET_TO_RIGHT_HAND = 2



# =============================================================================
# CLASS DEFINITION
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

    #self.loc = (1312, 470)  # Coordinates of the up right corner 
    self.xMin = self.loc[0] - (5*5*2) - (5*2)   # 5 chars, 5 horiz pixel per char, 1 pixel has size 2
    self.xMax = self.loc[0]
    self.yMin = self.loc[1]
    self.yMax = self.loc[1] + (7*2) + 2 + 2

    self.sel = "L"
    self.visible = True

    self.msgQueueIn = []
    self.msgQueueOut = []



  # ---------------------------------------------------------------------------
  # METHOD: HandSelector.render()
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
        self.top.screen, 
        "L - R", 
        colorSpec, {"r": R, "g": G, "n": GUI_TEXT_COLOR}, 
        formatSpec,
        self.loc,
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
    





  # ---------------------------------------------------------------------------
  # METHOD: HandSelector._onMouseEvent()                            [INHERITED]
  # ---------------------------------------------------------------------------
  def _onMouseEvent(self, event) :
    """
    Mouse event callback.
    
    This function is inherited from the Widget class.
    """
    
    if (event.type == pygame.MOUSEBUTTONDOWN) :
      if (event.button == MOUSE_LEFT_CLICK) :

        (x,y) = pygame.mouse.get_pos()

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

        elif ((x >= xMin_R) and (x <= xMax_R) and (y >= yMin_R) and (y <= yMax_R)) :
          self.sel = "R"



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
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'handSelector.py'")




