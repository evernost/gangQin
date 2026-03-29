# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : sequencer
# File name     : sequencer.py
# File type     : Python script (Python 3)
# Purpose       : controls the current location displayed in the score
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 14 April 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project libraries
from src.commons import *
import src.widgets.widget as widget
import arbiter

# Standard libraries
import datetime
import pygame       # For keyboard/mouse interactions



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Sequencer(widget.Widget) :

  """
  SEQUENCER object

  The Sequencer controls the position in the Score.
  
  It can be determined by:
  - the user (scrolling)
  - the MIDI keyboard inputs (if approved by the Arbiter)
  - the inner clock (for playback)
  - the 'note search' feature
  """

  def __init__(self, top) :
    
    # Call the Widget init method
    super().__init__(top, loc = WIDGET_LOC_UNDEFINED)

    self.name = "sequencer"

    # Internal attributes (not much yet)
    self.isAutoPlaying = False      # True when the sequencer plays the notes automatically



  # ---------------------------------------------------------------------------
  # METHOD Sequencer._onKeyEvent()                                    [PRIVATE]
  # ---------------------------------------------------------------------------
  def _onKeyEvent(self, key, type, modifier = "") :
    """
    Function is triggered by a keypress.
    """
    
    if (type == pygame.KEYDOWN) :
      
      # Simple keypresses (no modifiers)
      if (modifier == "") :
        # LEFT: jump backward (1 step)
        if (key == pygame.K_LEFT) :
          self.top.widgets[WIDGET_ID_SCORE].cursorStep(-1)

        # RIGHT: jump forward (1 step)
        elif (key == pygame.K_RIGHT) :
          self.top.widgets[WIDGET_ID_SCORE].cursorStep(1)
          self.top.widgets[WIDGET_ID_PLAYBACK].playNotesOnMidiOut()

        # HOME: jump to the beginning of the score
        elif (key == pygame.K_HOME) :
          self.top.widgets[WIDGET_ID_SCORE].cursorBegin()

        # END: jump to the end of the score
        elif (key == pygame.K_END) :
          self.top.widgets[WIDGET_ID_SCORE].cursorEnd()

        # DOWN: jump to the previous bookmark
        elif (key == pygame.K_DOWN) :
          self.top.widgets[WIDGET_ID_SCORE].cursorGotoNearestBookmark(direction = -1)

        # UP: jump to the next bookmark
        elif (key == pygame.K_UP) :
          self.top.widgets[WIDGET_ID_SCORE].cursorGotoNearestBookmark(direction = 1)

        elif (key == pygame.K_SPACE) :
          self.isAutoPlaying = not(self.isAutoPlaying)
          print("Autoplay")



      # Ctrl-modified keypress
      elif (modifier == "ctrl")  :

        # CTRL + LEFT: fast rewind (10 steps)
        if (key == pygame.K_LEFT) :
          self.top.widgets[WIDGET_ID_SCORE].cursorStep(-10)

        # CTRL + LEFT: fast forward (10 steps)
        elif (key == pygame.K_RIGHT) :
          self.top.widgets[WIDGET_ID_SCORE].cursorStep(10)



  # ---------------------------------------------------------------------------
  # METHOD: Widget._onMouseEvent()                                    [PRIVATE]
  # ---------------------------------------------------------------------------
  def _onMouseEvent(self, event) :
    """
    Function is triggered by a keypress.
    """
    
    # Read eventual keyboard modifiers
    keys = pygame.key.get_pressed()
    ctrl = keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]

    if (event.type == pygame.MOUSEWHEEL) :
      if (event.y > 0) :
        if ctrl :
          self.top.widgets[WIDGET_ID_SCORE].cursorStep(10)
        else :
          self.top.widgets[WIDGET_ID_SCORE].cursorStep(1)

      elif (event.y < 0) :
        if ctrl :
          self.top.widgets[WIDGET_ID_SCORE].cursorStep(-10)
        else :
          self.top.widgets[WIDGET_ID_SCORE].cursorStep(-1)



  # ---------------------------------------------------------------------------
  # METHOD: Sequencer.onExternalMidiEvent()
  # ---------------------------------------------------------------------------
  def onExternalMidiEvent(self, midiMessage) -> None :
    """
    Updates the Sequencer machinery in case of an external MIDI input.
    """

    (decision, step) = self.top.widgets[WIDGET_ID_ARBITER].eval()

    if (arbiter.arbiterStatus.VALID_INPUT in decision) :
      if (step == 1) :
        self.top.widgets[WIDGET_ID_SCORE].cursorNext()
      else :
        # TODO: be careful, this could cause issues in loop practice
        self.top.widgets[WIDGET_ID_SCORE].cursorStep(step)
      self.top.widgets[WIDGET_ID_STATS].logCorrectNote()

    elif (arbiter.arbiterStatus.EXCESS_NOTE in decision) :
      self.top.widgets[WIDGET_ID_STATS].logWrongNote()
      




# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'sequencer.py'")

