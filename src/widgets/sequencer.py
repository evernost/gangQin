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

    # Internal attributes
    # ...



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



#  elif (event.type == pygame.MOUSEBUTTONDOWN) :
        
#         pianoRollWidget.mouseEvent(event)

#         # Left click
#         if (event.button == MOUSE_LEFT_CLICK) :
#           clickMsg = True
#           clickCoord = pygame.mouse.get_pos()
        
#         # Scroll up
#         if (event.button == MOUSE_SCROLL_UP) :
          
#           # Find feature: go to the next cursor whose active notes match 
#           # the current notes being pressed.
#           # Note : use a copy of the MIDI notes list to prevent the 
#           #        MIDI callback to mess with the function.
#           if (pianoArbiter.hasActiveMidiInput()) :
#             print("[INFO] Backward search requested...")
#             (suspendReq, pitchListHold) = userScore.search(pianoArbiter.midiCurr.copy())
#             if suspendReq :
#               pianoArbiter.suspendReq(pitchListHold)

#           elif ctrlKey :
#             userScore.cursorStep(10)
#           else :
#             userScore.cursorStep(1)

#         # Scroll down
#         if (event.button == MOUSE_SCROLL_DOWN) :
          
#           # Find feature



  # ---------------------------------------------------------------------------
  # METHOD: Sequencer.onExternalMidiEvent()
  # ---------------------------------------------------------------------------
  def onExternalMidiEvent(self, midiMessage) :
    """
    Updates the Sequencer machinery in case of an external MIDI input.
    """

    # TODO 
    # In "normal" gameplay mode:
    # - call the arbiter
    # - ask his opinion about the user MIDI input
    # In "automatic" gameplay mode:
    # MIDI inputs are ignored.

    decision = self.top.widgets[WIDGET_ID_ARBITER].eval()

    if (decision == arbiter.msg.VALID_INPUT) :
      self.top.widgets[WIDGET_ID_SCORE].cursorStep(1)



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'sequencer.py'")

