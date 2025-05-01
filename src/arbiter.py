# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : arbiter
# File name     : arbiter.py
# File type     : Python script (Python 3)
# Purpose       : decision machinery to approve or reject the keyboard input.
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Friday, 26 July 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *



# =============================================================================
# Constants pool
# =============================================================================
# Messages returned by the arbiter
MSG_CURSOR_NEXT = 0
MSG_RESET_COMBO = 1



# =============================================================================
# Main code
# =============================================================================
class Arbiter :

  """
  Provides all the machinery that determines if the keyboard inputs
  are valid and whether it allows to progress in the song.

  It returns the decision, that can be used then:
  - to step to the next cursor
  - update the combo counter ("how many good notes in a row")
  - play a "fail" sound 

  Criteria to allow moving forward in the score are the following:
  - "exact": won't go further until the expected notes only are pressed, nothing else.
  - "exactWithSustain": same as "exact", but tolerates the last valid notes to be sustained
  - "permissive": anything else played alongside the expected notes is ignored
  Only the "permissive" mode is used, the others are here for "historical" reasons.

  MIDI update:
  - midiCurr        : state of all the notes on the MIDI keyboard
  - midiSustained   : '1' for all notes that were correct in the score, but have been 
                      sustained since then.
  - midiSuperfluous : TODO
  - midiAssociatedID: TODO


  Mode of operation
  - declare what happened on the MIDI interface using 'updateMidiState'
  - indicate the expected notes using 'eval'


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

    self.suspended = False
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
  # METHOD: Arbiter.hasActiveMidiInput()
  # ---------------------------------------------------------------------------
  def hasActiveMidiInput(self) :
    """
    Returns True if notes are currently being played on the keyboard.
    """
    
    return (max(self.midiCurr) == 1)



  # ---------------------------------------------------------------------------
  # METHOD: Arbiter.suspendReq(pitchList)
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
  # METHOD: Arbiter.eval(teacherNotes)
  # ---------------------------------------------------------------------------
  def eval(self, teacherNotes) :
    """
    Compares the notes currently played on the keyboard ('self.midiCurr') with 
    the notes expected ('teacherNotes') and returns the decision in the 
    message queue 'msgQueue'.
    Decision can either be
    - MSG_CURSOR_NEXT: valid input
    - MSG_RESET_COMBO: invalid input
    """

    # Reformat the teacher notes, keep the 'new' notes only
    # (not the sustained ones, not the notes of the inactive hand)
    teacherNotesAsMidiArray = [0 for _ in range(128)]
    for noteObj in teacherNotes :
      if ((noteObj.sustained == False) and (noteObj.inactive == False)):
        teacherNotesAsMidiArray[noteObj.pitch] = 1
    
    msgQueue = []

    # STRATEGY: PERMISSIVE
    # Progress as long as the expected notes are pressed. 
    # The rest is ignored, but flagged as 'superfluous'.
    # 'Superfluous' notes need to be released and pressed again to be accepted later on.
    if (self.comparisonMode == "permissive") :
      allowProgress = True
      for pitch in MIDI_CODE_GRAND_PIANO_RANGE :

        # Case 1: a required note is missing.
        if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 0) and (self.midiSuperfluous[pitch] == 0)) :
          allowProgress = False

        # Case 2: a required note is here, but it was hit before (it wasn't even expected)
        # and has been maintained since then. 
        # Therefore, it does not count.
        if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 1) and (self.midiSuperfluous[pitch] == 1)) :
          allowProgress = False

        # Case 3: a required note is here, but it was hit before and has been sustained since then.
        # Meanwhile, the score requires this note to be played again.
        # This case is detected as follows:
        # Every time a note is valid, we bind its pitch to the unique ID of the note in the score, and
        # the binding lasts for as long as the note is sustained on the keyboard.
        # Later on, the score requires this note. The note is pressed, but a binding exists: the note is rejected.
        if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 1) and (self.midiSustained[pitch] == 1)) :
          
          # Read the ID of the current note
          expectedIDs = [x.id for x in teacherNotes if ((x.pitch == pitch) and (x.sustained == False) and (x.inactive == False))]
          
          # The expected ID does not match with the ID of the sustained note.:
          # The note being played on the keyboard right now is a previous valid note being sustained.
          # It cannot be used to trigger a new note of the same pitch.
          if not(self.midiAssociatedID[pitch] in expectedIDs) :
            allowProgress = False
          
        # Case 4: a wrong note is pressed.
        # Since it is permissive, it does not block the progress.
        # But it resets the combo counter and plays a notification.
        if ((teacherNotesAsMidiArray[pitch] == 0) and (self.midiCurr[pitch] == 1) and (self.midiSustained[pitch] == 0)) :
          msgQueue.append(MSG_RESET_COMBO)
          
      # Case 5: progress is on hold because the "note finding" feature is active.
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
        msgQueue.append(MSG_CURSOR_NEXT)
        
        # Update note status
        for pitch in MIDI_CODE_GRAND_PIANO_RANGE :
          
          # Flag the notes played in 'excess'.
          if ((teacherNotesAsMidiArray[pitch] == 0) and (self.midiCurr[pitch] == 1)) :
            self.midiSuperfluous[pitch] = 1

          # Flag the sustained notes.
          # Any note that was valid becomes flagged as 'sustained' as long as it's held.
          # The ID of the associated teacher note is stored in an array,
          # so that this keypress cannot validate another note of the same pitch.
          if ((teacherNotesAsMidiArray[pitch] == 1) and (self.midiCurr[pitch] == 1)) :
            self.midiSustained[pitch] = 1
            
            # Get the ID of the correct note
            # TODO: is it really always the first one that needs to be taken?
            q = [x for x in teacherNotes if (x.pitch == pitch)]
            self.midiAssociatedID[pitch] = q[0].id


    return msgQueue



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'arbiter.py'")

