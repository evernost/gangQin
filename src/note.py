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
# External libs
# =============================================================================
# Project specific constants
from src.commons import *

import src.utils as utils




class Note :

  """
  NOTE object
  
  TODO
  """

  def __init__(self, pitch, hand = NOTE_UNDEFINED_HAND, finger = 0, noteIndex = 0, startTime = 0, stopTime = 0, voice = NOTE_VOICE_DEFAULT, highlight = False) :
    
    # General common attributes of a note
    self.pitch = pitch
    self.hand = hand
    self.finger = finger
    self.keyColor = NOTE_WHITE_KEY if ((pitch % 12) in MIDI_CODE_WHITE_NOTES_MOD12) else NOTE_BLACK_KEY
    
    # Info relative to the pianoroll
    self.noteIndex = noteIndex      # Index of the note in this pitch
    self.startTime = startTime
    self.stopTime = stopTime
    self.sustained = False          # True if the note is held at a given time (note will be ignored by the arbiter)
    self.highlight = highlight      # True if its fingersatz is being edited
    self.inactive = False           # True if the note shall be ignored by the arbiter (single hand practice)
    self.disabled = False           # True if the note shall be ignored by the arbiter (unplayable note)
    self.upcoming = False           # True if the note is about to be played soon
    self.upcomingDistance = 0       # The highest the value, the further the note
    self.fromKeyboardInput = False  # True if it is a note played by the user from the MIDI input
    self.voice = voice              # Define the voice the note belongs to, if another is needed on top of the usual left/right voice
    self.lookAheadDistance = 0      # Define how far away this note is located relative to the current cursor
    
    # Not used anymore?
    self.name = getFriendlyName(self.pitch)
    self.id = -1
    self.visible = False
    


  # ---------------------------------------------------------------------------
  # getNoteColor()
  # ---------------------------------------------------------------------------
  def getNoteColor(self) :
    """
    Returns the RGB color (as a 3-tuple) of the note based on its properties.
    """


    if (self.voice != NOTE_VOICE_DEFAULT) :
      baseColor = VOICE_COLOR[self.voice]
    else :
      if (self.hand == NOTE_LEFT_HAND) :
        if (self.upcoming) :
          baseColor = utils.adjustHSV((255, 0, 127), 0, -40 - (self.upcomingDistance*20), -10)
        else :
          baseColor = utils.adjustHSV((255, 0, 0), 0, -20, -10)

      else :
        if (self.upcoming) :
          baseColor = utils.adjustHSV((0, 255, 127), 0, -40 - (self.upcomingDistance*20), -20)
        else :
          baseColor = utils.adjustHSV((0, 255, 0), 0, -20, -20)
      

    # Disabled note (unplayable, wrong, etc.) ---------------------------------
    # Same color no matter what the voice is.
    # 'sustained', 'highlight', 'voice', 'lookAheadDistance' attributes are all ignored.
    if self.disabled :

      if (self.keyColor == NOTE_WHITE_KEY) :
        (rectColor, rectOutlineColor, pianoRollColor) = ((200, 200, 200), (170, 170, 170), (250, 250, 250))
      
      else :
        (rectColor, rectOutlineColor, pianoRollColor) = ((80, 80, 80), (100, 100, 100), (120, 120, 120))
        
    else :

      # Highlighted note for fingersatz editing -------------------------------
      if self.highlight :

        if (self.hand == NOTE_LEFT_HAND) :
          hueShift = 30
        else :
          hueShift = 60

        if (self.keyColor == NOTE_WHITE_KEY) :
          (rectColor, rectOutlineColor, pianoRollColor) = (utils.adjustHSV(baseColor, hueShift, 0, 0), utils.adjustHSV(baseColor, hueShift, 0, -50), utils.adjustHSV(baseColor, hueShift, 0, 0))

        else :
          (rectColor, rectOutlineColor, pianoRollColor) = (utils.adjustHSV(baseColor, hueShift, 0, 0), utils.adjustHSV(baseColor, hueShift, 0, -50), utils.adjustHSV(baseColor, hueShift, 0, 0))

      # Inactive note (single hand practice) ----------------------------------
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
  # print() function overloading
  # ---------------------------------------------------------------------------
  def __str__(self) :
    if (self.hand == NOTE_RIGHT_HAND) : handStr = "right hand"
    if (self.hand == NOTE_LEFT_HAND) : handStr = "left hand"
    if (self.keyColor == NOTE_WHITE_KEY) : keyColorStr = "white key"
    if (self.keyColor == NOTE_BLACK_KEY) : keyColorStr = "black key"

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



# -----------------------------------------------------------------------------
# METHOD: Note.getFriendlyName(pitchList)
# -----------------------------------------------------------------------------
def getFriendlyName(midiCode) :
  """
  Converts a MIDI code (integer) to a human understandable note name.
  
  EXAMPLES
  getFriendlyName(60) = "C4"
  """
    
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
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'note.py'")

