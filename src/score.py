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
    
    self.progressEnable = True
    self.fsmState = FSM_STATE_NORMAL 

    

    # Loop practice feature
    self.loopEnable = False
    self.loopStart = 0
    self.loopEnd = 0





  
  def setTimecodes(self, timecodes) :
    self.timecodes = timecodes

    # Update <cursor> too as it might not be valid anymore
    # ...


  def cursorStep(self, delta) :

    if (self.fsmState == FSM_STATE_NORMAL) :
      if (delta > 0) :
        if ((self.timeIndex + delta) < (len(self.timecodes)-1)) :
          self.timeIndex += delta
          print(f"[INFO] Cursor: {self.timeIndex}")

      else :
        if ((self.timeIndex < delta) >= 0) :
          self.timeIndex -= delta
          print(f"[INFO] Cursor: {self.timeIndex}")


  

  def cursorReset(self) :
    
    if (self.fsmState == FSM_STATE_NORMAL) :
      self.timeIndex = 0



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
      print(f"[NOTE] Bookmark added at time {self.cursor}")
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
      # oracle.setTimecodesDB = pianoRoll.noteOnTimecodes[1]
    else :
      self.activeHands = "L" + self.activeHands[1]
      # oracle.setTimecodesDB = pianoRoll.noteOnTimecodesMerged

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



  # ---------------------------------------------------------------------------
  # METHOD <toggleRehearsalMode>
  #
  # Turns ON/OFF the rehearsal mode (ie progress in the score is halted no 
  # matter what is being played)
  # ---------------------------------------------------------------------------
  def toggleRehearsalMode(self) :
    self.progressEnable = not(self.progressEnable)
    




  def toggleLoopMode(self) :
    print("[NOTE] Loop practice will be available in a future release.")












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

    self.bookmarks = []
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

    # Loop on the tracks
    for (trackNumber, track) in enumerate(mid.tracks) :

      currTime = 0
      for msg in track :

        # Update the current date ---------------------------------------------
        currTime += msg.time
        
        # Keypress event ------------------------------------------------------
        if ((msg.type == 'note_on') and (msg.velocity > 0)) :
          
          pitch = msg.note
          
          # There was a note before this one. Is it done?
          if (len(self.pianoRoll[trackNumber][pitch]) > 0) :
            for currNote in self.pianoRoll[trackNumber][pitch] :
              if (currNote.stopTime < 0) :
                print(f"[WARNING] [MIDI import] MIDI note {pitch}: a keypress overlaps a note that is already being pressed.")

            l = len(self.pianoRoll[trackNumber][pitch])
            self.pianoRoll[trackNumber][pitch].append(utils.Note(pitch, hand = trackNumber, noteIndex = l, startTime = currTime, stopTime = -1))
            
            if not(currTime in self.noteOntimecodes[trackNumber]) : 
              self.noteOntimecodes[trackNumber].append(currTime)
          
          # New note
          else :
            # Its duration is unknown for now, so set its endtime to "-1"
            l = len(self.pianoRoll[trackNumber][pitch])
            self.pianoRoll[trackNumber][pitch].append(utils.Note(pitch, hand = trackNumber, noteIndex = l, startTime = currTime, stopTime = -1))
            
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
          nNotes += 1.0

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
      print(f"[WARNING] [.pr import] Loading piano roll file from {importDict['revision']}. Current version is v{REV_MAJOR}.{REV_MINOR}")

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
    
