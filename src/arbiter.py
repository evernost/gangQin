# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : arbiter
# File name     : arbiter.py
# File type     : Python script (Python 3)
# Purpose       : 
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : July 26th, 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This lib is not intended to be called as a main.")



# =============================================================================
# Constants pool
# =============================================================================
ARBITER_MODE_EXACT = 0                # Deprecated
ARBITER_MODE_EXACT_WITH_SUSTAIN = 1   # Deprecated
ARBITER_MODE_PERMISSIVE = 2

ARBITER_MSG_CURSOR_NEXT = 0
ARBITER_MSG_RESET_COMBO = 1



class Arbiter :

  """
  DESCRIPTION
  
  Provides all the machinery to help determine if the keyboard inputs
  are valid and whether it allows to progress in the song.

  It returns the decision, that can be used then:
  - to step to the next cursor
  - update the combo counter
  - play a "fail" sound 

  Criteria to allow moving forward in the score are the following:
  - "exact": won't go further until the expected notes only are pressed, nothing else.
  - "exactWithSustain": same as "exact", but tolerates the last valid notes to be sustained
  - "permissive": anything else played alongside the expected notes is ignored
  


  MIDI update:
  - midiCurr        : state of all the notes on the MIDI keyboard
  - midiSustained   : '1' for all notes that were correct in the score, but have been 
                      sustained since then.
  - midiSuperfluous : TODO
  - midiAssociatedID: TODO



  NOTES
  Modes "exact" and "exact with sustain" came up with the very first releases 
  of gangQin, and have been refined since then because of several flaws.
  They will be removed in future releases.

  """
  
  
  
  # ---------------------------------------------------------------------------
  # METHOD: Arbiter.__init__ (constructor)
  # ---------------------------------------------------------------------------
  def __init__(self, comparisonMode) :
    
    self.status = False  
    self.comparisonMode = comparisonMode
    
    self.midiCurr         = [0 for _ in range(128)]
    self.midiSustained    = [0 for _ in range(128)]
    self.midiSuperfluous  = [0 for _ in range(128)]
    self.midiAssociatedID = [-1 for _ in range(128)]

    self.arbiterSuspendReq = False
    self.queryNotesPitch = []



  # ---------------------------------------------------------------------------
  # METHOD: Arbiter.updateMidiState(midiMessage)
  # ---------------------------------------------------------------------------
  def updateMidiState(self, midiMessage) :
    """
    Updates the internal state with the incoming MIDI message.
    """
    
    if (midiMessage.type == 'note_on') :
      self.midiCurr[midiMessage.note] = 1

    elif (midiMessage.type == 'note_off') :
      self.midiCurr[midiMessage.note] = 0
      self.midiSustained[midiMessage.note] = 0
      self.midiSuperfluous[midiMessage.note] = 0
      self.midiAssociatedID[midiMessage.note] = -1


    
  # ---------------------------------------------------------------------------
  # METHOD: Arbiter.eval(teacherNotes)
  # ---------------------------------------------------------------------------
  def eval(self, teacherNotes) :
    """
    Evaluates the decision based on the current input with respect to the 
    expected notes.

    <teacherNotes> is a list of all the expected notes.
    <midiCurr> is the current MIDI input in format TODO

    """

    # Reformat the teacher notes
    teacherNotesAsMidiArray = [0 for _ in range(128)]
    for noteObj in teacherNotes :
      teacherNotesAsMidiArray[noteObj.pitch] = 1
    
    msgQueue = []

    # STRATEGY: EXACT MODE (deprecated)
    # if (self.comparisonMode == "exact") :
    #   if (teacherNotesMidi == midiCurr) :
    #     msgQueue.append(ARBITER_MSG_CURSOR_NEXT)
    #     return ARBITER_DECISION_OK

    # STRATEGY: EXACT WITH SUSTAIN (deprecated)
    # if (self.comparisonMode == "exactWithSustain") :
    #   allowProgress = True
    #   for pitch in GRAND_PIANO_MIDI_RANGE :

    #     # Case 1: the right note is pressed, but is actually an "old" key press (sustained note)
    #     if ((teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 1) and (self.midiSustained[pitch] == 1)) :
    #       allowProgress = False

    #     # Case 2: a note is missing
    #     if ((teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 0) and (self.midiSustained[pitch] == 0)) :
    #       allowProgress = False
        
    #     # Case 3: a wrong note is pressed 
    #     if ((teacherNotesMidi[pitch] == 0) and (midiCurr[pitch] == 1) and (self.midiSustained[pitch] == 0)) :
    #       allowProgress = False

    #   # Case 4: progress disabled because the "note finding" feature is still active
    #   if (userScore.arbiterSuspendReq) :
    #     allDown = True
    #     for x in userScore.arbiterPitchListHold :
    #       if (self.midiCurr[x] == 1) :
    #         allDown = False

    #     if allDown :
    #       userScore.arbiterSuspendReq = False
    #     else :
    #       allowProgress = False

    #   if allowProgress :
    #     self.status = ARBITER_DECISION_OK
        
    #     # Take snapshot
    #     for pitch in range(128) :
    #       if ((teacherNotesMidi[pitch] == 1) and (self.midiCurr[pitch] == 1) and (self.midiSustained[pitch] == 0)) :
    #         self.midiSustained[pitch] = 1

    # STRATEGY: PERMISSIVE
    # Progress as long as the expected notes are pressed. 
    # The rest is ignored, but flagged as 'superfluous'.
    # 'Superfluous' notes need to be released and pressed again to be accepted later on.
    if (self.comparisonMode == "permissive") :
      allowProgress = True
      for pitch in GRAND_PIANO_MIDI_RANGE :

        # Case 1: a required notes is missing.
        if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 0) and (self.midiSuperfluous[pitch] == 0)) :
          allowProgress = False

        # Case 2: a required note is here, but it was hit before (it wasn't even expected)
        # and has been maintained since then. 
        # Therefore, it does not count.
        if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 1) and (self.midiSuperfluous[pitch] == 1)) :
          allowProgress = False

        # Case 3: a required note is here, but it was hit before and has been sustained since then.
        # Meanwhile, the score requires this note to be played again.
        # This case is detected by comparing the ID of the notes.
        if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 1) and (self.midiSustained[pitch] == 1)) :
          
          # Read the ID of the current note
          authorisedIDs = [x.id for x in teacherNotes if (x.pitch == pitch)]        
          
          # The expected ID do not match with the ID of the sustained note.:
          # The note being played on the keyboard right now is a previous valid note being sustained.
          # It cannot be used to trigger a new note of the same pitch.
          if not(self.midiAssociatedID[pitch] in authorisedIDs) :
            allowProgress = False
          
        # Case 4: a wrong note is pressed.
        # Since it is permissive, it does not block the progress.
        # But it resets the combo counter and plays a notification.
        if ((teacherNotesAsMidiArray[pitch] == 0) and (self.midiCurr[pitch] == 1) and (self.midiSustained[pitch] == 0)) :
          msgQueue.append(ARBITER_MSG_RESET_COMBO)
          
      # Case 5: progress is on hold because the "note finding" feature is active.
      # The current notes pressed are 'query' notes and all of them 
      # must be released before reenabling the arbiter.
      if (self.arbiterSuspendReq) :
        allDown = True
        for x in self.queryNotesPitch :
          if (self.midiCurr[x] == 1) :
            allDown = False

        if allDown :
          self.arbiterSuspendReq = False
        else :
          allowProgress = False



      # CONCLUSION
      if allowProgress :
        msgQueue.append(ARBITER_MSG_CURSOR_NEXT)
        
        # Update note status
        for pitch in GRAND_PIANO_MIDI_RANGE :
          
          # Is it a superfluous note?
          if ((teacherNotesAsMidiArray[pitch] == 0) and (self.midiCurr[pitch] == 1)) :
            self.midiSuperfluous[pitch] = 1

          # A valid note is now flagged as 'sustained'
          # The ID of the associated teacher note is registered (this keypress cannot validate another note 
          # of the same pitch)
          if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 1)) :
            self.midiSustained[pitch] = 1
            
            # Get the ID of the correct note
            # TODO: is it really always the first one that needs to be taken?
            q = [x for x in teacherNotes if (x.pitch == pitch)]
            self.midiAssociatedID[pitch] = q[0].id


    return msgQueue
  
