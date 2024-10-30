# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : playGlow
# File name     : playGlow.py
# Purpose       : playGlow object for the staffScope
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Saturday, 26 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================



# =============================================================================
# External libs 
# =============================================================================
# None



# =============================================================================
# Constants pool
# =============================================================================
# None



# =============================================================================
# Main code
# =============================================================================
class PlayGlow :
  
  """
  Defines the class for the PlayGlow widgets in scoreShot_fusion and gangQin.
  """  
  def __init__(self) :
    
    self.hand = None

    self.type = "active"   # Can be "active" or "passive"

    self.coord_xMin = -1
    self.coord_xMax = -1
    self.coord_yMin = -1
    self.coord_yMax = -1

    self.width = -1
    self.height = -1

    self.hitBox_xMin = -1
    self.hitBox_xMax = -1
    self.hitBox_yMin = -1
    self.hitBox_yMax = -1



  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.isClickInBox(click coordinates)
  # ---------------------------------------------------------------------------
  def isClickInBox(self, coord) :
    """
    Returns True if a click occurs within the playGlow.
    Used to detect a drag&drop.
    """
    
    x = coord[0]; y = coord[1]

    test_x = ((x >= self.hitBox_xMin) and (x <= self.hitBox_xMax))
    test_y = ((y >= self.hitBox_yMin) and (y <= self.hitBox_yMax))
    return (test_x and test_y)



  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.isClickOnBorder(click coordinates)
  # ---------------------------------------------------------------------------
  def isClickOnBorder(self, coord) :
    """
    Returns True if a click occurs within the playGlow.
    Used to detect a resize.
    """
    
    print("[DEBUG] PlayGlow.isClickOnBorder() is TODO")
  


  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.toTuple()
  # ---------------------------------------------------------------------------
  def toTuple(self) :
    """
    TODO
    """
    
    return (self.coord_xMin, self.coord_yMin, self.width, self.height)
  


  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.load(coordinates tuple)
  # ---------------------------------------------------------------------------
  def load(self, coords) :
    """
    Initialises the fields based on the coordinates of the rectangle using a
    start point (x0,y0) and a shape (width, height)
    """
    
    (x0, y0, width, height) = coords

    self.coord_xMin = x0
    self.coord_xMax = x0 + width
    self.coord_yMin = y0
    self.coord_yMax = y0 + height

    self.width  = width
    self.height = height

    self.hitBox_xMin = x0
    self.hitBox_xMax = x0 + width
    self.hitBox_yMin = y0
    self.hitBox_yMax = y0 + height



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'playGlow.py'")



