# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : scoreStatus
# File name     : scoreStatus.py
# Purpose       : widget showing the status of a score in the staffScope
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Thursday, 28 November 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from src.commons import *

import src.text as text

from enum import Enum



# =============================================================================
# Constants pool
# =============================================================================
class Msg(Enum) :
  SET_TO_LEFT_HAND  = 1
  SET_TO_RIGHT_HAND = 2



# =============================================================================
# Main code
# =============================================================================
class scoreStatus :

  def __init__(self) :
    
    self.screen = None

    self.loc = (1312, 470)  # Coordinates of the up right corner 
    self.xMin = self.loc[0] - (5*5*2) - (5*2)   # 5 chars, 5 horiz pixel per char, 1 pixel has size 2
    self.xMax = self.loc[0]
    self.yMin = self.loc[1]
    self.yMax = self.loc[1] + (7*2) + 2 + 2

    self.sel = "OK"
    self.visible = True

    self.msgQueueIn = []
    self.msgQueueOut = []



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
        colorSpec, {"r": R, "g": G, "n": UI_TEXT_COLOR}, 
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




