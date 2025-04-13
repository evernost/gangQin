# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : pianoRoll
# File name     : main.py
# Purpose       : provides a piano roll widget for the main app GUI
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Friday, 1 Sept 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from src.commons import *

import src.widgets.widget as widget

import pygame



# =============================================================================
# Constants pool
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class PianoRoll(widget.Widget) :

  """
  Piano roll widget.
  """

  def __init__(self, top, loc) :
    
    # Call the Widget init method
    super().__init__(top, loc)
  
    # Drawing location
    self.x = loc[0]
    self.yTop = loc[1]
    self.yBottom = 300-2

    # Defines the amount of notes shown in the piano roll view
    # Units are in timecodes. Use "avgNoteDuration" to use it conveniently
    self.viewSpan = 1000

    self.noteArray = [[] for _ in range(128)]
    self.nStaffs = 0
    
    # Color scheme
    self.backgroundRGB = PIANOROLL_BACKGROUND_COLOR         # Background color for the piano roll
    self.keyLineRGB = PIANOROLL_NOTE_LINE_COLOR            # Color of the lines separating each notes in the piano roll
    self.leftNoteOutlineRGB = (243, 35, 35)   # Border color for the notes in the piano roll
    self.rightNoteOutlineRGB = (35, 243, 118)
    self.leftNoteRGB = PIANOROLL_NOTE_COLOR_LEFT_HAND        # Color of a left hand note in piano roll
    self.rightNoteRGB = PIANOROLL_NOTE_COLOR_RIGHT_HAND      # Color of a right hand note in piano roll
    
    # Shortcuts for the key sizes
    self.b = KEYBOARD_WHITE_NOTE_WIDTH
    self.d = KEYBOARD_BLACK_NOTE_WIDTH
    self.e = KEYBOARD_NOTE_SPACING

    # UI interaction queues
    self._altPressed = False
    self.msgQueueIn = []
    self.msgQueueOut = []



  # ---------------------------------------------------------------------------
  # METHOD <_drawKeyLines> (private)
  #
  # Draw the thin lines in-between each note.
  # ---------------------------------------------------------------------------
  def _drawKeyLines(self, screenInst) :

    # Some shortcuts
    x0 = self.x
    b = self.b
    d = self.d

    self.xLines = [
      x0,                 # begin(A0)
      x0+(1*b)-(d//3),    # begin(Bb0)
      x0+(1*b)+(2*d//3),  # begin(B0)
    ]
    x0 = x0+(2*b)         # end(B0) = begin(C0)
    
    for oct in range(7) :
      self.xLines += [
        x0,
        x0+(1*b)-(2*d//3),
        x0+(1*b)+(d//3),
        x0+(2*b)-(d//3),
        x0+(2*b)+(2*d//3),
        x0+(3*b),
        x0+(4*b)-(2*d//3),
        x0+(4*b)+(d//3),
        x0+(5*b)-(d//2),
        x0+(5*b)+(d//2),
        x0+(6*b)-(d//3),
        x0+(6*b)+(2*d//3)
      ]

      x0 += 7*b

    self.xLines += [
      x0,
      x0+(1*b)
    ]

    # Draw the background rectangle
    backRect = [
      (self.xLines[0], self.yBottom),
      (self.xLines[-1], self.yBottom),
      (self.xLines[-1], self.yTop),
      (self.xLines[0], self.yTop)
    ]
    pygame.draw.polygon(screenInst, self.backgroundRGB, backRect)


    # Draw the lines
    for x in self.xLines :
      pygame.draw.line(screenInst, self.keyLineRGB, (x, self.yTop), (x, self.yBottom), 1)

    # Close the rectangle
    pygame.draw.line(screenInst, self.keyLineRGB, (self.xLines[0], self.yTop), (self.xLines[-1], self.yTop), 1)



  # ---------------------------------------------------------------------------
  # METHOD <drawPianoRoll>
  #
  # Draw the note content of the piano roll at the current time
  # ---------------------------------------------------------------------------
  def drawPianoRoll(self, screenInst, startTimeCode) :
    
    # Draw the background and inner components
    self._drawKeyLines(screenInst)

    # List the notes that intersect the current window
    notesInWindow = []

    # Draw the notes
    # NOTE: some processing could be avoided here since the notes are sorted by startTime
    # Once the notes start way after the end of the window, why bother exploring the rest?
    for (staffIndex, _) in enumerate(self.noteArray) :
      for pitch in GRAND_PIANO_MIDI_RANGE :
        for note in self.noteArray[staffIndex][pitch] :
          
          # Shortcuts
          a = startTimeCode; b = startTimeCode + self.viewSpan
          c = note.startTime; d = note.stopTime
        
          # Does the note span intersect the current view window?
          if (((c >= a) and (c < b)) or ((d >= a) and (d < b)) or ((c <= a) and (d >= b))) :
            notesInWindow.append(note)

    # Sort the notes to display them in a given order.
    # Longest notes are displayed first
    notesInWindow.sort(key = lambda x : -(x.stopTime-x.startTime))

    # Draw the notes
    for note in notesInWindow :

      # Shortcuts
      a = startTimeCode; b = startTimeCode + self.viewSpan
      c = note.startTime; d = note.stopTime

      # Convert the size measured in "time" to a size in pixels
      rectBottom = -((self.yBottom-self.yTop)*(c-b)/(b-a)) + self.yTop
      rectTop = -((self.yBottom-self.yTop)*(d-b)/(b-a)) + self.yTop
      
      # Trim the rectangle representing the note to the current view
      rectBottom = max([rectBottom, self.yTop]); rectBottom = min([rectBottom, self.yBottom])
      rectTop = max([rectTop, self.yTop]); rectTop = min([rectTop, self.yBottom])

      sq = [(self.xLines[note.pitch-21]+2, rectBottom),
            (self.xLines[note.pitch-21]+2, rectTop),
            (self.xLines[note.pitch+1-21]-2, rectTop),
            (self.xLines[note.pitch+1-21]-2, rectBottom)
          ]
      
      # TODO: replace with a call to getNoteColor()
      if (note.hand == LEFT_HAND) :
        color = self.leftNoteOutlineRGB
      
      if (note.hand == RIGHT_HAND) :
        color = self.rightNoteOutlineRGB

      (rectColor, rectOutlineColor, pianoRollColor) = note.getNoteColor()
      pygame.draw.line(screenInst, color, sq[0], sq[1], 3)
      pygame.draw.line(screenInst, color, sq[1], sq[2], 3)
      pygame.draw.line(screenInst, color, sq[2], sq[3], 3)
      pygame.draw.line(screenInst, color, sq[3], sq[0], 3)
      
      pygame.draw.polygon(screenInst, rectColor, sq)
            



    

  # ---------------------------------------------------------------------------
  # METHOD PianoRoll.loadPianoRoll(noteArray)
  # ---------------------------------------------------------------------------
  def loadPianoRoll(self, noteArray) :
    """
    TODO
    """

    # Use .copy instead of direct assign for safety 
    # (we don't want the pianoroll widget to mess with the real score)
    self.noteArray = noteArray.copy()



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'pianoRoll.py'")

