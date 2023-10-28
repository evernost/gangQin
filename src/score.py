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
    
    self.bookmarks = []         # List of all bookmarked timecodes (integers)
    
    self.activeHands = "LR"
    
    self.teacherNotes = []
    self.teacherNotesMidi = [0 for _ in range(128)]
    self.sustainedNotes = []

    # Key scales used throughout the song
    # List of tuples: (scaleObject, startTimeCode)
    self.scale = []

    self.progressEnable = True
    self.fsmState = FSM_STATE_NORMAL 

    

    # Loop practice feature
    self.loopEnable = False
    self.loopStart = -1
    self.loopEnd = -1



  def getCursor(self) :
    return self.cursor



  def getCurrentTimecode(self) :
    return self.noteOntimecodesMerged[self.cursor]



  
  def setTimecodes(self, timecodes) :
    self.noteOntimecodes = timecodes

    # Update <cursor> too as it might not be valid anymore
    # ...


  # Increase / decrease the cursor value of a given step (positive or negative)
  # The cursor 
  def cursorStep(self, delta) :
  
    if (delta > 0) :
      if ((self.cursor + delta) < len(self.noteOntimecodesMerged)-1) :
        self.cursor += delta
        print(f"[INFO] Cursor: {self.cursor}")

    else :
      if ((self.cursor + delta) >= 0) :
        self.cursor += delta
        print(f"[INFO] Cursor: {self.cursor}")




  def cursorNext(self) :

    if self.loopEnable :
      if ((self.cursor + 1) <= self.loopEnd) :
        self.cursor += 1
      else : 
        self.cursor = self.loopStart
      
      print(f"[INFO] Cursor: {self.cursor}")

    else :
      self.cursorStep(1)

  

  def cursorReset(self) :
    
    if (self.loopEnable and (self.cursor >= self.loopStart)) :
      self.cursor = self.loopStart
    else :
      self.cursor = 0



  def cursorEnd(self) :
    
    if (self.loopEnable and (self.cursor <= self.loopEnd)) :
      self.cursor = self.loopEnd
    




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
  # Turns ON/OFF the practice on left hand
  # ---------------------------------------------------------------------------
  def toggleLeftHand(self) :

    # TODO: update the timecode set we are working on!!
    # TODO: update the current location

    if (self.activeHands[0] == "L") :
      self.activeHands = " " + self.activeHands[1]
    else :
      self.activeHands = "L" + self.activeHands[1]



  # ---------------------------------------------------------------------------
  # METHOD <toggleRightHand>
  #
  # Turns ON/OFF the practice on left hand
  # ---------------------------------------------------------------------------
  def toggleRightHand(self) :

    # TODO: update the timecode set we are working on!!
    # TODO: update the current location

    if (self.activeHands[1] == "R") :
      self.activeHands = self.activeHands[0] + " "
      # oracle.setTimecodesDB = pianoRoll.noteOnTimecodes[0]
    else :
      self.activeHands = self.activeHands[0] + "R"
      # oracle.setTimecodesDB = pianoRoll.noteOnTimecodesMerged






  def setLoopStart(self) :
    
    # Loop end is not yet defined
    if (self.loopEnd == -1) :
      self.loopStart = self.getCursor()
      print(f"[NOTE] Start of loop set at {self.loopStart}")

    else :
      if (self.getCursor() < self.loopEnd) :
        self.loopStart = self.getCursor()
        self.loopEnable = True
        print(f"[NOTE] Loop set: start = {self.loopStart} / end = {self.loopEnd}")




  def setLoopEnd(self) :
    
    # Loop start is not yet defined
    if (self.loopStart == -1) :
      self.loopEnd = self.getCursor()
      print(f"[NOTE] End of loop set at {self.loopEnd}")

    else :
      if (self.getCursor() > self.loopStart) :
        self.loopEnd = self.getCursor()
        self.loopEnable = True
        print(f"[NOTE] Loop set: start = {self.loopStart} / end = {self.loopEnd}")
    

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
    
    self.teacherNotes = []
    self.teacherNotesMidi = [0 for _ in range(128)]    # same information as <teacherNotes> but different structure
    
    # Two hands mode
    if (self.activeHands == "LR") :
      for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        for (staffIndex, _) in enumerate(self.pianoRoll) :
          for noteObj in self.pianoRoll[staffIndex][pitch] :
            if (noteObj.startTime == self.getCurrentTimecode()) :
              self.teacherNotes.append(noteObj)
              self.teacherNotesMidi[pitch] = 1

    # Left hand practice
    if (self.activeHands == "L ") :
      staffIndex = 0
      for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        for noteObj in self.pianoRoll[staffIndex][pitch] :
          if (noteObj.startTime == self.getCurrentTimecode()) :
            self.teacherNotes.append(noteObj)
            self.teacherNotesMidi[pitch] = 1

    # Right hand practice
    if (self.activeHands == " R") :
      staffIndex = 1
      for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        for noteObj in self.pianoRoll[staffIndex][pitch] :
          if (noteObj.startTime == self.getCurrentTimecode()) :
            self.teacherNotes.append(noteObj)
            self.teacherNotesMidi[pitch] = 1



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
  # METHOD <_updateSustainedNotes> (private)
  #
  # See <getSustainedNotes>.
  # ---------------------------------------------------------------------------
  def _updateSustainedNotes(self) :
    
    self.sustainedNotes = []
    
    for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
      for (staffIndex, _) in enumerate(self.pianoRoll) :
        for noteObj in self.pianoRoll[staffIndex][pitch] :
          if ((self.getCurrentTimecode() > noteObj.startTime) and (self.getCurrentTimecode() <= noteObj.stopTime)) :
            self.sustainedNotes.append(noteObj)



  # ---------------------------------------------------------------------------
  # METHOD <getSustainedNotes>
  #
  # Return the list of all notes that are not pressed at the current cursor
  # but still active (sustained)
  # This list is purely used for display purposes (to show what notes are
  # maintainted) / informative purposes
  # These notes are not expected to be played by the user.
  # ---------------------------------------------------------------------------
  def getSustainedNotes(self) :
    self._updateSustainedNotes()
    return self.sustainedNotes




  # ---------------------------------------------------------------------------
  # METHOD <updateNoteProperties>
  #
  # 
  # ---------------------------------------------------------------------------
  def updateNoteProperties(self, note) :
    self.pianoRoll[note.hand][note.pitch][note.noteIndex].finger = note.finger








  # ---------------------------------------------------------------------------
  # METHOD <toggleRehearsalMode>
  #
  # Turns ON/OFF the rehearsal mode (ie progress in the score is halted no 
  # matter what is being played)
  # ---------------------------------------------------------------------------
  def toggleRehearsalMode(self) :
    self.progressEnable = not(self.progressEnable)
    print("[NOTE] Rehearsal mode will be available in a future release.")




  def toggleLoopMode(self) :
    print("[NOTE] Loop practice will be available in a future release.")





  # ---------------------------------------------------------------------------
  # METHOD <toggleRehearsalMode>
  #
  # Return the current scale of the song based on the cursor.
  # ---------------------------------------------------------------------------
  def getCurrentScale(self) :
    print("[NOTE] Showing the current scale will be available in a future release.")





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
          
          # There is a note with the same pitch before this one
          if (len(self.pianoRoll[trackNumber][pitch]) > 0) :
            
            # Detect if a note is pressed while a previous one was not released
            for currNote in self.pianoRoll[trackNumber][pitch] :
              if (currNote.stopTime < 0) :
                print(f"[WARNING] [MIDI import] Ambiguous note {utils.noteName(pitch)}: a keypress overlaps a note that is already being pressed.")

                # Close the previous note
                # That is one strategy, but it might be wrong. It depends on the song.
                # User should decide here.
                currNote.stopTime = currTime


            l = len(self.pianoRoll[trackNumber][pitch])
            self.pianoRoll[trackNumber][pitch].append(utils.Note(pitch, hand = trackNumber, noteIndex = l, startTime = currTime, stopTime = -1))
            
            if not(currTime in self.noteOntimecodes[trackNumber]) : 
              self.noteOntimecodes[trackNumber].append(currTime)
          
          # New note
          else :
            # Its duration is unknown for now, so set its endtime to "-1"
            insertLoc = len(self.pianoRoll[trackNumber][pitch])
            self.pianoRoll[trackNumber][pitch].append(utils.Note(pitch, hand = trackNumber, noteIndex = insertLoc, startTime = currTime, stopTime = -1))
            
            if not(currTime in self.noteOntimecodes[trackNumber]) : 
              self.noteOntimecodes[trackNumber].append(currTime)

        # Keyrelease event ----------------------------------------------------
        if ((msg.type == 'note_off') or ((msg.type == 'note_on') and (msg.velocity == 0))) :
          
          pitch = msg.note

          # Take the latest event in the piano roll for this note
          # noteObj = self.pianoRoll[trackID][pitch][-1]
          
          # Close it
          self.pianoRoll[trackNumber][pitch][-1].stopTime = currTime
          noteDuration += (self.pianoRoll[trackNumber][pitch][-1].stopTime - self.pianoRoll[trackNumber][pitch][-1].startTime)
          self.pianoRoll[trackNumber][pitch][-1].id = id
          nNotes += 1.0
          id += 1

          # if (noteObj.startTime == noteObj.stopTime) :
          #   print(f"[WARNING] MIDI note {pitch} ({noteName(pitch)}): ignoring note with null duration (start time = stop time = {noteObj.startTime})")
          #   self.pianoRoll[pitch].pop()

        # Others --------------------------------------------------------------
        # Other MIDI events are ignored.

    

    # Merge note ON time codes from both staves
    timecodesMerged = [item for sublist in self.noteOntimecodes for item in sublist]
    timecodesMerged = list(set(timecodesMerged))
    self.noteOntimecodesMerged = sorted(timecodesMerged)

    # Estimate average note duration
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
    exportDict["revision"] = f"v{REV_MAJOR}.{REV_MINOR}"
    exportDict["nStaffs"] = self.nStaffs
    exportDict["noteOntimecodes"] = self.noteOntimecodes
    exportDict["noteOntimecodesMerged"] = self.noteOntimecodesMerged
    exportDict["avgNoteDuration"] = self.avgNoteDuration
    exportDict["bookmarks"] = self.bookmarks

    # TODO: export the scales
    # exportDict["scale"] = self.scale

    # Convert the Note() objects to a dictionnary before pushing them in the export dict
    exportDict["pianoRoll"] = [[[noteObj.__dict__ for noteObj in noteList] for noteList in trackList] for trackList in self.pianoRoll]

    with open(pianoRollFile, "w") as fileHandler :
      json.dump(exportDict, fileHandler)

    print(f"[NOTE] Saved to {pianoRollFile}!")



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
      print(f"[WARNING] [.pr import] Piano roll file was made in version v{importDict['revision']}. Current version is v{REV_MAJOR}.{REV_MINOR}")

    # TODO: check here that all fields exist. Previous versions might not have them
    # if ...
    # else :
    #   raise SystemExit(0)

    # Import "manually" elements of the PianoRoll object to the export dictionary.
    # Not ideal but does the job for now as there aren't too many properties.
    self.nStaffs                = importDict["nStaffs"]
    self.noteOntimecodes        = importDict["noteOntimecodes"]
    self.noteOntimecodesMerged  = importDict["noteOntimecodesMerged"]
    self.avgNoteDuration        = importDict["avgNoteDuration"]
    self.bookmarks              = importDict["bookmarks"]

    # Note() objects were converted to a dictionary. Convert them back to a Note object
    self.pianoRoll = [[[utils.Note(**noteDict) for noteDict in noteList] for noteList in trackList] for trackList in importDict["pianoRoll"]]

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
  



