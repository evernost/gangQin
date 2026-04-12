# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : Playback (inherited from Widget)
# File name     : playback.py
# File type     : Python script (Python 3)
# Purpose       : handles the 
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 29 March 2026
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project libraries
from src.commons import *
import src.widgets.widget as widget
import src.text as text

# Standard libraries
import mido
import pygame



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Playback(widget.Widget) :

  """
  PLAYBACK object
  
  Description is TODO.
  """

  def __init__(self, top) :
    
    # Call the Widget init method
    super().__init__(top, loc = WIDGET_LOC_UNDEFINED)
   
    self.name = "playback"

    self.enable = False
    self._midiOutActiveNotes = []   # pitches currently held on MIDI out
    


  # ---------------------------------------------------------------------------
  # METHOD Playback.play()                                            [PRIVATE]
  # ---------------------------------------------------------------------------
  def play(self) -> None :
    """
    Updates MIDI out to reflect the notes at the current cursor.

    - Notes that just appeared  -> note_on
    - Notes that are sustained  -> keep sounding (no action)
    - Notes that disappeared    -> note_off
    """

    if not(self.enable) :
      return

    if (self.top.midiOutPort is None) :
      return


    # Close everything before playing the new cursor
    for pitch in self._midiOutActiveNotes :
      #print(f"[DEBUG] Closing pitch {pitch}")
      self.top._onMidiOutputCallback(mido.Message("note_off", note = pitch, velocity = 0))
    self._midiOutActiveNotes = []

    # Request the current notes
    notes = self.top.widgets[WIDGET_ID_SCORE].getTeacherNotes()

    for N in notes :
      if not(N.sustained) :
        
        velocity = N.velocity if (N.velocity > 0) else 80

        #print(f"[DEBUG] New pitch: {N.pitch}")
        self.top._onMidiOutputCallback(mido.Message("note_on",  note = N.pitch, velocity = velocity))
        self._midiOutActiveNotes.append(N.pitch)

        # if (N.pitch in self._midiOutActiveNotes) :
        #   print(f"[DEBUG] Closing pitch {N.pitch} before replay")
        #   #self.top._onMidiOutputCallback(mido.Message("note_off", note = N.pitch, velocity = 0))
        #   self.top._onMidiOutputCallback(mido.Message("note_on",  note = N.pitch, velocity = velocity))

        # else :
        #   print(f"[DEBUG] New pitch: {N.pitch}")
        #   self.top._onMidiOutputCallback(mido.Message("note_on",  note = N.pitch, velocity = velocity))
        #   self._midiOutActiveNotes.append(N.pitch)




    # currentlyHeld = set(self._midiOutActiveNotes)
    # newPitches    = set(newActive.keys())

    # # Stop notes that are no longer in the score at this cursor
    # for pitch in currentlyHeld - newPitches :
    #   self.top._onMidiOutputCallback(mido.Message("note_off", note = pitch, velocity = 0))

    # # Start notes that have just appeared (skip sustained ones already sounding)
    # for pitch in newPitches - currentlyHeld :
    #   n = newActive[pitch]
    #   velocity = n.velocity if (n.velocity > 0) else 80
    #   self.top._onMidiOutputCallback(mido.Message("note_on", note = pitch, velocity = velocity))

    # self._midiOutActiveNotes = list(newPitches)



  # ---------------------------------------------------------------------------
  # METHOD Playback.close()                                           [PRIVATE]
  # ---------------------------------------------------------------------------
  def close(self) -> None :
    """
    Terminates all notes on the MIDI output interface properly.
    """
    
    if (self.top.midiOutPort is None) :
      return
    
    for pitch in self._midiOutActiveNotes :
      self.top.midiOutPort.send(mido.Message("note_off", note = pitch, velocity = 0))



  # ---------------------------------------------------------------------------
  # METHOD Playback._onKeyEvent()                                     [PRIVATE]
  # ---------------------------------------------------------------------------
  def _onKeyEvent(self, key, type, modifier = "") :
    """
    Function is triggered by a keypress.
    """
    
    if (type == pygame.KEYDOWN) :
      if (modifier == "") :
        if (key == pygame.K_p) :
          if self.enable :
            print("[INFO] MIDI out playback disabled")
          else :
            print("[INFO] MIDI out playback enabled")
          self.enable = not(self.enable)



  # ---------------------------------------------------------------------------
  # METHOD: Playback.render()
  # ---------------------------------------------------------------------------
  def render(self) -> None :
    """
    Renders the widget on screen.
    This function is called at every frame of the top level application.
    """

    if self.enable :
      text.render(self.top.screen, "P", (200, 470), 2, GUI_TEXT_COLOR)



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :  
  print("[INFO] There are no unit tests available for 'playback.py'")

