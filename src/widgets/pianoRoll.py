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
from commons import *

# For point in polygon test
from shapely.geometry import Point, Polygon

import pygame



# =============================================================================
# Constants pool
# =============================================================================



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")



# =============================================================================
# Main code
# =============================================================================

class PianoRoll :

  # ---------------------------------------------------------------------------
  # Constructor
  # ---------------------------------------------------------------------------
  def __init__(self, x, yTop, yBottom) :
    # Drawing localisation
    self.x = x
    self.yTop = yTop
    self.yBottom = yBottom

    # Defines the amount of notes shown in the piano roll view
    # Units are in timecodes. Use <avgNoteDuration> to use it conveniently
    self.viewSpan = 1000

    self.noteArray = [[] for _ in range(128)]
    self.nStaffs = 0
    
    self.teacherNotes = []
    self.teacherNotesPolygons = []
    self.teacherMidi = []

    # TODO: add comments to explain the meaning of this
    self.activeNoteClicked = ()

    # Color scheme
    self.backgroundRGB = (80, 80, 80)         # Background color for the piano roll
    self.keyLineRGB = (50, 50, 50)            # Color of the lines separating each notes in the piano roll
    self.leftNoteOutlineRGB = (35, 243, 118)  # Border color for the notes in the piano roll
    self.rightNoteOutlineRGB = (243, 35, 35)       
    self.leftNoteRGB = (165, 250, 200)        # Color of a left hand note in piano roll
    self.rightNoteRGB = (250, 165, 165)       # Color of a right hand note in piano roll
    
    # Shortcuts for the key sizes
    self.b = WHITE_NOTE_WIDTH
    self.d = BLACK_NOTE_WIDTH
    self.e = NOTE_SPACING



  # ---------------------------------------------------------------------------
  # METHOD <_drawKeyLines> (private)
  #
  # Draw the thin lines in-between each note
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

    # Draw the notes
    for (staffIndex, _) in enumerate(self.noteArray) :
      for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        for note in self.noteArray[staffIndex][pitch] :
          a = startTimeCode; b = startTimeCode + self.viewSpan
          c = note.startTime; d = note.stopTime
        
          # Does the note span intersect the current view window?
          if (((c >= a) and (c < b)) or ((d >= a) and (d < b)) or ((c <= a) and (d >= b))) :
            
            # Convert the size measured in "time" to a size in pixels
            rectBottom = -((self.yBottom-self.yTop)*(c-b)/(b-a)) + self.yTop
            rectTop = -((self.yBottom-self.yTop)*(d-b)/(b-a)) + self.yTop
            
            # Trim the rectangle representing the note to the current view
            rectBottom = max([rectBottom, self.yTop]); rectBottom = min([rectBottom, self.yBottom])
            rectTop = max([rectTop, self.yTop]); rectTop = min([rectTop, self.yBottom])

            sq = [(self.xLines[pitch-21]+2, rectBottom),
                  (self.xLines[pitch-21]+2, rectTop),
                  (self.xLines[pitch+1-21]-2, rectTop),
                  (self.xLines[pitch+1-21]-2, rectBottom)
                ]
            
            # Draw the note outline
            if (staffIndex == LEFT_HAND) :
              color = self.leftNoteOutlineRGB
            else :
              color = self.rightNoteOutlineRGB

            pygame.draw.line(screenInst, color, sq[0], sq[1], 3)
            pygame.draw.line(screenInst, color, sq[1], sq[2], 3)
            pygame.draw.line(screenInst, color, sq[2], sq[3], 3)
            pygame.draw.line(screenInst, color, sq[3], sq[0], 3)
            
            if (staffIndex == 0) :
              pygame.draw.polygon(screenInst, self.leftNoteRGB, sq)
            
            if (staffIndex == 1) :
              pygame.draw.polygon(screenInst, self.rightNoteRGB, sq)



  # ---------------------------------------------------------------------------
  # METHOD <isActiveNoteClicked>
  #
  # Based on a click coordinates, indicate whether it is a key that is lit or not
  # Return value: True or False
  # Updates the attribute <activeNoteClicked> with the info about the note
  # that has been clicked.
  # ---------------------------------------------------------------------------
  def isActiveNoteClicked(self, clickX, clickY, litKeysPolygons) :

    for (sq, pitchCurr) in litKeysPolygons :
      pol = Polygon(sq)
      p = Point(clickX, clickY)

      # Intersection!
      if p.within(pol) :

        # Find the corresponding note in pianoRoll
        for (track, pitch, noteIndex) in self.teacherNotes :
          if (pitch == pitchCurr) :
            # print(f"You try to edit the following note in pianoRoll:")
            # print(f"- startTime = {self.noteArray[track][pitch][noteIndex].startTime}")
            # print(f"- stopTime = {self.noteArray[track][pitch][noteIndex].stopTime}")
            self.activeNoteClicked = self.noteArray[track][pitch][noteIndex]
            return True

    return False
  


  # ---------------------------------------------------------------------------
  # METHOD <getActiveNoteClicked>
  #
  # TODO
  # ---------------------------------------------------------------------------
  def getActiveNoteClicked(self) :
    return self.activeNoteClicked
  


  # ---------------------------------------------------------------------------
  # METHOD <updateNoteProperties>
  #
  # TODO
  # ---------------------------------------------------------------------------
  def updateNoteProperties(self, note) :
    self.noteArray[note.hand][note.pitch][note.noteIndex].finger = note.finger

    

  # ---------------------------------------------------------------------------
  # METHOD <importPianoRoll>
  #
  # TODO
  # ---------------------------------------------------------------------------
  def loadPianoRoll(self, noteArray) :
    
    # Use .copy instead of direct assign for safety 
    # (we don't want the pianoroll widget to mess with the real score)
    self.noteArray = noteArray.copy()


