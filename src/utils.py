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



# ---------------------------------------------------------------------------
# FUNCTION <noteName>
#
# Converts a MIDI code (integer) to a human understandable note name
# ---------------------------------------------------------------------------
def noteName(midiCode) :
    
    if ((midiCode > 0) and (midiCode < 128)) :
      # List of note names
      noteRefs = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

      # Calculate the octave and note index
      octave = (midiCode // 12) - 1
      noteIndex = midiCode % 12

      # Create the note name
      return f"{noteRefs[noteIndex]}{octave}"

    else :
      return ""



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
# NOTE object
# =============================================================================
class Note :

  def __init__(self, pitch, hand = UNDEFINED_HAND, finger = 0, noteIndex = 0, startTime = 0, stopTime = 0, voice = VOICE_DEFAULT, highlight = False) :
    
    # General common attributes of a note
    self.pitch = pitch
    self.hand = hand
    self.finger = finger
    self.keyColor = WHITE_KEY if ((pitch % 12) in WHITE_NOTES_CODE_MOD12) else BLACK_KEY
    
    # Info relative to the pianoroll
    self.noteIndex = noteIndex
    self.startTime = startTime
    self.stopTime = stopTime
    self.sustained = False          # True if the note is held at a given time (note will be ignored by the arbiter)
    self.highlight = highlight      # True if its fingersatz is being edited
    self.inactive = False           # True if the note shall be ignored by the arbiter (single hand practice)
    self.disabled = False           # True if the note shall be ignored by the arbiter (unplayable note)
    self.fromKeyboardInput = False  # True if it is a note played by the user from the MIDI input
    self.voice = voice              # Define the voice the note belongs to, if another is needed on top of the usual left/right voice
    self.lookAheadDistance = 0      # Define how far away this note is located relative to the current cursor
    
    # Not used anymore?
    self.name = noteName(self.pitch)
    self.id = -1
    self.visible = False
    


  # ---------------------------------------------------------------------------
  # getNoteColor()
  # ---------------------------------------------------------------------------
  def getNoteColor(self) :

    if (self.voice != VOICE_DEFAULT) :
      baseColor = VOICE_COLOR[self.voice]
    else :
      if (self.hand == LEFT_HAND) :
        baseColor = adjustHSV((255, 0, 0), 0, -20, -10)
      else :
        baseColor = adjustHSV((0, 255, 0), 0, -20, -20)
      

    # Disabled note (unplayable, wrong, etc.) ---------------------------------
    # Same color no matter what the voice is.
    # 'sustained', 'highlight', 'voice', 'lookAheadDistance' attributes are all ignored.
    if self.disabled :

      if (self.lookAheadDistance > 0) :
        print("[ERROR] A disabled note cannot have a non-zero lookahead")

      if (self.keyColor == WHITE_KEY) :
        (rectColor, rectOutlineColor, pianoRollColor) = ((200, 200, 200), (170, 170, 170), (250, 250, 250))
      
      else :
        (rectColor, rectOutlineColor, pianoRollColor) = ((80, 80, 80), (100, 100, 100), (120, 120, 120))
        
    else :

      # Highlighted note for fingersatz editing -------------------------------
      if self.highlight :

        if (self.hand == LEFT_HAND) :
          hueShift = 30
        else :
          hueShift = 60

        if (self.keyColor == WHITE_KEY) :
          (rectColor, rectOutlineColor, pianoRollColor) = (adjustHSV(baseColor, hueShift, 0, 0), adjustHSV(baseColor, hueShift, 0, -50), adjustHSV(baseColor, hueShift, 0, 0))

        else :
          (rectColor, rectOutlineColor, pianoRollColor) = (adjustHSV(baseColor, hueShift, 0, 0), adjustHSV(baseColor, hueShift, 0, -50), adjustHSV(baseColor, hueShift, 0, 0))

      # Inactive note (single hand practice) ----------------------------------
      elif self.inactive :

        if (self.keyColor == WHITE_KEY) :
          (rectColor, rectOutlineColor, pianoRollColor) = (adjustHSV(baseColor, 0, -60, 0), (240, 240, 240), adjustHSV(baseColor, 0, -60, 0))
        
        else :
          (rectColor, rectOutlineColor, pianoRollColor) = (adjustHSV(baseColor, 0, -60, 0), (170, 170, 170), adjustHSV(baseColor, 0, -60, 0))
            
      else :

        # Sustained note ------------------------------------------------------
        if (self.sustained) :

          if (self.keyColor == WHITE_KEY) :
            (rectColor, rectOutlineColor, pianoRollColor) = (adjustHSV(baseColor, 0, -60, 0), (160, 160, 160), adjustHSV(baseColor, 0, -60, 0))
            
          else :
            (rectColor, rectOutlineColor, pianoRollColor) = (adjustHSV(baseColor, 0, 0, -30), (80, 80, 80), adjustHSV(baseColor, 0, 0, -30))

        # Normal note ---------------------------------------------------------
        else : 
          
          if (self.keyColor == WHITE_KEY) :
            (rectColor, rectOutlineColor, pianoRollColor) = (baseColor, (10, 10, 10), baseColor)
            
          else :
            (rectColor, rectOutlineColor, pianoRollColor) = (baseColor, (80, 80, 80), baseColor)


    return (rectColor, rectOutlineColor, pianoRollColor)


  
  # ---------------------------------------------------------------------------
  # print() function overloading
  # ---------------------------------------------------------------------------
  def __str__(self) :
    if (self.hand == RIGHT_HAND) : handStr = "right hand"
    if (self.hand == LEFT_HAND) : handStr = "left hand"
    if (self.keyColor == WHITE_KEY) : keyColorStr = "white key"
    if (self.keyColor == BLACK_KEY) : keyColorStr = "black key"

    ret = f"""Note object properties
    - pitch:     {self.pitch}
    - hand:      {self.hand} ({handStr})
    - finger:    {self.finger}
    - key color: {keyColorStr}
    - index:     {self.noteIndex}
    - start:     {self.startTime}
    - stop:      {self.stopTime}
    - visible:   {self.visible}
    - sustained: {self.sustained}
    - highlight: {self.highlight}
    - name:      {self.name}
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
