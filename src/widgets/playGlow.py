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
# None.



# =============================================================================
# Constants pool
# =============================================================================
# None.



# =============================================================================
# Main code
# =============================================================================
class PlayGlow :
  
  """
  Class definition for the PlayGlow object used in gangQin and scoreShot_fusion.
  """  
  def __init__(self) :
    
    self.hand = None

    self.active = True

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

    self.dragCoord_x = -1
    self.dragCoord_y = -1

    self.shift_x = 0
    self.shift_y = 0



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
    Returns True if a click occurs at the bottom right of the playglow object.
    Used to detect a resize.
    """
    
    x = coord[0]; y = coord[1]

    test_x = ((x >= (self.hitBox_xMax-5)) and (x <= (self.hitBox_xMax+5)))
    test_y = ((y >= (self.hitBox_yMax-5)) and (y <= (self.hitBox_yMax+5)))
    
    return (test_x and test_y)
  


  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.toTuple()
  # ---------------------------------------------------------------------------
  def toTuple(self) :
    """
    Returns a tuple with the playglow coordinates, ready to be used in the 
    "pygame.draw.rect" function.
    """
    
    return (
      self.coord_xMin + self.shift_x, 
      self.coord_yMin + self.shift_y, 
      self.width,
      self.height
    )
  


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



  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.shift(dx,dy)
  # ---------------------------------------------------------------------------
  def shift(self, dx, dy) :
    """
    TODO
    """
    
    self.shift_x = dx
    self.shift_y = dy



  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.shiftApply(None)
  # ---------------------------------------------------------------------------
  def shiftApply(self) :
    """
    TODO
    """
    
    self.coord_xMin += self.shift_x
    self.coord_xMax += self.shift_x
    self.coord_yMin += self.shift_y
    self.coord_yMax += self.shift_y

    self.hitBox_xMin += self.shift_x
    self.hitBox_xMax += self.shift_x
    self.hitBox_yMin += self.shift_y
    self.hitBox_yMax += self.shift_y



  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.dragFrom(x,y)
  # ---------------------------------------------------------------------------
  def dragFrom(self, x, y) :
    """
    TODO
    """
    
    self.dragCoord_x = x
    self.dragCoord_y = y


  # ---------------------------------------------------------------------------
  # METHOD PlayGlow.resizeFrom(x,y)
  # ---------------------------------------------------------------------------
  def resizeFrom(self, x, y) :
    """
    TODO
    """
    
    self.dragCoord_x = x
    self.dragCoord_y = y




# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'playGlow.py'")



