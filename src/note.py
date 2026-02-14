# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : note
# File name     : note.py
# File type     : Python script (Python 3)
# Purpose       : note object definition
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : July 26th, 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project libraries
from src.commons import *
import src.utils as utils

# Standard libraries
from enum import Enum     # For enumerated types



# =============================================================================
# CONSTANTS
# =============================================================================
class keyColor_T(Enum) :
  WHITE_NOTE = 0
  BLACK_NOTE = 1

class hand_T(Enum) :
  UNDEFINED = -1
  LEFT      = 0
  RIGHT     = 1

class finger_T(Enum) :
  UNDEFINED = 0
  FINGER_1  = 1
  FINGER_2  = 2
  FINGER_3  = 3
  FINGER_4  = 4
  FINGER_5  = 5



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Note :

  """
  NOTE object
  
  The Note object is a representation of a musical note with all the properties
  necessary accross the different objects. 
  
  Do not change the pitch afterwards.
  """

  def __init__(self, pitch) :
    
    # Note general attributes (fields preserved during file import/export)
    self.pitch    = pitch
    self.hand     = NOTE_UNDEFINED_HAND
    self.finger   = NOTE_UNDEFINED_FINGER
    self.name     = getFriendlyName(pitch)
    self.voice    = NOTE_VOICE_DEFAULT
    self.velocity = 0

    # Note database attributes (fields partially preserved during file import/export)
    self.startTime  = 0                 # Timecode of the key press event
    self.stopTime   = NOTE_END_UNKNOWN  # Timecode of the key release event
    self.dbIndex    = -1                # Index of the note in the score database
    self.id         = -1                # Note unique identifier in the score (might change from a session to the other)
    
    # Note display attributes (fields not preserved during file import/export)
    self.color      = None
    self.keyColor   = self._getKeyColor()   # White or Black note
    self.sustained  = False                 # True if the note is held at a given time
    self.highlight  = False                 # True if the note fingersatz is being edited
    self.inactive   = False                 # True if the note shall be ignored by the arbiter (single hand practice)
    self.upcoming   = False                 # True if the note is about to be played soon
    self.upcomingDistance = 0               # The higher the value, the further the note in the score from the current location
    self.fromKeyboardInput  = False         # True if it is a note played by the user from the MIDI input

    # Not used anymore?
    self.visible            = False
    self.disabled           = False   # True if the note shall be ignored by the arbiter (unplayable note)
    self.lookAheadDistance  = 0       # Define how far away this note is located relative to the current cursor
    


  # ---------------------------------------------------------------------------
  # METHOD: Note._getKeyColor()                                       [PRIVATE]
  # ---------------------------------------------------------------------------
  def _getKeyColor(self) :
    """
    Returns the color of the note on a piano keyboard (black or white note)
    """

    if (self.pitch % 12) in MIDI_CODE_WHITE_NOTES_MOD12 :
      return keyColor_T.WHITE_NOTE
    else :
      return keyColor_T.BLACK_NOTE



  # ---------------------------------------------------------------------------
  # METHOD: Note.getNoteColor()
  # ---------------------------------------------------------------------------
  def getNoteColor(self) :
    """
    Returns the color of 3 elements of the note:
    - the rectangle overlay on the keyboard
    - the outline of the rectangle overlay on the keyboard
    - the rectangle on the piano roll

    All 3 are a 3-tuples with the RGB values.
    """

    # 
    # Non-default voices (unsupported yet)
    #
    if (self.voice != NOTE_VOICE_DEFAULT) :
      baseColor = VOICE_COLOR[self.voice]
    
    # 
    # Default voices and notes types
    #
    else :
      if (self.hand == NOTE_LEFT_HAND) :
        if (self.upcoming) :
          baseColor = utils.adjustHSV((255, 0, 127), 0, -40 - (self.upcomingDistance*20), -10)
        else :
          baseColor = utils.adjustHSV(KEYBOARD_NOTE_COLOR_LEFT_HAND, 0, -20, -10)

      else :
        if (self.upcoming) :
          baseColor = utils.adjustHSV((0, 255, 127), 0, -40 - (self.upcomingDistance*20), -20)
        else :
          baseColor = utils.adjustHSV(KEYBOARD_NOTE_COLOR_RIGHT_HAND, 0, -20, -20)
  
    #
    # Disabled note (unplayable, wrong, etc.)
    #
    # [DEPRECATED]
    #if self.disabled :
    if False :

      if (self.keyColor == NOTE_WHITE_KEY) :
        (rectColor, rectOutlineColor, pianoRollColor) = ((200, 200, 200), (170, 170, 170), (250, 250, 250))
      
      else :
        (rectColor, rectOutlineColor, pianoRollColor) = ((80, 80, 80), (100, 100, 100), (120, 120, 120))
        
    else :

      #
      # Highlighted note for fingersatz edition
      #
      if self.highlight :

        if (self.hand == NOTE_LEFT_HAND) :
          hueShift = 30
        else :
          hueShift = 60

        if (self.keyColor == NOTE_WHITE_KEY) :
          (rectColor, rectOutlineColor, pianoRollColor) = (utils.adjustHSV(baseColor, hueShift, 0, 0), utils.adjustHSV(baseColor, hueShift, 0, -50), utils.adjustHSV(baseColor, hueShift, 0, 0))
        else :
          (rectColor, rectOutlineColor, pianoRollColor) = (utils.adjustHSV(baseColor, hueShift, 0, 0), utils.adjustHSV(baseColor, hueShift, 0, -50), utils.adjustHSV(baseColor, hueShift, 0, 0))

      #
      # Inactive note (single hand practice)
      #
      elif self.inactive :

        if (self.keyColor == NOTE_WHITE_KEY) :
          (rectColor, rectOutlineColor, pianoRollColor) = (utils.adjustHSV(baseColor, 0, -70, 0), (240, 240, 240), utils.adjustHSV(baseColor, 0, -60, 0))
        else :
          (rectColor, rectOutlineColor, pianoRollColor) = (utils.adjustHSV(baseColor, 0, -70, 0), (170, 170, 170), utils.adjustHSV(baseColor, 0, -60, 0))
            
      else :

        # Upcoming note -------------------------------------------------------
        if (self.upcoming) :
          if (self.keyColor == NOTE_WHITE_KEY) :
            (rectColor, rectOutlineColor, pianoRollColor) = (baseColor, (255, 255, 255), baseColor)
          else :
            (rectColor, rectOutlineColor, pianoRollColor) = (baseColor, (0, 0, 0), baseColor)

        # Sustained note ------------------------------------------------------
        if (self.sustained) :
          if (self.keyColor == NOTE_WHITE_KEY) :
            (rectColor, rectOutlineColor, pianoRollColor) = (utils.adjustHSV(baseColor, 0, -60, 0), (160, 160, 160), utils.adjustHSV(baseColor, 0, -60, 0))
          else :
            (rectColor, rectOutlineColor, pianoRollColor) = (utils.adjustHSV(baseColor, 0, 0, -30), (80, 80, 80), utils.adjustHSV(baseColor, 0, 0, -30))

        # Normal note ---------------------------------------------------------
        else : 
          if (self.keyColor == NOTE_WHITE_KEY) :
            (rectColor, rectOutlineColor, pianoRollColor) = (baseColor, (10, 10, 10), baseColor)
          else :
            (rectColor, rectOutlineColor, pianoRollColor) = (baseColor, (80, 80, 80), baseColor)


    return (rectColor, rectOutlineColor, pianoRollColor)



  # ---------------------------------------------------------------------------
  # METHOD: Note.setPitch()
  # ---------------------------------------------------------------------------
  def setPitch(self, newPitch: int) -> None :
    """
    Changes the pitch of the note.
    Do not try to modify the 'pitch' attribute manually as some side attributes
    would not be up to date anymore.
    """
      
    self.pitch    = newPitch
    self.name     = getFriendlyName(newPitch)
    self.keyColor = self._getKeyColor()



  # ---------------------------------------------------------------------------
  # METHOD: Note.start()
  # ---------------------------------------------------------------------------
  def start(self, startTime: int) -> None :
    """
    Sets the start time attribute of the note.
    """
      
    self.startTime = startTime



  # ---------------------------------------------------------------------------
  # METHOD: Note.stop()
  # ---------------------------------------------------------------------------
  def stop(self, stopTime: int) -> None :
    """
    Sets the stop time attribute of the note.
    Warning: unlike 'Note.stop()', this method does not overwrite the 'stopTime'
    attribute but appends a stop time to the list.

    MIDI notation causes inherent ambiguity on the stop time: more than 1 
    'note on' event can occur on the same hand and pitch before it is even 
    released. 
    To let the user choose the proper note duration, all possible stoptime are
    stored.
    """
    
    self.stopTime = stopTime



  # ---------------------------------------------------------------------------
  # METHOD: Note.toDict()
  # ---------------------------------------------------------------------------
  def toDict(self) :
    """
    Generates a dictionary with the attributes that need to be exported 
    """
      
    out = {
      "pitch"   : self.pitch,
      "hand"    : self.hand,
      "finger"  : self.finger,
      "voice"   : self.voice,
      "name"    : self.name
    }

    return out



  # ---------------------------------------------------------------------------
  # METHOD: Note.__str__() (overloading of the standard 'print')
  # ---------------------------------------------------------------------------
  def __str__(self) -> str :
    """
    Defines a pretty print formatting for the Note object.
    """
    
    if (self.hand == NOTE_RIGHT_HAND)     : strHand = "right hand"
    if (self.hand == NOTE_LEFT_HAND)      : strHand = "left hand"
    if (self.hand == NOTE_UNDEFINED_HAND) : strHand = "undefined"

    if (self.keyColor == keyColor.WHITE_NOTE) : strKeyColor = "white key"
    if (self.keyColor == keyColor.BLACK_NOTE) : strKeyColor = "black key"

    strFinger = "undefined" if (self.finger == NOTE_UNDEFINED_FINGER) else self.finger

    ret = f"""Note object properties
    - pitch:     {self.pitch}
    - name:      {self.name}
    - hand:      {self.hand} ({strHand})
    - finger:    {strFinger}
    - key color: {strKeyColor}
    - dbIndex:   {self.dbIndex}
    - start:     {self.startTime}
    - stop:      {self.stopTime}
    - visible:   {self.visible}
    - sustained: {self.sustained}
    - highlight: {self.highlight}
    - id:        {self.id}
    """
    
    return ret



  # # ---------------------------------------------------------------------------
  # # METHOD: Note._getFriendlyName()                                   [PRIVATE]
  # # ---------------------------------------------------------------------------
  # def _getFriendlyName(self) :
  #   """
  #   Converts a MIDI code (integer) to a human understandable note name.
    
  #   EXAMPLES
  #   > Note(60)._getFriendlyName(60) = "C4"
  #   """
      
  #   if ((self.pitch > 0) and (self.pitch < 128)) :
  #     noteRefs = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
  #     octave = (self.pitch // 12) - 1
  #     noteIndex = self.pitch % 12

  #     return f"{noteRefs[noteIndex]}{octave}"
  #   else :
  #     return ""


# ---------------------------------------------------------------------------
# UTILITY: getFriendlyName()
# ---------------------------------------------------------------------------
def getFriendlyName(pitch) -> str :
  """
  Converts a MIDI code (integer) to a human understandable note name.
  
  TODO: add an option to choose flats or sharps

  EXAMPLES
  > Note(60)._getFriendlyName(60) = "C4"
  """
    
  if ((pitch > 0) and (pitch < 128)) :
    noteRefs = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    octave = (pitch // 12) - 1
    noteIndex = pitch % 12

    return f"{noteRefs[noteIndex]}{octave}"
  else :
    return ""



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] Library 'Note' called as main: running unit tests...")

  N = Note(64)
  print(N)
