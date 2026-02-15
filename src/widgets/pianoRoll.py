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
import src.note as note

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

    self.xLines = []

    self.activePitches = []

    # Color scheme
    self.leftNoteOutlineRGB   = PIANOROLL_NOTE_BORDER_COLOR_LEFT
    self.rightNoteOutlineRGB  = PIANOROLL_NOTE_BORDER_COLOR_RIGHT
    


  # ---------------------------------------------------------------------------
  # METHOD PianoRoll.render()
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Draws the pianoroll on screen.
    This function is called every time the app renders a new frame.
    """

    # Disable rendering if the staffscope has something to show
    if (WIDGET_ID_STAFFSCOPE in self.top.widgets) :
      if self.top.widgets[WIDGET_ID_STAFFSCOPE].isViewEmpty() :
        self._renderKeyLines()
        self._renderNotes()

      else :
        pass

    else :
      self._renderKeyLines()
      self._renderNotes()



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
    tmpSurface = pygame.Surface((GUI_SCREEN_WIDTH, GUI_SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(tmpSurface, (*PIANOROLL_BACKGROUND_COLOR, PIANOROLL_TRANSPARENCY), backRect)
    self.top.screen.blit(tmpSurface, (0, 0))

    # Draw the separation lines
    for x in self.xLines :
      pygame.draw.line(self.top.screen, PIANOROLL_NOTE_LINE_SEP_COLOR, (x, self.yTop), (x, self.yBottom), 1)
    pygame.draw.line(self.top.screen, PIANOROLL_NOTE_LINE_SEP_COLOR, (self.xLines[0], self.yTop), (self.xLines[-1], self.yTop), 1)    # Close the rectangle

    # Show the note played on keyboard
    for pitch in self.activePitches :
      rectBottom  = self.yBottom
      rectTop     = self.yTop
      
      # TODO: remove the magic constants
      sq = [
        (self.xLines[pitch-21]+2, rectBottom),
        (self.xLines[pitch-21]+2, rectTop),
        (self.xLines[pitch+1-21]-2, rectTop),
        (self.xLines[pitch+1-21]-2, rectBottom)
      ]
      
      # Draw the outline
      # color = PIANOROLL_NOTE_BORDER_COLOR_LEFT
      # pygame.draw.line(self.top.screen, color, sq[0], sq[1], 3)
      # pygame.draw.line(self.top.screen, color, sq[1], sq[2], 3)
      # pygame.draw.line(self.top.screen, color, sq[2], sq[3], 3)
      # pygame.draw.line(self.top.screen, color, sq[3], sq[0], 3)
      
      # Draw the rectangle
      # pygame.draw.polygon(self.top.screen, (165, 250, 200), sq)

      tmpSurface = pygame.Surface((GUI_SCREEN_WIDTH, GUI_SCREEN_HEIGHT), pygame.SRCALPHA)
      pygame.draw.polygon(tmpSurface, (165, 250, 200, PIANOROLL_TRANSPARENCY), sq)
      self.top.screen.blit(tmpSurface, (0, 0))



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
      if (N.hand == note.hand_T.LEFT)   : color = PIANOROLL_NOTE_BORDER_COLOR_LEFT
      if (N.hand == note.hand_T.RIGHT)  : color = PIANOROLL_NOTE_BORDER_COLOR_RIGHT
      pygame.draw.line(self.top.screen, color, sq[0], sq[1], 3)
      pygame.draw.line(self.top.screen, color, sq[1], sq[2], 3)
      pygame.draw.line(self.top.screen, color, sq[2], sq[3], 3)
      pygame.draw.line(self.top.screen, color, sq[3], sq[0], 3)
      
      # Draw the rectangle
      (rectColor, _, _) = N.getNoteColor()
      pygame.draw.polygon(self.top.screen, rectColor, sq)



  # ---------------------------------------------------------------------------
  # METHOD: PianoRoll.onExternalMidiEvent()
  # ---------------------------------------------------------------------------
  def onExternalMidiEvent(self, midiMessage) :
    """
    Updates the list of active MIDI notes coming from the keyboard so that 
    they can be displayed at rendering.
    """

    if (midiMessage.type == "note_on") :
      self.activePitches.append(midiMessage.note)
      
    elif (midiMessage.type == "note_off") :
      self.activePitches = [pitch for pitch in self.activePitches if (pitch != midiMessage.note)]



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :

  print("[INFO] There are no unit tests available for 'pianoRoll.py'")

