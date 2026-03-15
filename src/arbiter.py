# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : arbiter
# File name     : arbiter.py
# File type     : Python script (Python 3)
# Purpose       : decision machinery for the gangQin gameplay
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Friday, 26 July 2024
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
import enum     # For enumerated types in FSM
import pygame



# =============================================================================
# CONSTANTS
# =============================================================================

# NOTE: the following statuses can be combined to fully depict the state.
class arbiterStatus(enum.Enum) :
  NO_INPUT          = 0       # Nothing played by the user
  INCOMPLETE_INPUT  = 1       # Some notes in the score are missing 
  EXCESS_NOTE       = 2       # At least one note that is played is not expected in the score
  STALE_EXCESS_NOTE = 3       # At least one note has been held (but not requested in the score) yet the score expects it to be played again
  STALE_VALID_NOTE  = 4       # At least one note has been held since its last occurence in the score, yet the score expects it to be played again
  VALID_INPUT       = 5       # 

class arbiterDecision(enum.Enum) :
  WAITING_VALID_INPUT = 0
  PROGRESS_ALLOWED    = 1
  WRONG_INPUT         = 2



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Arbiter(widget.Widget) :

  """
  ARBITER object

  Class definition for the Arbiter widget.
  
  Provides all the machinery that determines if the keyboard inputs are valid 
  and whether they allows to progress in the song.

  It returns the decision, that can be used then:
  - to step to the next cursor
  - update the combo counter ("how many good notes in a row")
  - play a "fail" sound 

  MIDI update:
  - midiCurr        : state of all the notes on the MIDI keyboard
  - midiSustained   : '1' for all notes that were correct in the score, but have been 
                      sustained since then.
  - midiSuperfluous : TODO
  - midiAssociatedID: TODO


  Mode of operation
  - declare what happened on the MIDI interface using 'updateMidiState'
  - indicate the expected notes using 'eval'

  """
  
  def __init__(self, top) :
    
    # Call the Widget init method
    super().__init__(top, loc = WIDGET_LOC_UNDEFINED)

    self.name = "arbiter"

    self.status = False
    
    self.midiCurr         = [0 for _ in range(128)]
    self.midiSustained    = [0 for _ in range(128)]
    self.midiSuperfluous  = [0 for _ in range(128)]
    self.midiAssociatedID = [-1 for _ in range(128)]

    self.suspended = False
    self.queryNotesPitch = []



  # ---------------------------------------------------------------------------
  # METHOD: Arbiter.onExternalMidiEvent()
  # ---------------------------------------------------------------------------
  def onExternalMidiEvent(self, midiMessage) :
    """
    Updates the internal state with the incoming MIDI message.
    """
    
    if (midiMessage.type == "note_on") :
      self.midiCurr[midiMessage.note] = 1

    elif (midiMessage.type == "note_off") :
      self.midiCurr[midiMessage.note] = 0
      self.midiSustained[midiMessage.note] = 0
      self.midiSuperfluous[midiMessage.note] = 0
      self.midiAssociatedID[midiMessage.note] = -1

    else :
      pass



  # ---------------------------------------------------------------------------
  # METHOD: Arbiter.hasActiveMidiInput()
  # ---------------------------------------------------------------------------
  def hasActiveMidiInput(self) :
    """
    Returns True if notes are currently being played on the keyboard.
    """
    
    return (max(self.midiCurr) == 1)



  # ---------------------------------------------------------------------------
  # METHOD: Arbiter.suspendReq()
  # ---------------------------------------------------------------------------
  def suspendReq(self, queryNotesPitch) :
    """
    Turns on the "suspend" mode.
    "Suspend mode" is triggered for the search mode, i.e. when the user inputs
    some "query" notes on the keyboard and wants to know where these notes 
    appear in the score.
    """

    self.suspended = True
    self.queryNotesPitch = queryNotesPitch

    

  # ---------------------------------------------------------------------------
  # METHOD: Arbiter.eval()
  # ---------------------------------------------------------------------------
  def eval(self) -> arbiterStatus :
    """
    Compares the notes currently played on the keyboard ('self.midiCurr') with 
    the notes expected ('teacherNotes') and returns the decision.

    Decision is one of the following:
    - NO_INPUT          : waits for user input
    - INCOMPLETE_INPUT  : the user hasn't pressed all the expected notes 
    - WRONG_NOTE        : something is wrong in the user input
    - VALID_INPUT       : the user input is correct
    """

    # Read the teacher notes in the score
    teacherNotes = self.top.widgets[WIDGET_ID_SCORE].getTeacherNotes()

    # Reformat the teacher notes
    # Filter out the sustained notes
    teacherNotesAsMidiArray = [0 for _ in range(128)]
    for noteObj in teacherNotes :
      if ((noteObj.sustained == False) and (noteObj.inactive == False)):
        teacherNotesAsMidiArray[noteObj.pitch] = 1

    # STRATEGY: PERMISSIVE
    # Progress in the score is allowed as long as the expected notes are pressed.
    # All the other notes are ignored and flagged as 'superfluous'.
    # 'Superfluous' notes need to be released and pressed again to be accepted later on.
    allowProgress = True
    
    # Cumulate the different statuses
    ret = []
    
    for pitch in MIDI_CODE_GRAND_PIANO_RANGE :

      # Case 1: a note in the score is not played
      if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 0) and (self.midiSuperfluous[pitch] == 0)) :
        allowProgress = False
        if not(arbiterStatus.INCOMPLETE_INPUT in ret) : ret.append(arbiterStatus.INCOMPLETE_INPUT)

      # Case 2: a note in the score is played, but it was hit before (it wasn't expected then) and held since.
      # Therefore, the played note cannot count.
      if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 1) and (self.midiSuperfluous[pitch] == 1)) :
        allowProgress = False
        if not(arbiterStatus.STALE_EXCESS_NOTE in ret) : ret.append(arbiterStatus.STALE_EXCESS_NOTE)

      # Case 3: a note in the score is played, but it was hit before (as requested by the score) and held since.
      # Therefore, the played note cannot count.
      #
      # This case is detected as follows:
      # Every time a note is valid, we bind its pitch to the unique ID of the note in the score, and
      # the binding lasts for as long as the note is sustained on the keyboard.
      # Later on when the score requires this note, if binding exists then the played note is rejected.
      if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 1) and (self.midiSustained[pitch] == 1)) :
        
        # Read the ID of the current note
        expectedIDs = [x.id for x in teacherNotes if ((x.pitch == pitch) and (x.sustained == False) and (x.inactive == False))]
        
        # The expected ID doesn't match the ID of the sustained note:
        # The note being played on the keyboard right now is a previous valid note being sustained.
        # It cannot be used to trigger a new note of the same pitch.
        if not(self.midiAssociatedID[pitch] in expectedIDs) :
          allowProgress = False
          if not(arbiterStatus.STALE_VALID_NOTE in ret) : ret.append(arbiterStatus.STALE_VALID_NOTE)
        
      # Case 4: a wrong note is pressed.
      # Since it is permissive, it does not block the progress.
      # But it resets the combo counter and plays a notification.
      if ((teacherNotesAsMidiArray[pitch] == 0) and (self.midiCurr[pitch] == 1) and (self.midiSustained[pitch] == 0)) :
        if not(arbiterStatus.EXCESS_NOTE in ret) : ret.append(arbiterStatus.EXCESS_NOTE)
              
    # Case 6: progress is on hold because the "note finding" feature is active.
    # The current notes pressed are 'query' notes and all of them 
    # must be released before reenabling the arbiter.
    if (self.suspended) :
      allDown = True
      for x in self.queryNotesPitch :
        if (self.midiCurr[x] == 1) :
          allDown = False

      if allDown :
        self.suspended = False
      else :
        allowProgress = False



    # CONCLUSION
    if allowProgress :
      
      # Update note status
      for pitch in MIDI_CODE_GRAND_PIANO_RANGE :
        
        # Flag the notes played in 'excess'
        if ((teacherNotesAsMidiArray[pitch] == 0) and (self.midiCurr[pitch] == 1)) :
          self.midiSuperfluous[pitch] = 1

        # Flag the sustained notes
        # Any note that was valid becomes flagged as 'sustained' for as long as it's held.
        # The ID of the associated teacher note is stored in an array,
        # so that this keypress cannot validate another note of the same pitch later on.
        if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 1)) :
          self.midiSustained[pitch] = 1
          
          # Get the ID of the correct note
          # TODO: is it really always the first one that needs to be taken?
          q = [x for x in teacherNotes if (x.pitch == pitch)]
          self.midiAssociatedID[pitch] = q[0].id


      if not(arbiterStatus.VALID_INPUT in ret) : ret.append(arbiterStatus.VALID_INPUT)


    return ret



  # ---------------------------------------------------------------------------
  # METHOD Sequencer._onKeyEvent()                                  [INHERITED]
  # ---------------------------------------------------------------------------
  def _onKeyEvent(self, key, type, modifier = "") :
    """
    Function is triggered by a keypress.
    """
    
    if (type == pygame.KEYDOWN) :
      
      # Simple keypresses (no modifiers)
      if (modifier == "") :
        
        if (key == pygame.K_t) :
          self.top.midiTranspose += 1
          if (self.top.midiTranspose >= 0) :
            print(f"Transpose: +{self.top.midiTranspose}")
          else :
            print(f"Transpose: {self.top.midiTranspose}")

      # Ctrl-modified keypress
      elif (modifier == "ctrl")  :

        if (key == pygame.K_t) :
          self.top.midiTranspose -= 1
          if (self.top.midiTranspose >= 0) :
            print(f"Transpose: +{self.top.midiTranspose}")
          else :
            print(f"Transpose: {self.top.midiTranspose}")



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'arbiter.py'")

