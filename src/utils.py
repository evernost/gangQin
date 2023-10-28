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



# =============================================================================
# Constants pool
# =============================================================================



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")




def noteName(midiCode) :
    
    if ((midiCode > 0) and (midiCode < 128)) :
      # List of note names
      note_names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

      # Calculate the octave and note index
      octave = (midiCode // 12) - 1
      note_index = midiCode % 12

      # Create the note name
      return f"{note_names[note_index]}{octave}"

    else :
      return ""



# =============================================================================
# Class: Vector2D 
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
# NOTE object
# =============================================================================
class Note :

  def __init__(self, pitch, hand = UNDEFINED_HAND, finger = 0, noteIndex = 0, startTime = 0, stopTime = 0, voice = VOICE_DEFAULT, highlight = False) :
    
    # General common attributes of a note
    self.pitch = pitch
    self.hand = hand
    self.finger = finger
    
    # Info relative to the pianoroll
    self.noteIndex = noteIndex
    self.startTime = startTime
    self.stopTime = stopTime
    self.voice = voice
    self.highlight = highlight
    self.mustPlay = False
    self.id = -1
    

  def __str__(self) :
    noteNameStr = noteName(self.pitch)
    if (self.hand == RIGHT_HAND) : handStr = "R"
    if (self.hand == LEFT_HAND) : handStr = "L"

    ret = f"""Note object properties
    - pitch:     {self.pitch} ({noteNameStr})
    - hand:      {self.hand} ({handStr})
    - finger:    {self.finger}
    - index:     {self.noteIndex}
    - start:     {self.startTime}
    - stop:      {self.stopTime}
    - highlight: {self.highlight}
    - id:        {self.id}
    """
    return ret


# =============================================================================
# SCALE object
# =============================================================================
# References: 
# > https://music.stackexchange.com/questions/73110/what-are-the-interval-patterns-for-the-modes
# > https://en.wikipedia.org/wiki/Minor_scale


class Scale :

  def __init__(self, key, mode) :
    
    self.key = key
    self.mode = mode
    
    self.MAJOR_SCALE_MODE = [2, 2, 1, 2, 2, 2, 1]
    self.MINOR_SCALE_MODE = [2, 1, 2, 2, 1, 2, 2]
    self.C_KEY = 0
    self.D_KEY = 2
    self.E_KEY = 4
    self.F_KEY = 5

  def generateScale(self) :
    print("TODO")





# =============================================================================
# Keystrokes handling function
# =============================================================================
# Function takes as argument the list of key pressed (as indicated by pygame)
def keystrokeTest(keyStatus, *args) :
  print("TODO")