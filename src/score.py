# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : score
# File name     : score.py
# Purpose       : provides an abstraction to a music score
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : October 5th, 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

import utils

import json   # for JSON database import/export
import os     # for file manipulation
import mido   # for MIDI file manipulation

import datetime



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This lib is not intended to be called as a main.")



# =============================================================================
# Constants pool
# =============================================================================
FSM_STATE_NORMAL = 0



# =============================================================================
# Main code 
# =============================================================================

class Score :

  def __init__(self) :
    
    # Info about the score
    self.nStaffs = 0
    self.avgNoteDuration = 0
    self.hasUnsavedChanges = False
    
    # Current location in the score
    self.cursor = 0
    self.pianoRoll = []

    self.noteOntimecodes = [[]]       # List of all <noteON> timecodes, one for each staff
    self.noteOntimecodesMerged = []   # Merge of <self.timecodes> on all staves
    self.cursorsLeft = []             # List of cursors values where a note is pressed on the left hand
    self.cursorsRight = []            # List of cursors values where a note is pressed on the right hand

    self.bookmarks = []               # List of all bookmarked timecodes (integers)
    
    self.activeHands = "LR"
    
    self.teacherNotes = []
    self.teacherNotesMidi = [0 for _ in range(128)]
    self.sustainedNotes = []

    # Key scales used throughout the song
    # List of tuples: (scaleObject, startTimeCode)
    self.keyList = []

    self.progressEnable = True
    self.arbiterSuspendReq = False
    self.arbiterPitchListHold = []

    # Combo!
    self.comboCount = 0
    self.comboDrop = False
    self.comboHighestSession = 0
    self.comboHighestAllTime = 0

    # Loop practice feature
    # TODO: allow to store several loops
    self.loopEnable = False
    self.loopStart = -1
    self.loopEnd = -1



  # ---------------------------------------------------------------------------
  # METHOD <getCursor>
  #
  # Return the current cursor position. 
  # ---------------------------------------------------------------------------
  def getCursor(self) :
    return self.cursor



  # ---------------------------------------------------------------------------
  # METHOD <getCurrentTimecode>
  #
  # TODO for the single hand practice
  # ---------------------------------------------------------------------------
  def getCurrentTimecode(self) :
    return self.noteOntimecodesMerged[self.cursor]



  
  def setTimecodes(self, timecodes) :
    self.noteOntimecodes = timecodes

    # Update <cursor> too as it might not be valid anymore
    # ...


  # ---------------------------------------------------------------------------
  # METHOD <cursorStep>
  #
  # Increase / decrease the cursor value of a given step (positive or negative)
  # Notes: 
  # - the cursor jumps regardless of the loop mode.
  #   Use <cursorNext> to take the loop info into account and wrap accordingly
  # - the cursor moves depending on the current hand practice mode. 
  #   So the cursor might jump non linearly in single hand mode.
  # ---------------------------------------------------------------------------
  def cursorStep(self, delta) :
  
    if (delta > 0) :

      if (self.activeHands == ACTIVE_HANDS_BOTH) :
        if ((self.cursor + delta) <= (len(self.noteOntimecodesMerged)-1)) :
          self.cursor += delta
          # print(f"[INFO] Cursor: {self.cursor}")

      if (self.activeHands == ACTIVE_HANDS_LEFT) :
        try :
          index = self.cursorsLeft.index(self.cursor)
        except :
          print("[DEBUG] The current cursor is not aligned to browse the left hand.")
          
        if ((index + delta) <= (len(self.cursorsLeft)-1)) :
          self.cursor = self.cursorsLeft[index + delta]
          # print(f"[INFO] Cursor: {self.cursor}")

      if (self.activeHands == ACTIVE_HANDS_RIGHT) :
        try :
          index = self.cursorsRight.index(self.cursor)
        except :
          print("[DEBUG] The current cursor is not aligned to browse the right hand.")
          
        if ((index + delta) <= (len(self.cursorsRight)-1)) :
          self.cursor = self.cursorsRight[index + delta]
          # print(f"[INFO] Cursor: {self.cursor}")

    else :

      if (self.activeHands == ACTIVE_HANDS_BOTH) :
        if ((self.cursor + delta) >= 0) :
          self.cursor += delta
          # print(f"[INFO] Cursor: {self.cursor}")

      if (self.activeHands == ACTIVE_HANDS_LEFT) :
        try :
          index = self.cursorsLeft.index(self.cursor)
        except :
          print("[DEBUG] The current cursor is not aligned to browse the left hand.")
          
        if ((index + delta) >= 0) :
          self.cursor = self.cursorsLeft[index + delta]
          # print(f"[INFO] Cursor: {self.cursor}")

      if (self.activeHands == ACTIVE_HANDS_RIGHT) :
        try :
          index = self.cursorsRight.index(self.cursor)
        except :
          print("[DEBUG] The current cursor is not aligned to browse the right hand.")
          
        if (index + delta >= 0) :
          self.cursor = self.cursorsRight[index + delta]
          # print(f"[INFO] Cursor: {self.cursor}")



  # ---------------------------------------------------------------------------
  # METHOD <cursorNext>
  #
  # Increase the cursor value of +1 step, with wrapping if loop mode is enabled
  # ---------------------------------------------------------------------------
  def cursorNext(self) :

    if self.loopEnable :
      if ((self.cursor + 1) <= self.loopEnd) :
        self.cursorStep(1)
      else : 
        self.cursor = self.loopStart
      
      print(f"[INFO] Cursor: {self.cursor}")

    else :
      self.cursorStep(1)

    self.comboCount += 1
    if (self.comboCount > self.comboHighestSession) :
      self.comboHighestSession = self.comboCount

    if (self.comboCount > self.comboHighestAllTime) :
      self.comboHighestAllTime = self.comboCount


  # ---------------------------------------------------------------------------
  # METHOD <cursorAlignToHand>
  #
  # Return the first compatible value right after the current location.
  # ---------------------------------------------------------------------------
  def cursorAlignToHand(self, hand, direction = 0) :
    
    if (hand == LEFT_HAND) :
    
      if (direction > 0) : 
        subList = [x >= self.cursor for x in self.cursorsLeft]
        self.cursor = subList[0]

      if (direction < 0) : 
        subList = [x <= self.cursor for x in self.cursorsLeft]
        self.cursor = subList[-1]

      if (direction == 0) : 
        minIndex = 0
        dist = abs(self.cursor - self.cursorsLeft[0])
        for (index, cursorLeft) in enumerate(self.cursorsLeft[1:]) :
          if (abs(self.cursor - cursorLeft) < dist) :
            dist = abs(self.cursor - cursorLeft)
            minIndex = index+1
          
        self.cursor = self.cursorsLeft[minIndex]


    if (hand == RIGHT_HAND) :
    
      if (direction > 0) : 
        subList = [x >= self.cursor for x in self.cursorsRight]
        self.cursor = subList[0]

      if (direction < 0) : 
        subList = [x <= self.cursor for x in self.cursorsRight]
        self.cursor = subList[-1]

      if (direction == 0) : 
        minIndex = 0
        dist = abs(self.cursor - self.cursorsRight[0])
        for (index, cursorRight) in enumerate(self.cursorsRight[1:]) :
          if (abs(self.cursor - cursorRight) < dist) :
            dist = abs(self.cursor - cursorRight)
            minIndex = index+1
          
        self.cursor = self.cursorsRight[minIndex]
      


  # ---------------------------------------------------------------------------
  # METHOD <cursorBegin>
  #
  # Set the cursor to the beginning of the score
  # ---------------------------------------------------------------------------
  def cursorBegin(self) :
    
    # If the loop mode is enabled, we want to go back to the beginning of the loop
    if (self.loopEnable and (self.cursor >= self.loopStart)) :
      self.cursor = self.loopStart
    
    # Otherwise just set the cursor home
    else :
      if (self.activeHands == ACTIVE_HANDS_RIGHT) :
        self.cursor = self.cursorsRight[0]
      elif (self.activeHands == ACTIVE_HANDS_LEFT) :
        self.cursor = self.cursorsLeft[0]
      else :
        self.cursor = 0



  # ---------------------------------------------------------------------------
  # METHOD <cursorEnd>
  #
  # Set the cursor to the end of the score
  # ---------------------------------------------------------------------------
  def cursorEnd(self) :
    
    if (self.loopEnable and (self.cursor <= self.loopEnd)) :
      self.cursor = self.loopEnd
    
    # Otherwise just set the cursor to the end
    else :
      if (self.activeHands == ACTIVE_HANDS_RIGHT) :
        self.cursor = self.cursorsRight[-1]
      elif (self.activeHands == ACTIVE_HANDS_LEFT) :
        self.cursor = self.cursorsLeft[-1]
      else :
        self.cursor = len(self.noteOntimecodesMerged)-1



  # ---------------------------------------------------------------------------
  # METHOD <cursorJumpToNextMatch>
  #
  # Search feature: move the cursor to the next location where the given notes
  # appear in the score.
  # Direction of search can be specified.
  # ---------------------------------------------------------------------------
  def cursorJumpToNextMatch(self, noteList, direction = 1) :

    if (direction >= 0) :
      if (self.activeHands == ACTIVE_HANDS_RIGHT) :
        timecodeSearchField = [x > self.cursor for x in self.cursorsRight]
      elif (self.activeHands == ACTIVE_HANDS_LEFT) :
        timecodeSearchField = [x > self.cursor for x in self.cursorsRight]
      else :
        timecodeSearchField = [x for x in range(self.cursor+1, len(self.noteOntimecodesMerged))]
    
    else :
      if (self.activeHands == ACTIVE_HANDS_RIGHT) :
        timecodeSearchField = [x < self.cursor for x in self.cursorsRight]
      elif (self.activeHands == ACTIVE_HANDS_LEFT) :
        timecodeSearchField = [x < self.cursor for x in self.cursorsRight]
      else :
        timecodeSearchField = [x for x in range(0, self.cursor)]

      timecodeSearchField.sort(reverse = True)


    pitchList = [index for (index, element) in enumerate(noteList) if element == 1]
    found = False

    # Loop on the notes of the score
    for cursorTry in timecodeSearchField :
      
      foundPitch = []
      
      for pitch in pitchList :
        for (staffIndex, _) in enumerate(self.pianoRoll) :
          for noteObj in self.pianoRoll[staffIndex][pitch] :
            
            # Detect a note pressed at this timecode
            if (noteObj.startTime == self.noteOntimecodesMerged[cursorTry]) :
              foundPitch.append(noteObj.pitch)

      if (len(foundPitch) > 0) :
        isInList = True
        
        for x in pitchList :
          if not(x in foundPitch) :
            isInList = False
            break
        
        if isInList :
          print(f"[NOTE] Find: current input was found at cursor = {cursorTry}")
          found = True
          foundCursor = cursorTry
          break
      
    if found :
      
      # We must prevent the arbiter from taking this as a valid input
      # and move on to the next cursor
      # All notes must be released before moving on.
      self.cursor = foundCursor
      self.arbiterSuspendReq = True
      self.arbiterPitchListHold = pitchList.copy()
    
    else :
      print("[NOTE] Could not find the current MIDI notes in the score!")



  # ---------------------------------------------------------------------------
  # METHOD <getCurrentKey>
  #
  # Return the current key the song is in, if any has been set.
  # ---------------------------------------------------------------------------
  def getCurrentKey(self) :
    
    # No key in the score
    if (len(self.keyList) == 0) :
      return None
    
    # Otherwise, return the latest key applied
    else :
      scalesBefore = [x for x in self.keyList if (x.startTime <= self.cursor)]
      return scalesBefore[-1]



  # ---------------------------------------------------------------------------
  # METHOD <gotoNextBookmark>
  #
  # Set the cursor to the next closest bookmark (if any, otherwise do nothing)
  # ---------------------------------------------------------------------------
  def gotoNextBookmark(self) :
    
    # Is there any bookmark?
    if (len(self.bookmarks) > 0) :
      tmp = [x for x in self.bookmarks if (x > self.cursor)]
      if (len(tmp) > 0) :
        self.cursor = tmp[0]
      else :
        print(f"[NOTE] Last bookmark reached")
    
    # Is there any bookmark?
    else :
      print(f"[NOTE] No bookmark!")



  # ---------------------------------------------------------------------------
  # METHOD <gotoPreviousBookmark>
  #
  # Set the cursor to the previous closest bookmark (if any, otherwise do nothing)
  # ---------------------------------------------------------------------------
  def gotoPreviousBookmark(self) :

    # Is there any bookmark?
    if (len(self.bookmarks) > 0) :
      tmp = [x for x in self.bookmarks if (x < self.cursor)]
      if (len(tmp) > 0) :
        self.cursor = tmp[-1]
      else :
        print(f"[NOTE] First bookmark reached")
    
    else :
      print(f"[NOTE] No bookmark!")



  # ---------------------------------------------------------------------------
  # METHOD <toggleBookmark>
  #
  # Toggles a bookmark at the current location pointed by the cursor.
  # ---------------------------------------------------------------------------
  def toggleBookmark(self) :

    # Is it an existing bookmark?
    if self.cursor in self.bookmarks :
      self.bookmarks = [x for x in self.bookmarks if (x != self.cursor)]
      print(f"[NOTE] Bookmark removed at time {self.cursor}")
    
    # New bookmark
    else :
      print(f"[NOTE] Bookmark added at cursor {self.getCursor()} (timecode = {self.getCurrentTimecode()})")
      self.bookmarks.append(self.cursor)
      self.bookmarks.sort()

    self.hasUnsavedChanges = True



  # ---------------------------------------------------------------------------
  # METHOD <toggleLeftHand>
  #
  # Turns ON/OFF the left hand practice
  # ---------------------------------------------------------------------------
  def toggleLeftHand(self) :

    if ((self.activeHands == ACTIVE_HANDS_BOTH) or (self.activeHands == ACTIVE_HANDS_RIGHT)) :
      self.activeHands = ACTIVE_HANDS_LEFT
      self.cursorAlignToHand(LEFT_HAND)
    
    else :
      self.activeHands = ACTIVE_HANDS_BOTH



  # ---------------------------------------------------------------------------
  # METHOD <toggleRightHand>
  #
  # Turns ON/OFF the practice on left hand
  # ---------------------------------------------------------------------------
  def toggleRightHand(self) :
      
    if ((self.activeHands == ACTIVE_HANDS_BOTH) or (self.activeHands == ACTIVE_HANDS_LEFT)) :
      self.activeHands = ACTIVE_HANDS_RIGHT
      self.cursorAlignToHand(RIGHT_HAND)
    
    else :
      self.activeHands = ACTIVE_HANDS_BOTH





  def setLoopStart(self) :
    
    # Loop end is not yet defined
    if (self.loopEnd == -1) :
      self.loopStart = self.getCursor()
      print(f"[NOTE] Start of loop set at {self.loopStart+1}")

    else :
      if (self.getCursor() < self.loopEnd) :
        self.loopStart = self.getCursor()
        self.loopEnable = True
        print(f"[NOTE] Loop set: start = {self.loopStart+1} / end = {self.loopEnd+1}")




  def setLoopEnd(self) :
    
    # Loop start is not yet defined
    if (self.loopStart == -1) :
      self.loopEnd = self.getCursor()
      print(f"[NOTE] End of loop set at {self.loopEnd+1}")

    else :
      if (self.getCursor() > self.loopStart) :
        self.loopEnd = self.getCursor()
        self.loopEnable = True
        self.cursor = self.loopStart
        print(f"[NOTE] Loop set: start = {self.loopStart+1} / end = {self.loopEnd+1}")
  



  def clearLoop(self) :
    self.loopStart = -1
    self.loopEnd = -1
    self.loopEnable = False
    print("[NOTE] Loop cleared.")



  # ---------------------------------------------------------------------------
  # METHOD <_updateTeacherNotes> (private)
  #
  # Build the list (<teacherNotes>) of current expected notes to be played at 
  # that time.
  # ---------------------------------------------------------------------------
  def _updateTeacherNotes(self) :
    
    # Reset the play attributes of the previous notes before deleting them
    if len(self.teacherNotes) > 0 :
      for noteObj in self.teacherNotes :
        noteObj.visible = True
        noteObj.sustained = False
        noteObj.inactive = False

    self.teacherNotes = []
    self.teacherNotesMidi = [0 for _ in range(128)]    # same information as <teacherNotes> but different structure
    
    # Loop on the notes of the score
    for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
      for (staffIndex, _) in enumerate(self.pianoRoll) :
        for noteObj in self.pianoRoll[staffIndex][pitch] :
          
          # Detect a note pressed at this timecode
          if (noteObj.startTime == self.getCurrentTimecode()) :
            
            # Single hand practice mode: flag the notes of the other hand as "inactive"
            # so that it is displayed with the appropriate color
            if ((self.activeHands == ACTIVE_HANDS_LEFT) and (staffIndex == RIGHT_HAND)) :
              noteObj.inactive = True

            elif ((self.activeHands == ACTIVE_HANDS_RIGHT) and (staffIndex == LEFT_HAND)) :
              noteObj.inactive = True

            else :
              self.inactive = False
              self.teacherNotes.append(noteObj)
              self.teacherNotesMidi[pitch] = 1

          # Detect a note held at this timecode
          if ((self.getCurrentTimecode() > noteObj.startTime) and (self.getCurrentTimecode() <= noteObj.stopTime)) :
            noteObj.sustained = True
            self.teacherNotes.append(noteObj)



  # ---------------------------------------------------------------------------
  # METHOD <getTeacherNotes>
  #
  # Return the list of all notes that must be pressed at the current cursor
  # location in the score.
  # Note: notes that were pressed before and held up to the current cursor are
  #       not included. To list them, use <getSustainedNotes>.
  # ---------------------------------------------------------------------------
  def getTeacherNotes(self) :
    self._updateTeacherNotes()
    return self.teacherNotes



  # ---------------------------------------------------------------------------
  # METHOD <switchHand>
  #
  # Affects a given note to the other hand.
  # ---------------------------------------------------------------------------
  def switchHand(self, note) :

    if (note.hand == LEFT_HAND) :
      sourceHand = LEFT_HAND
      destHand = RIGHT_HAND

      self.cursorsRight.append(self.cursor)
      self.cursorsRight.sort()
      self.cursorsLeft.remove(self.cursor)

    else :
      sourceHand = RIGHT_HAND
      destHand = LEFT_HAND

      self.cursorsLeft.append(self.cursor)
      self.cursorsLeft.sort()
      self.cursorsRight.remove(self.cursor)

      
    # Update the note property
    note.hand = destHand
    
    # Move the note in the pianoroll
    self.pianoRoll[destHand][note.pitch].append(note)
    self.pianoRoll[destHand][note.pitch].sort(key = lambda x: x.startTime)
    del self.pianoRoll[sourceHand][note.pitch][note.noteIndex]

    if not(note.startTime in self.noteOntimecodes[destHand]) :
      self.noteOntimecodes[destHand].append(note.startTime)
      self.noteOntimecodes[destHand].sort()
    
    # Remove this timecode from the timecode list of the original hand
    # unless there is another note that has the same startTime
    # Quite an oddity but better take it into account.
    doubleStart = False
    for x in self.pianoRoll[sourceHand][note.pitch] :
      if (x.startTime == note.startTime) :
        doubleStart = True
        break
    
    if not(doubleStart) :
      self.noteOntimecodes[destHand].remove(note.startTime)

    
    



  # ---------------------------------------------------------------------------
  # METHOD <toggleRehearsalMode>
  #
  # Turns ON/OFF the rehearsal mode (ie progress in the score is halted no 
  # matter what is being played)
  # ---------------------------------------------------------------------------
  def toggleRehearsalMode(self) :
    self.progressEnable = not(self.progressEnable)
    print("[NOTE] Rehearsal mode will be available in a future release.")



  # ---------------------------------------------------------------------------
  # METHOD <importFromFile>
  #
  # Load the internal piano roll from an external file (.mid or .pr)
  # ---------------------------------------------------------------------------
  def importFromFile(self, inputFile) :
    if (os.path.splitext(inputFile)[-1] == ".mid") :
      self._importFromMIDIFile(inputFile)
    else :
      self._importFromPrFile(inputFile)

    self.hasUnsavedChanges = False

  # ---------------------------------------------------------------------------
  # METHOD <importFromMIDIFile>
  #
  # Builds the piano roll (i.e. a 128-elements array) from a MIDI file.
  # 
  # Input:
  # The MIDI file to read.
  #
  # Outputs:
  # - pianoRoll.noteArray
  # - pianoRoll.noteOnTimecodes
  # - pianoRoll.avgNoteDuration
  #
  # pianoRoll.noteArray[t][p] = [note0, note1, ...]
  # is the list of all notes played on track <t>, on pitch <p>. 
  # Each element of the list is an instance of the Note() class.
  # A Note() class has attributes:
  # - noteXXX.start/.end (integer) : timestamp of its beginning/end
  # - noteXXX.hand (string: "l", "r" or ""): hand used to play the note.
  #
  # pianoRoll.timecodes[t] = [t0, t1, ...]
  # ---------------------------------------------------------------------------
  def _importFromMIDIFile(self, midiFile) :

    mid = mido.MidiFile(midiFile)

    # TODO: give more flexibility when opening MIDI files
    # It is assumed here that the MIDI file has 2 tracks.
    # But in general MIDI files might contain more than that.
    # And in general, the user might want to map specific tracks to the staffs
    # and not only track 0 and 1.
    print(f"[NOTE] [MIDI import] Tracks found: {len(mid.tracks)}")
    self.nStaffs = len(mid.tracks)
    
    # Allocate outputs
    self.pianoRoll = [[[] for _ in range(128)] for _ in range(self.nStaffs)]
    self.noteOntimecodes = [[] for _ in range(self.nStaffs)]

    nNotes = 0; noteDuration = 0
    id = 0

    # Loop on the tracks
    for (trackNumber, track) in enumerate(mid.tracks) :

      currTime = 0
      for msg in track :

        # Update the current date ---------------------------------------------
        currTime += msg.time
        
        # Keypress event ------------------------------------------------------
        if ((msg.type == 'note_on') and (msg.velocity > 0)) :
          
          pitch = msg.note
          
          # Inspect the previous notes with the same pitch
          if (len(self.pianoRoll[trackNumber][pitch]) > 0) :
            
            # Detect if among these notes, one is still held
            for currNote in self.pianoRoll[trackNumber][pitch] :
              if (currNote.stopTime < 0) :
                print(f"[WARNING] [MIDI import] Ambiguous note {utils.noteName(pitch)}: a keypress overlaps a note that is already being pressed.")

                # New note detected: close the previous note.
                # That is one strategy, but it might be wrong. It depends on the song.
                # User should decide here.
                currNote.stopTime = currTime
                noteDuration += (currNote.stopTime - currNote.startTime)
                nNotes += 1.0
                id += 1

            # Append the new note to the list
            # Its duration is unknown for now, so set its endtime to NOTE_END_UNKNOWN = -1
            insertIndex = len(self.pianoRoll[trackNumber][pitch])
            self.pianoRoll[trackNumber][pitch].append(utils.Note(pitch, hand = trackNumber, noteIndex = insertIndex, startTime = currTime, stopTime = NOTE_END_UNKNOWN))
            
            # Append the timecode of this keypress
            if not(currTime in self.noteOntimecodes[trackNumber]) : 
              self.noteOntimecodes[trackNumber].append(currTime)
          
          # First note with this pitch
          else :
            
            # Append the new note to the list
            # Its duration is unknown for now, so set its endtime to NOTE_END_UNKNOWN = -1
            insertIndex = len(self.pianoRoll[trackNumber][pitch])
            self.pianoRoll[trackNumber][pitch].append(utils.Note(pitch, hand = trackNumber, noteIndex = insertIndex, startTime = currTime, stopTime = NOTE_END_UNKNOWN))
            
            # Append the timecode of this keypress
            if not(currTime in self.noteOntimecodes[trackNumber]) : 
              self.noteOntimecodes[trackNumber].append(currTime)



        # Keyrelease event ----------------------------------------------------
        if ((msg.type == 'note_off') or ((msg.type == 'note_on') and (msg.velocity == 0))) :
          
          pitch = msg.note

          # Take the latest event in the piano roll for this note
          noteObj = self.pianoRoll[trackNumber][pitch][-1]
          
          # Close it
          noteObj.stopTime = currTime
          noteObj.id = id
          
          noteDuration += (noteObj.stopTime - noteObj.startTime)
          nNotes += 1.0
          id += 1

          # Quite common apparently. Is that really an error case?
          # if (noteObj.startTime == noteObj.stopTime) :
          #   print(f"[WARNING] [MIDI import] MIDI note {pitch} ({utils.noteName(pitch)}) has null duration (start time = stop time = {noteObj.startTime})")
          #   self.pianoRoll[trackNumber][pitch].pop()



        # Others --------------------------------------------------------------
        # Other MIDI events are ignored.



    # Merge note ON time codes from both staves
    timecodesMerged = [item for sublist in self.noteOntimecodes for item in sublist]
    timecodesMerged = list(set(timecodesMerged))
    self.noteOntimecodesMerged = sorted(timecodesMerged)

    # The variable pointing in the <noteOntimecodesMerged> is called the "cursor" of the score.
    # This section lists the values of the cursor for which a noteOn event occured 
    # specifically on one hand or the other.
    # This is needed for the single hand practice mode.
    self.cursorsLeft = []; self.cursorsRight = []
    for (cursor, timecode) in enumerate(self.noteOntimecodesMerged) :
      if (timecode in self.noteOntimecodes[RIGHT_HAND]) :
        self.cursorsRight.append(cursor)

      if (timecode in self.noteOntimecodes[LEFT_HAND]) :
        self.cursorsLeft.append(cursor)

    # Estimate average note duration (needed for the piano roll display)
    self.avgNoteDuration = noteDuration/nNotes
    print(f"[NOTE] [MIDI import] Average note duration = {self.avgNoteDuration:.1f} ticks")



  # ---------------------------------------------------------------------------
  # METHOD <exportToPrFile>
  #
  # Export the piano roll and all metadata (finger, hand, comments etc.) in 
  # a .pr file (JSON)
  # ---------------------------------------------------------------------------
  def exportToPrFile(self, pianoRollFile) :
    
    # Create the dictionnary containing all the things we want to save
    exportDict = {}

    # Export "manually" elements of the PianoRoll object to the export dictionary.
    # Not ideal but does the job for now as there aren't too many properties.
    exportDict["revision"]              = f"v{REV_MAJOR}.{REV_MINOR}"

    exportDict["nStaffs"]               = self.nStaffs
    exportDict["avgNoteDuration"]       = self.avgNoteDuration
    
    exportDict["cursor"]                = self.cursor

    exportDict["noteOntimecodes"]       = self.noteOntimecodes
    exportDict["noteOntimecodesMerged"] = self.noteOntimecodesMerged
    exportDict["cursorsLeft"]           = self.cursorsLeft
    exportDict["cursorsRight"]          = self.cursorsRight

    exportDict["bookmarks"]             = self.bookmarks

    exportDict["activeHands"]           = self.activeHands

    exportDict["comboHighestAllTime"]   = self.comboHighestAllTime

    # TODO: export the scales
    # exportDict["scale"] = self.scale

    # Convert the Note() objects to a dictionnary before pushing them in the export dict
    exportDict["pianoRoll"] = [[[noteObj.__dict__ for noteObj in noteList] for noteList in trackList] for trackList in self.pianoRoll]

    with open(pianoRollFile, "w") as fileHandler :
      json.dump(exportDict, fileHandler)

    currTime = datetime.datetime.now()
    print(f"[NOTE] Saved to '{pianoRollFile}' at {currTime.strftime('%H:%M:%S')}")



  # ---------------------------------------------------------------------------
  # METHOD <importFromPrFile>
  #
  # Import the piano roll and all metadata (finger, hand, comments etc.)
  # from a .pr file (JSON) and restore them in the current session.
  # ---------------------------------------------------------------------------
  def _importFromPrFile(self, pianoRollFile) :
    
    with open(pianoRollFile, "r") as fileHandler :
      importDict = json.load(fileHandler)

    if (f"v{REV_MAJOR}.{REV_MINOR}" != importDict["revision"]) :
      print(f"[WARNING] [.pr import] Piano roll file was made in version {importDict['revision']}. Current version is v{REV_MAJOR}.{REV_MINOR}")

    # Safe loading feature
    safeDict = {
      "revision"              : "v0.0",
      "nStaffs"               : 2,
      "avgNoteDuration"       : 100.0,
      "cursor"                : 0,
      "noteOntimecodes"       : [[0], [0]],
      "noteOntimecodesMerged" : [0],
      "cursorsLeft"           : [0],
      "cursorsRight"          : [0],
      "bookmarks"             : [0],
      "activeHands"           : "LR",
      "comboHighestAllTime"   : 0
    }
    for currKey in safeDict :
      if currKey in importDict :
        safeDict[currKey] = importDict[currKey]

    # Import "manually" elements of the PianoRoll object to the export dictionary.
    # Not ideal but does the job for now as there aren't too many properties.
    self.nStaffs                = safeDict["nStaffs"]
    self.avgNoteDuration        = safeDict["avgNoteDuration"]

    self.cursor                 = safeDict["cursor"]

    self.noteOntimecodes        = safeDict["noteOntimecodes"]
    self.noteOntimecodesMerged  = safeDict["noteOntimecodesMerged"]
    self.cursorsLeft            = safeDict["cursorsLeft"]
    self.cursorsRight           = safeDict["cursorsRight"]

    self.bookmarks              = safeDict["bookmarks"]

    self.activeHands            = safeDict["activeHands"]

    self.comboHighestAllTime    = safeDict["comboHighestAllTime"]

    # TODO: import the scales
    # TODO: import the loops

    # Note() objects were converted to a dictionary. Convert them back to a Note object
    self.pianoRoll = [[[] for noteList in trackList] for trackList in importDict["pianoRoll"]]

    for track in range(self.nStaffs) :
      for pitch in GRAND_PIANO_MIDI_RANGE :
        for noteDict in importDict["pianoRoll"][track][pitch] :
          noteObj = utils.Note(noteDict['pitch'])
          
          for noteAttr in noteObj.__dict__ :
            setattr(noteObj, noteAttr, noteDict[noteAttr])
          
          self.pianoRoll[track][pitch].append(noteObj)


    print(f"[NOTE] {pianoRollFile} successfully loaded!")
    


  # ---------------------------------------------------------------------------
  # METHOD <_checkForChanges> (private)
  #
  # Detect if there are any unsaved changes and updates the attribute
  # <hasUnsavedChanges>
  # ---------------------------------------------------------------------------
  def _checkForChanges(self) :
    print("TODO")
    


  def isBookmarkedTimecode(self) :
    return (self.cursor in self.bookmarks)
  






  def guessScale(self, startCursor, span = -1) :
    print("TODO")
