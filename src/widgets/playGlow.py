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

    self.coord_xMin = -1
    self.coord_xMax = -1
    self.coord_yMin = -1
    self.coord_yMax = -1

    self.hitBox_xMin = -1
    self.hitBox_xMax = -1
    self.hitBox_yMin = -1
    self.hitBox_yMax = -1



  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.isClickInBox(click coordinates)
  # ---------------------------------------------------------------------------
  def isClickInBox(self) :
    """
    Returns True if a click occurs within the playGlow.
    Used to detect a drag&drop.
    """
    
    print("[DEBUG] PlayGlow.isClickInBox() is TODO")



  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.isClickOnBorder(click coordinates)
  # ---------------------------------------------------------------------------
  def isClickOnBorder(self) :
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
    
    return (self.coord_xMin, self.coord_yMin, self.coord_xMax, self.coord_yMax)
  


  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.loadFromTuple(coordinates tuple)
  # ---------------------------------------------------------------------------
  def loadFromTuple(self, coord) :
    """
    TODO
    """
    
    (coord_xMin, coord_yMin, coord_xMax, coord_yMax) = coord

    self.coord_xMin = coord_xMin
    self.coord_xMax = coord_xMax
    self.coord_yMin = coord_yMin
    self.coord_yMax = coord_yMax



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'playGlow.py'")



