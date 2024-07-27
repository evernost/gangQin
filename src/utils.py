# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : utils
# File name     : utils.py
# Purpose       : provides various utilities 
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

# For color manipulation
import colorsys


# =============================================================================
# Constants pool
# =============================================================================



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")



# =============================================================================
# CLASS Vector2D 
# 
# Consider a list of (x,y) tuples representing 2D coordinates of a bunch of points.
# Let's say we want to add a new point constructed from a vector translation 
# of the last point of the list
# Typical use case: the list is a list of points making a polygon. We want to 
# add a point whose 
# Vector2D is an object that can be added to a list containing a bunch of 
# (x,y) tuples (representing 2D coordinates) and it will add a new tuple
# Formally: 
# [(x1,y1), (x2,y2), ..., (xN,yN)] + Vector2D(u,v) = [(x1,y1), (x2,y2), ..., (xN,yN), (xN+u,yN+v)]
# =============================================================================
class Vector2D :

  # ---------------------------------------------------------------------------
  # Constructor
  # ---------------------------------------------------------------------------
  def __init__(self, x, y) :
    self.x = x
    self.y = y



  # ---------------------------------------------------------------------------
  # Right addition: vector + listOfPoints
  # ---------------------------------------------------------------------------
  def __add__(self, other):
    self._checkOperand(other)

    # Adding a vector to a list
    if isinstance(other, list) :
      tmp = other.copy()
      if ((other[-1][0] == 0) and (other[-1][0] == 0)) :
        pass
      else :
        tmp.append((self.x + other[-1][0], self.y + other[-1][1]))
      return tmp
    
    # Adding a vector to another vector
    elif isinstance(other, Vector2D) :
      self.x += other.x
      self.y += other.y



  # ---------------------------------------------------------------------------
  # Left addition: listOfPoints + vector
  # ---------------------------------------------------------------------------
  def __radd__(self, other):
    return self.__add__(other)



  # ---------------------------------------------------------------------------
  # Define print
  # ---------------------------------------------------------------------------
  def __str__(self):
    return f"({self.x},{self.y})"



  # ---------------------------------------------------------------------------
  # Check the validity of the other operand
  # ---------------------------------------------------------------------------
  def _checkOperand(self, other) :
    
    if isinstance(other, list) :
      for i in other :
        if isinstance(i, tuple) :
          if (len(i) == 2) : 
            if all(isinstance(j, int) for j in i) :
              pass
            else :
              raise TypeError("[ERROR] Adding a vector to a list: the tuple must contain integers only.")
          else :
            raise TypeError("[ERROR] Adding a vector to a list: tuples in the list must be of length 2.")
        else :
          raise TypeError("[ERROR] Adding a vector to a list: the list must contain tuples only.")
      
    elif isinstance(other, Vector2D) :
      pass

    else :
      raise TypeError("[ERROR] A vector can only be added to a list or to another vector.")




# =============================================================================
# SCALE object
# =============================================================================
# References: 
# > https://music.stackexchange.com/questions/73110/what-are-the-interval-patterns-for-the-modes
# > https://en.wikipedia.org/wiki/Minor_scale

class Scale :

  def __init__(self, root = "C", mode = "major", startTime = 0) :
    
    self.startTime = startTime
    self.root = root
    self.mode = mode
    
    self.MAJOR_INTERVALS = [2, 2, 1, 2, 2, 2, 1]
    self.MINOR_INTERVALS = [2, 1, 2, 2, 1, 2, 2]
    self.NOTE_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

    self.activeNotes = [0, 2, 4, 5, 7, 9, 11]  # Default is C maj
    self.selector = 0



  def _update(self) :
    
    # *** Selector = 0: no active scale ***
    if (self.selector == SCALE_DISABLED) :
      self.activeNotes = []
    
    # *** Selector = 1 ... 12: major scales ***
    elif ((self.selector >= 1) and (self.selector <= 12)) :
      self.root = self.NOTE_NAMES[self.selector-1]
      self.mode = "major"
      
      # Generate the scale
      scale = [self.selector-1]
      for interval in self.MAJOR_INTERVALS :
          scale.append((scale[-1] + interval) % 12)
    
      # Map the scale to integer codes
      self.activeNotes = sorted(scale)
    
    # *** Selector = 13 ... 24: minor scales ***
    else :
      self.root = self.NOTE_NAMES[self.selector-13]
      self.mode = "minor"
      
      # Generate the scale
      scale = [self.selector-13]
      for interval in self.MINOR_INTERVALS :
          scale.append((scale[-1] + interval) % 12)
    
      # Map the scale to integer codes
      self.activeNotes = sorted(scale)



  def nextRoot(self) :
    self.selector = (self.selector + 1) % 25
    self._update()



  def previousRoot(self) :
    self.selector = (self.selector - 1) % 25
    self._update()




  def generateScale(self) :
    print("TODO")



# =============================================================================
# Keystrokes handling function
# =============================================================================
# Function takes as argument the list of key pressed (as indicated by pygame)
def keystrokeTest(keyStatus, *args) :
  print("TODO")



# =============================================================================
# Color manipulation function
# =============================================================================
def adjustHSV(rgbColor, deltaHue, deltaSat, deltaVal) :

  # Normalize input RGB
  (R,G,B) = (x/255.0 for x in rgbColor)

  # Convert to HSV
  (H,S,V) = colorsys.rgb_to_hsv(R,G,B)

  # Apply correction
  # TODO : add guards
  (H,S,V) = ((H + (deltaHue/360.0)) % 1.0, S + (deltaSat/100.0), V + (deltaVal/100.0))

  # Convert back to RGB
  (R,G,B) = colorsys.hsv_to_rgb(H,S,V)

  return (int(R*255.0), int(G*255.0), int(B*255.0))
