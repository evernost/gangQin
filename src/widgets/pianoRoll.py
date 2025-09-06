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
# EXTERNALS
# =============================================================================
# Project specific constants
from src.commons import *

import src.widgets.widget as widget

import pygame



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class PianoRoll(widget.Widget) :

  """
  PIANOROLL object
  
  The PianoRoll class derives from the Widget class.

  It renders a typical vertical 'piano roll' view on the screen, aligned with
  the keyboard.
  """

  def __init__(self, top, loc) :
    
    # Call the Widget init method
    super().__init__(top, loc)
  
    self.name = "pianoroll"

    # Widget location
    self.x = loc[0]
    self.yTop = loc[1]
    self.yBottom = 300-2

    # Defines the amount of notes shown in the piano roll view
    # Units are in timecodes. Use "avgNoteDuration" to use it conveniently
    self.viewSpan = 1000
    
    # Color scheme
    self.leftNoteOutlineRGB   = PIANOROLL_NOTE_BORDER_COLOR_LEFT
    self.rightNoteOutlineRGB  = PIANOROLL_NOTE_BORDER_COLOR_RIGHT
    
    

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
      pygame.draw.line(self.top.screen, PIANOROLL_NOTE_LINE_SEP_COLOR, (x, self.yTop), (x, self.yBottom), 1)

    # Close the rectangle
    pygame.draw.line(self.top.screen, PIANOROLL_NOTE_LINE_SEP_COLOR, (self.xLines[0], self.yTop), (self.xLines[-1], self.yTop), 1)



  # ---------------------------------------------------------------------------
  # METHOD PianoRoll._renderNotes()                                   [PRIVATE]
  # ---------------------------------------------------------------------------
  def _renderNotes(self) :
    """
    Renders the rectangle symbols for each note.
    """
    
    # Get the current timecode
    currTimecode = self.top.widgets[WIDGET_ID_SCORE].getTimecode()

    # List the notes that intersect the current window
    notesInWindow = []

    for N in self.top.widgets[WIDGET_ID_SCORE].noteList :
      
      # Shorcuts
      winStart  = currTimecode 
      winEnd    = currTimecode + self.viewSpan
      noteStart = N.startTime 
      noteEnd   = N.stopTime
        
      # Does the note span intersect the current view window?
      if (
        ((noteStart >= winStart)  and (noteStart < winEnd)) or    # The note starts in the window
        ((noteEnd >= winStart)    and (noteEnd < winEnd))   or    # The note ends in the window
        ((noteStart <= winStart)  and (noteEnd >= winEnd))        # The note starts before the window and ends after the window
      ) : notesInWindow.append(N)


    # Sort the notes to display them in a given order.
    # Longest notes are displayed first
    notesInWindow.sort(key = lambda N : -(N.stopTime-N.startTime))

    # Draw the notes
    for N in notesInWindow :

      # Shortcuts
      winStart  = currTimecode
      winEnd    = currTimecode + self.viewSpan
      noteStart = N.startTime
      noteEnd   = N.stopTime

      # Convert the size from time units to pixels
      rectBottom  = self.yTop - ((self.yBottom-self.yTop)*(noteStart-winEnd)/(winEnd-winStart))
      rectTop     = self.yTop - ((self.yBottom-self.yTop)*(noteEnd-winEnd)/(winEnd-winStart))
      
      # Limit the coordinates to the view size
      rectBottom = max([rectBottom, self.yTop])
      rectBottom = min([rectBottom, self.yBottom])
      rectTop = max([rectTop, self.yTop])
      rectTop = min([rectTop, self.yBottom])

      # TODO: remove the magic constants
      sq = [
        (self.xLines[N.pitch-21]+2, rectBottom),
        (self.xLines[N.pitch-21]+2, rectTop),
        (self.xLines[N.pitch+1-21]-2, rectTop),
        (self.xLines[N.pitch+1-21]-2, rectBottom)
      ]
      
      # Draw the outline
      # TODO: replace with a call to getNoteColor()
      if (N.hand == NOTE_LEFT_HAND)   : color = PIANOROLL_NOTE_BORDER_COLOR_LEFT
      if (N.hand == NOTE_RIGHT_HAND)  : color = PIANOROLL_NOTE_BORDER_COLOR_RIGHT
      pygame.draw.line(self.top.screen, color, sq[0], sq[1], 3)
      pygame.draw.line(self.top.screen, color, sq[1], sq[2], 3)
      pygame.draw.line(self.top.screen, color, sq[2], sq[3], 3)
      pygame.draw.line(self.top.screen, color, sq[3], sq[0], 3)
      
      # Draw the rectangle
      (rectColor, _, _) = N.getNoteColor()
      pygame.draw.polygon(self.top.screen, rectColor, sq)



  # ---------------------------------------------------------------------------
  # METHOD PianoRoll.render()
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Draws the pianoroll on screen.
    This function is called every time the app renders a new frame.
    """

    # Disable piano roll rendering if the staffscope has something available
    # to show
    if (WIDGET_ID_STAFFSCOPE in self.top.widgets) :
      if self.top.widgets[WIDGET_ID_STAFFSCOPE].isViewEmpty() :
        self._renderKeyLines()
        self._renderNotes()

      else :
        pass

    else :
      self._renderKeyLines()
      self._renderNotes()



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] There are no unit tests available for 'pianoRoll.py'")

