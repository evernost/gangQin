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
  PIANO_ROLL object
  
  The PianoRoll class derives from the Widget class.

  It renders a typical vertical 'piano roll' view on the screen, aligned with
  the keyboard.
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
    #self.backgroundRGB = PIANOROLL_BACKGROUND_COLOR       # Background color for the piano roll
    #self.keyLineRGB = PIANOROLL_NOTE_LINE_COLOR           # Color of the lines separating each notes in the piano roll
    self.leftNoteOutlineRGB = (243, 35, 35)               # Border color for the notes in the piano roll
    self.rightNoteOutlineRGB = (35, 243, 118)
    self.leftNoteRGB = PIANOROLL_NOTE_COLOR_LEFT_HAND     # Color of a left hand note in piano roll
    self.rightNoteRGB = PIANOROLL_NOTE_COLOR_RIGHT_HAND   # Color of a right hand note in piano roll
    


  # ---------------------------------------------------------------------------
  # METHOD PianoRoll._renderKeyLines()                                [PRIVATE]
  # ---------------------------------------------------------------------------
  def _renderKeyLines(self) :
    """
    Draws the thin lines separating each key on the virtual keyboard.
    """

    # Some shortcuts
    x0 = self.x
    wnw = KEYBOARD_WHITE_NOTE_WIDTH
    bnw = KEYBOARD_BLACK_NOTE_WIDTH

    self.xLines = [
      x0,                     # begin(A0)
      x0+(1*wnw)-(bnw//3),    # begin(Bb0)
      x0+(1*wnw)+(2*bnw//3),  # begin(B0)
    ]
    x0 = x0+(2*wnw)           # end(B0) = begin(C0)
    
    for octave in range(7) :
      self.xLines += [
        x0,
        x0+(1*wnw)-(2*bnw//3),
        x0+(1*wnw)+(bnw//3),
        x0+(2*wnw)-(bnw//3),
        x0+(2*wnw)+(2*bnw//3),
        x0+(3*wnw),
        x0+(4*wnw)-(2*bnw//3),
        x0+(4*wnw)+(bnw//3),
        x0+(5*wnw)-(bnw//2),
        x0+(5*wnw)+(bnw//2),
        x0+(6*wnw)-(bnw//3),
        x0+(6*wnw)+(2*bnw//3)
      ]
      x0 += 7*wnw

    self.xLines += [
      x0,
      x0+(1*wnw)
    ]

    # Draw the background rectangle
    backRect = [
      (self.xLines[0], self.yBottom),
      (self.xLines[-1], self.yBottom),
      (self.xLines[-1], self.yTop),
      (self.xLines[0], self.yTop)
    ]

    # TODO: make the rectangle transparent    
    pygame.draw.polygon(self.top.screen, PIANOROLL_BACKGROUND_COLOR, backRect)


    # # Create a transparent surface
    # transparentSurface = pygame.Surface((400, 400), pygame.SRCALPHA)

    # # Draw the polygon onto the transparent surface (red with 50% transparency)
    # pygame.draw.polygon(transparentSurface, (255, 0, 0, 128), [(100, 100), (300, 100), (200, 300)])


    # while running:
    #     screen.fill((255, 255, 255))  # Clear screen to white
    #     screen.blit(transparentSurface, (0, 0))  # Blit the polygon with transparency
    #     pygame.display.flip()
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             running = False
    #     clock.tick(60)

    # Draw the lines
    for x in self.xLines :
      pygame.draw.line(self.top.screen, PIANOROLL_NOTE_LINE_COLOR, (x, self.yTop), (x, self.yBottom), 1)

    # Close the rectangle
    pygame.draw.line(self.top.screen, PIANOROLL_NOTE_LINE_COLOR, (self.xLines[0], self.yTop), (self.xLines[-1], self.yTop), 1)



  # ---------------------------------------------------------------------------
  # METHOD PianoRoll._renderNotes()                                   [PRIVATE]
  # ---------------------------------------------------------------------------
  def _renderNotes(self) :
    """
    Renders the rectangle symbols for each note.
    """
    
    # Get the current timecode
    startTimecode = self.top.widgets[WIDGET_ID_SCORE].getTimecode()

    # List the notes that intersect the current window
    notesInWindow = []

    # Draw the notes
    # NOTE: some processing could be avoided here since the notes are sorted by startTime
    # Once the notes start way after the end of the window, why bother exploring the rest?
    # for (staffIndex, _) in enumerate(self.noteArray) :
    #   for pitch in MIDI_CODE_GRAND_PIANO_RANGE :
    #     for note in self.noteArray[staffIndex][pitch] :
          
    #       # Shortcuts
    #       a = startTimecode; b = startTimecode + self.viewSpan
    #       c = note.startTime; d = note.stopTime
        
    #       # Does the note span intersect the current view window?
    #       if (((c >= a) and (c < b)) or ((d >= a) and (d < b)) or ((c <= a) and (d >= b))) :
    #         notesInWindow.append(note)
    for noteObj in self.top.widgets[WIDGET_ID_SCORE].noteList :
      pass


    # Sort the notes to display them in a given order.
    # Longest notes are displayed first
    notesInWindow.sort(key = lambda x : -(x.stopTime-x.startTime))

    # Draw the notes
    for note in notesInWindow :

      # Shortcuts
      a = startTimecode; b = startTimecode + self.viewSpan
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
      if (note.hand == NOTE_LEFT_HAND) :
        color = self.leftNoteOutlineRGB
      
      if (note.hand == NOTE_RIGHT_HAND) :
        color = self.rightNoteOutlineRGB

      (rectColor, rectOutlineColor, pianoRollColor) = note.getNoteColor()
      pygame.draw.line(self.top.screen, color, sq[0], sq[1], 3)
      pygame.draw.line(self.top.screen, color, sq[1], sq[2], 3)
      pygame.draw.line(self.top.screen, color, sq[2], sq[3], 3)
      pygame.draw.line(self.top.screen, color, sq[3], sq[0], 3)
      
      pygame.draw.polygon(self.top.screen, rectColor, sq)



  # ---------------------------------------------------------------------------
  # METHOD PianoRoll.render()
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Draws the pianoroll on screen.
    This function is called every time the app renders a new frame.
    """

    self._renderKeyLines()
    self._renderNotes()



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] There are no unit tests available for 'pianoRoll.py'")

