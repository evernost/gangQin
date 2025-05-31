# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : Score (inherited from Widget)
# File name     : score.py
# File type     : Python script (Python 3)
# Purpose       : provides the functions to interact with the music score
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Thursday, 5 October 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project specific constants
from src.commons import *

import src.note as note
import src.widgets.widget as widget
import text

import copy
import datetime
import json       # for .gq file database import/export
import mido       # for MIDI file manipulation
import os         # for filename manipulation
import pygame
import time



# =============================================================================
# CONSTANTS POOL
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Score(widget.Widget) :

  """
  SCORE object
  
  The Score object is a database storing the song in a structure that is suited 
  for the gameplay.
  
  Score is first initialised from a MIDI file. 
  All the notes and their timings are read and stored in a custom representation.

  The Score objects gives various utility functions that help in various tasks:
  - navigate through the score
  - return the notes that must be pressed at a given moment 
  - store context-based user information (fingersatz, comments, tempo, etc.)
  
  As you play, edit, add information, etc. those annotations are joined
  to the database in a custom file (.gq) 
  A .gq file is nothing more but a JSON file, so it remains human readable.
  
  The 'cursor' concept: 
  In a MIDI file, each event (note on/note off) has a timestamp attached.
  The value of the timestamp depends on the duration of the note, the tempo etc.
  
  In the Score object, these timestamps are abstracted and you browse in the 
  song using a 'cursor'.
  There is a cursor value for every unique moment a note starts playing.
  Chords contribute to 1 value of the cursor.
  """

  def __init__(self, top) :
    
    # Call the Widget init method
    super().__init__(top, loc = WIDGET_LOC_UNDEFINED)
   
    # Pointer in the score
    self.cursor = 0         # Range: 0 ... score.cursorMax
    self.cursorsLeft = []
    self.cursorsRight = []
    self.bookmarks = []
    self.cursorMax = 0
    self.length = 0

    # Internal representation
    self.noteList = []
    self.pianoRoll = [[[] for _ in range(128)] for _ in range(SCORE_N_STAFF)]   # Cursed old school format (deprecated)
    self.noteOnTimecodes = {"L": [], "R": [], "LR": [], "LR_full": []}

    # Options for Score.getTeacherNotes()
    self.teacherNotes = []
    self.teacherNotesCursor = -1
    self.lookAheadDistance = 0
    self.activeHands = "LR"
    
    # Sections in the score
    self.sectionLoop = []
    self.sectionKey = []
    self.sectionWeakArbitration = []
    self.sectionTempo = []
    
    # Settings for the interaction with the cursor
    self.loopStart = -1
    self.loopEnd = -1
    self.loopEnable = False
    
    # Custom attributes (not organised yet)
    self.hasUnsavedChanges = False
    self.avgNoteDuration = 0



  # ---------------------------------------------------------------------------
  # METHOD Score.loadMIDIFile_v2_DEPRECATED()
  # ---------------------------------------------------------------------------
  def loadMIDIFile_v2_DEPRECATED(self, midiFile: str, midiTracks: list[str]) -> None :
    """
    ********
    WARNING: this version generates the old school score database from MIDI.
    Use it for compatibility from gangQin v2 to v3 only.
    ********
    
    Loads and initialises the Score object from a MIDI file.

    'midiFile' must be the full path to the file with its extension.
    Example: './songs/Chopin_Etude_Op_10_No_1.mid'
    """
    
    print("[INFO] Importing MIDI file... ")
    
    # For statistics
    startTime = time.time()

    # Open MIDI file
    midiData = mido.MidiFile(midiFile)

    # Initialise attributes 
    self.pianoRoll = [[[] for _ in range(128)] for _ in range(SCORE_N_STAFF)]
    self.noteOnTimecodes = {"L": [], "R": [], "LR": [], "LR_full": []}
    noteCount = 0; noteDuration = 0
    
    # Assign a unique identifier to each note (simple counter)
    id = 0

    # Loop on the tracks, decode the MIDI messages
    for (i, track) in enumerate(midiData.tracks) :
      
      # Process the track if it is linked to left or right hand
      # Ignore it otherwise
      if (midiTracks[i] != "") :
        if (midiTracks[i] == "R") : trackID = SCORE_RIGHT_HAND_TRACK_ID
        if (midiTracks[i] == "L") : trackID = SCORE_LEFT_HAND_TRACK_ID
      
        currTime = 0
        currTempo = 0
        for msg in track :

          # Update the current time
          currTime += msg.time
          
          # Keypress event
          if ((msg.type == 'note_on') and (msg.velocity > 0)) :
            
            pitch = msg.note
            
            # Inspect the previous notes with the same pitch
            if (len(self.pianoRoll[trackID][pitch]) > 0) :
              
              # Detect if among these notes, one is still held
              for currNote in self.pianoRoll[trackID][pitch] :
                if (currNote.stopTime < 0) :
                  print(f"[WARNING] Ambiguous note at t = {currTime} ({note.getFriendlyName(pitch)}): a keypress overlaps a hanging keypress on the same note.")

                  # New note detected: close the previous note.
                  # That is one strategy, but it might be wrong. It depends on the song.
                  # User should decide here.
                  currNote.stopTime = currTime
                  noteDuration += (currNote.stopTime - currNote.startTime)
                  noteCount += 1.0
                  id += 1

              # Append the new note to the list
              # Its duration is unknown for now, so set its endtime to NOTE_END_UNKNOWN = -1
              insertIndex = len(self.pianoRoll[trackID][pitch])
              newNote = note.Note(pitch)
              newNote.hand      = trackID
              newNote.id        = insertIndex
              newNote.startTime = currTime
              newNote.stopTime  = NOTE_END_UNKNOWN
              self.pianoRoll[trackID][pitch].append(newNote)
              
              # Append the timecode of this keypress
              if (trackID == SCORE_LEFT_HAND_TRACK_ID) :
                self.noteOnTimecodes["L"].append(currTime)
              elif (trackID == SCORE_RIGHT_HAND_TRACK_ID) :
                self.noteOnTimecodes["R"].append(currTime)
              else :
                print("[ERROR] Score.loadMIDIFile(): invalid track number (possible internal error)")

              self.noteOnTimecodes["LR_full"].append(currTime)
            
            # First note with this pitch
            else :
              
              # Append the new note to the list
              # Its duration is unknown for now, so set its endtime to NOTE_END_UNKNOWN = -1
              insertIndex = len(self.pianoRoll[trackID][pitch])
              newNote = note.Note(pitch)
              newNote.hand = trackID
              newNote.id = insertIndex
              newNote.startTime = currTime
              newNote.stopTime = NOTE_END_UNKNOWN
              self.pianoRoll[trackID][pitch].append(newNote)
              
              if (trackID == SCORE_LEFT_HAND_TRACK_ID) :
                self.noteOnTimecodes["L"].append(currTime)
              elif (trackID == SCORE_RIGHT_HAND_TRACK_ID) :
                self.noteOnTimecodes["R"].append(currTime)
              else :
                print("[ERROR] Score.loadMIDIFile(): invalid track number (possible internal error)")

              self.noteOnTimecodes["LR_full"].append(currTime)

          # Keyrelease event ----------------------------------------------------
          # NOTE: in some files, 'NOTE OFF' message is mimicked using a 'NOTE ON' with null velocity.
          elif ((msg.type == 'note_off') or ((msg.type == 'note_on') and (msg.velocity == 0))) :
            
            pitch = msg.note

            # Take the latest event in the piano roll for this note
            if (len(self.pianoRoll[trackID][pitch]) > 0) :
              noteObj = self.pianoRoll[trackID][pitch][-1]
              noteObj.stopTime = currTime
              noteObj.id = id
              noteDuration += (noteObj.stopTime - noteObj.startTime)
              noteCount += 1.0
              id += 1
            else :
              print("[WARNING] Score.loadMIDIFile(): read 'note OFF' with no matching 'note ON' event (possible MIDI corruption)")
            
            # Quite common apparently. Is that really an error case?
            # if (noteObj.startTime == noteObj.stopTime) :
            #   print(f"[WARNING] [MIDI import] MIDI note {pitch} ({note.getFriendlyName(pitch)}) has null duration (start time = stop time = {noteObj.startTime})")
            #   self.pianoRoll[trackNumber][pitch].pop()

          elif (msg.type == 'time_signature') :
            print(f"- read time signature: {msg.numerator}/{msg.denominator} (timecode = {currTime})")
            #eventTime = mido.tick2second(current_time, ticks_per_beat, tempo) for a display in seconds

          elif (msg.type == 'key_signature') :
            print(f"- read key signature: {msg.key} (timecode = {currTime})")

          elif (msg.type == 'set_tempo') :
            #print(f"- read new tempo: {msg.tempo} (timecode = {currTime})")
            currTempo = msg.tempo

          elif (msg.type == 'control_change') :
            pass

          elif (msg.type == 'program_change') :
            pass


    # Tidy up:
    # - sort the timecodes by ascending values
    # - remove duplicate entries
    self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
    self.noteOnTimecodes["LR_full"].sort()

    self.noteOnTimecodes["LR"] = list(set(self.noteOnTimecodes["LR_full"]))
    self.noteOnTimecodes["LR"].sort()

    # Build 'cursorsLeft' and 'cursorsRight' attributes
    self._buildCursorsLR()

    # Estimate average note duration (needed for the pianoroll display)
    self.avgNoteDuration = noteDuration/noteCount
    
    self.length = len(self.noteOnTimecodes["LR"])
    self.cursorMax = self.length-1
    
    print(f"- score length: {self.length} steps")

    stopTime = time.time()
    print(f"[INFO] Loading time: {stopTime-startTime:.2f}s")



  # ---------------------------------------------------------------------------
  # METHOD Score.loadMIDIFile()
  # ---------------------------------------------------------------------------
  def loadMIDIFile(self, midiFile: str, midiTracks: list[str]) -> None :
    """
    Loads and initialises the Score object from a MIDI file.

    'midiFile' must be the full path to the file with its extension.
    Example: './songs/Chopin_Etude_Op_10_No_1.mid'
    """
    
    print("[INFO] Importing MIDI file... ")
    
    # For statistics
    startTime = time.time()

    # Open MIDI file
    midiData = mido.MidiFile(midiFile)

    # Initialise attributes
    self.noteList = []
    self.noteOnTimecodes = {
      "L"       : [],
      "R"       : [],
      "LR"      : [],
      "LR_full" : []
    }
    
    noteCount = 0
    noteDuration = 0
    insertIndex = 0
    noteTracker = NoteTracker()

    # Loop on the tracks
    for (i, track) in enumerate(midiData.tracks) :
      
      # The track number has been paired with a hand 
      if (midiTracks[i] != "") :
        if (midiTracks[i] == "R") : trackID = SCORE_RIGHT_HAND_TRACK_ID
        if (midiTracks[i] == "L") : trackID = SCORE_LEFT_HAND_TRACK_ID
      
        # Loop on the notes within a track
        currTime = 0
        currTempo = 0
        for msg in track :

          currTime += msg.time

          if (msg.type in ["note_on", "note_off"]) :
            pitch = msg.note
          
          # MIDI EVENT: keypress
          if ((msg.type == "note_on") and (msg.velocity > 0)) :
            
            # Detect an overlapping keypress (new keypress without prior release)
            # This case is not supposed to happen.
            if noteTracker.isActive(pitch, trackID) :
              print(f"[WARNING] Score.loadMIDIFile(): odd keypress overlap on the same hand detected")
              i = noteTracker.getIndex(pitch, trackID)
              self.noteList[i].stopTime = currTime
              noteTracker.end(pitch, trackID)

            # Register the keypress in the database
            N = note.Note(pitch)
            N.hand      = trackID
            N.dbIndex   = insertIndex
            N.id        = insertIndex
            N.velocity  = msg.velocity
            N.startTime = currTime
            N.stopTime  = NOTE_END_UNKNOWN
            self.noteList.append(N)

            self.noteOnTimecodes["LR_full"].append(currTime)
            if (trackID == SCORE_LEFT_HAND_TRACK_ID)  : self.noteOnTimecodes["L"].append(currTime)
            if (trackID == SCORE_RIGHT_HAND_TRACK_ID) : self.noteOnTimecodes["R"].append(currTime)
            
            noteTracker.begin(pitch, trackID, insertIndex)
            insertIndex += 1
            
            #       # User should decide here.
            #       currNote.stopTime = currTime
            #       noteDuration += (currNote.stopTime - currNote.startTime)
            #       noteCount += 1.0
            #       id += 1


          # MIDI EVENT: key release
          elif ((msg.type == "note_off") or ((msg.type == "note_on") and (msg.velocity == 0))) :            
            
            if noteTracker.isActive(pitch, trackID) :
              i = noteTracker.getIndex(pitch, trackID)
              self.noteList[i].stopTime = currTime
              noteTracker.end(pitch, trackID)
              
            else :
              print(f"[WARNING] Score.loadMIDIFile(): read 'NOTE OFF' event with no matching 'NOTE ON'.")

          # MIDI EVENT: time signature change
          elif (msg.type == 'time_signature') :
            print(f"- read time signature: {msg.numerator}/{msg.denominator} (timecode = {currTime})")
            #eventTime = mido.tick2second(current_time, ticks_per_beat, tempo) for a display in seconds

          # MIDI EVENT: key signature change
          elif (msg.type == 'key_signature') :
            print(f"- read key signature: {msg.key} (timecode = {currTime})")

          # MIDI EVENT: tempo change
          elif (msg.type == 'set_tempo') :
            #print(f"- read new tempo: {msg.tempo} (timecode = {currTime})")
            currTempo = msg.tempo

          elif (msg.type == 'control_change') :
            pass

          elif (msg.type == 'program_change') :
            pass


    # Tidy up:
    # - sort the timecodes by ascending values
    # - remove duplicate entries
    self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
    self.noteOnTimecodes["LR_full"].sort()

    self.noteOnTimecodes["LR"] = list(set(self.noteOnTimecodes["LR_full"]))
    self.noteOnTimecodes["LR"].sort()

    # Build 'cursorsLeft' and 'cursorsRight' attributes
    self._buildCursorsLR()

    # Estimate average note duration (needed for the pianoroll display)
    self.avgNoteDuration = noteDuration/noteCount
    
    self.length = len(self.noteOnTimecodes["LR"])
    self.cursorMax = self.length-1
    
    print(f"- score length: {self.length} steps")

    stopTime = time.time()
    print(f"[INFO] Loading time: {stopTime-startTime:.2f}s")
    





  # ---------------------------------------------------------------------------
  # METHOD Score.loadPRFile()
  # ---------------------------------------------------------------------------
  def loadPRFile(self, prFile: str) -> None :
    """

    ********
    WARNING: pr files have been deprecated since gangQin v.3
    Use this function for conversion from .pr to .gq3 format only.
    Future version will use 'Score.loadGQ3File()' instead.
    ********

    Loads and initialises the Score object from a .pr file.

    'prFile' must be the full path to the file.

    Unlike MIDI files, .pr files store all the user annotated information 
    about the score (bookmarks, fingersatz, tempo, etc.)
    """
    
    # For statistics
    startTime = time.time()
    
    # Open the file as a JSON
    with open(prFile, "r") as fileHandler :
      importDict = json.load(fileHandler)

    # Read the revision
    rev = importDict["revision"][1:].split(".")
    revMajor = int(rev[0])
    revMinor = int(rev[1])
    
    # Fallback dictionary in case some fields do not exist.
    safeDict = {
      "revision"                  : "v0.0",
      "cursor"                    : 0,
      "cursorsLeft"               : [],
      "cursorsRight"              : [],
      "bookmarks"                 : [],
      "activeHands"               : "LR",
      "tempoSections"             : [(1, 120)],
      "weakArbitrationSections"   : []
    }
  
    # Load every existing field
    for currKey in safeDict :
      if currKey in importDict :
        safeDict[currKey] = importDict[currKey]

    # Initialize the object
    self.cursor     = safeDict["cursor"]
    self.bookmarks  = safeDict["bookmarks"]
    
    # -----------------------------
    # Pianoroll import - v0.X style
    # -----------------------------
    if (revMajor == 0) :
      print("[INFO] Importing dinosaur .pr file (versions v0.X) has been deprecated since gangQin v1.6")
      exit()
      
    # ---------------------------------
    # Pianoroll import - v1.0 and above
    # ---------------------------------
    self.pianoRoll = [[[] for _ in range(128)] for _ in range(SCORE_N_STAFF)]
    self.noteOnTimecodes = {"L": [], "R": [], "LR": [], "LR_full": []}
    noteCount = 0
    masteredNoteCount = 0
    for noteAsDict in importDict["pianoRoll"] :


      # # Note general attributes (fields preserved during file import/export)
      # self.pitch    = pitch
      # self.hand     = NOTE_UNDEFINED_HAND
      # self.finger   = NOTE_UNDEFINED_FINGER
      # self.voice    = NOTE_VOICE_DEFAULT

      # # Note database attributes (fields partially preserved during file import/export)
      # self.startTime  = 0     # Timecode of the key press event
      # self.stopTime   = 0     # Timecode of the key release event
      # self.dbIndex    = -1    # Index of the note in the score database
      # self.id         = -1    # Note unique identifier in the score (might change from a session to the other)
      
      # # Note display attributes (fields not preserved during file import/export)
      # self.sustained  = False     # True if the note is held at a given time
      # self.highlight  = False     # True if the note fingersatz is being edited
      # self.inactive   = False     # True if the note shall be ignored by the arbiter (single hand practice)
      # self.upcoming   = False     # True if the note is about to be played soon
      # self.upcomingDistance = 0   # The highest the value, the further the note
      # self.color      = self.getNoteColor()
      
      # # Not used anymore?
      # self.visible = False
      # self.disabled   = False         # True if the note shall be ignored by the arbiter (unplayable note)
      # self.fromKeyboardInput = False  # True if it is a note played by the user from the MIDI input
      # self.lookAheadDistance = 0      # Define how far away this note is located relative to the current cursor
      
      noteObj = note.Note(noteAsDict["pitch"])
      
      # Detect manual editions
      if (noteAsDict["name"] != noteObj.name) :
        print(f"[INFO] Manual edition detected: the new pitch will override the name.")
        print(f"- note name: {noteAsDict['name']} -> {noteObj.name}")
        print(f"- key color: {noteObj.keyColor}")

      noteObj.hand      = noteAsDict["hand"]
      noteObj.finger    = noteAsDict["finger"]
      noteObj.voice     = noteAsDict["voice"]
      noteObj.startTime = noteAsDict["startTime"]
      noteObj.stopTime  = noteAsDict["stopTime"]
      noteObj.dbIndex   = -1
      noteObj.id        = noteCount
      
      if (noteObj.finger != 0) :
        masteredNoteCount += 1

      self.pianoRoll[noteObj.hand][noteObj.pitch].append(noteObj)
      
      if (noteObj.hand == NOTE_LEFT_HAND) :
        self.noteOnTimecodes["L"].append(noteObj.startTime)
      elif (noteObj.hand == NOTE_RIGHT_HAND) :
        self.noteOnTimecodes["R"].append(noteObj.startTime)

      self.noteOnTimecodes["LR_full"].append(noteObj.startTime)
      
      noteCount += 1

    # Tidy up:
    # - sort the timecodes by ascending values
    # - remove duplicate entries
    self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
    self.noteOnTimecodes["LR_full"].sort()

    self.noteOnTimecodes["LR"] = set(self.noteOnTimecodes["LR_full"])
    self.noteOnTimecodes["LR"] = list(self.noteOnTimecodes["LR"])
    self.noteOnTimecodes["LR"].sort()

    # Build "cursorsLeft" and "cursorsRight".
    # Each one is a list of all cursors where something has to be played 
    # either on the left (cursorsLeft) or right hand (cursorsRight)
    self._buildCursorsLR()

    self.length = len(self.noteOnTimecodes["LR"])
    self.cursorMax = self.length-1

    stopTime = time.time()
    print(f"[INFO] Loading time: {stopTime-startTime:.2f}s")
    print(f"[INFO] {noteCount} notes read from .gq file.")
    print(f"[INFO] Score length: {self.length} steps")
    
    print(f"[INFO] Progress: {masteredNoteCount}/{noteCount} ({100*masteredNoteCount/noteCount:.1f}%)")



  # ---------------------------------------------------------------------------
  # METHOD Score.loadGQ3File()
  # ---------------------------------------------------------------------------
  def loadGQ3File(self, prFile: str) -> None :
    """
    Description is TODO.
    """
    
    # For statistics
    startTime = time.time()
    
    # Open the file as a JSON
    with open(prFile, "r") as fileHandler :
      importDict = json.load(fileHandler)

    # Read the revision
    rev = importDict["revision"][1:].split(".")
    revMajor = int(rev[0])
    revMinor = int(rev[1])
    
    # Fallback dictionary in case some fields do not exist.
    safeDict = {
      "revision"                  : "v0.0",
      "nStaffs"                   : 2,
      "avgNoteDuration"           : 100.0,
      "cursor"                    : 0,
      "cursorsLeft"               : [],
      "cursorsRight"              : [],
      "bookmarks"                 : [],
      "activeHands"               : "LR",
      "tempoSections"             : [(1, 120)],
      "weakArbitrationSections"   : []
    }
  
    # Load every existing field
    for currKey in safeDict :
      if currKey in importDict :
        safeDict[currKey] = importDict[currKey]

    # Initialize the object
    self.cursor           = safeDict["cursor"]
    self.bookmarks        = safeDict["bookmarks"]
    self.avgNoteDuration  = safeDict["avgNoteDuration"]
    
    # -----------------------------
    # Pianoroll import - v0.X style
    # -----------------------------
    if (revMajor == 0) :
      print("[INFO] Importing dinosaur .pr file (versions v0.X) has been deprecated since gangQin v1.6")
      exit()
      
    # ---------------------------------
    # Pianoroll import - v1.0 and above
    # ---------------------------------
    # From version 1.0, the pianoroll is flattened.
    # From version 1.3, the variables:
    # - 'noteOntimecodes'
    # - 'noteOntimecodesMerged'
    # - 'cursorsLeft'
    # - 'cursorsRight'
    # are rebuilt from the notes properties in the pianoroll.
    else :
      
      self.pianoRoll = [[[] for _ in range(128)] for _ in range(SCORE_N_STAFF)]
      self.noteOnTimecodes = {"L": [], "R": [], "LR": [], "LR_full": []}
      noteCount = 0
      masteredNoteCount = 0
      for noteObjImported in importDict["pianoRoll"] :

        # Create the object
        noteObj = note.Note(0)
        
        # List of all properties in a Note object, make a dictionary out of it.
        noteAttrDict = noteObj.__dict__.copy()
        
        # Make sure the ID is treated first, so that the warning later in the for loop
        # can display the ID of the edited note.
        noteObj.id = noteObjImported["id"]; del noteAttrDict["id"]

        # Detect manual editions
        noteNameExpected = note.getFriendlyName(noteObjImported["pitch"])
        noteNameActual   = noteObjImported["name"]
        newColor = NOTE_WHITE_KEY if ((noteObjImported["pitch"] % 12) in MIDI_CODE_WHITE_NOTES_MOD12) else NOTE_BLACK_KEY
        if (noteNameExpected != noteNameActual) :
          print(f"[INFO] Note ID {noteObj.id}: manual edition detected.")
          print(f"Following fields will be replaced:")
          print(f"- note name: {noteNameActual} -> {noteNameExpected}")
          print(f"- key color: {newColor}")
          noteObjImported["name"]     = noteNameExpected
          noteObjImported["keyColor"] = newColor

        # Loop on the attributes of the Note object
        # Set the attribute by string
        for noteAttr in noteAttrDict :
          if noteAttr in noteObjImported :
            setattr(noteObj, noteAttr, noteObjImported[noteAttr])
        
        if (noteObj.finger != 0) :
          masteredNoteCount += 1

        self.pianoRoll[noteObjImported["hand"]][noteObjImported["pitch"]].append(noteObj)
        
        if (noteObjImported["hand"] == NOTE_LEFT_HAND) :
          self.noteOnTimecodes["L"].append(noteObj.startTime)
        elif (noteObjImported["hand"] == NOTE_RIGHT_HAND) :
          self.noteOnTimecodes["R"].append(noteObj.startTime)

        self.noteOnTimecodes["LR_full"].append(noteObj.startTime)
        
        noteCount += 1
        
    # Tidy up:
    # - sort the timecodes by ascending values
    # - remove duplicate entries
    self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
    self.noteOnTimecodes["LR_full"].sort()

    self.noteOnTimecodes["LR"] = set(self.noteOnTimecodes["LR_full"])
    self.noteOnTimecodes["LR"] = list(self.noteOnTimecodes["LR"])
    self.noteOnTimecodes["LR"].sort()

    # Build "cursorsLeft" and "cursorsRight".
    # Each one is a list of all cursors where something has to be played 
    # either on the left (cursorsLeft) or right hand (cursorsRight)
    self._buildCursorsLR()

    self.length = len(self.noteOnTimecodes["LR"])
    self.cursorMax = self.length-1

    stopTime = time.time()
    print(f"[INFO] Loading time: {stopTime-startTime:.2f}s")
    print(f"[INFO] {noteCount} notes read from .gq file.")
    print(f"[INFO] Score length: {self.length} steps")
    
    print(f"[INFO] Progress: {masteredNoteCount}/{noteCount} ({100*masteredNoteCount/noteCount:.1f}%)")



  # ---------------------------------------------------------------------------
  # METHOD Score.exportToPRFile()
  # ---------------------------------------------------------------------------
  def exportToPRFile(self, prFile: str, backup = False) -> None :
    """

    ********
    WARNING: pr files have been deprecated since gangQin v.3
    Use 'Score.loadGQ3File()' instead.
    ********

    Exports the annotated score and all metadata (finger, hand, comments etc.) in 
    a .gq file (JSON) that can be imported later to restore the session.

    'gqFile' must be the full path to the file.

    Call the function with 'backup = True' to save under a '.bak' extension instead
    so that the original file is not overwritten. 
    """

    if backup :
      print("[INFO] Exporting a backup of the gangQin file...")
    else :
      print("[INFO] Exporting gangQin file...")

    # Create the dictionnary containing all the things we want to save
    exportDict = {}

    # Export "manually" elements of the PianoRoll object to the export dictionary.
    # Not ideal but does the job for now as there aren't too many properties.
    exportDict["revision"]        = f"v{REV_MAJOR}.{REV_MINOR}"
    exportDict["avgNoteDuration"] = self.avgNoteDuration
    exportDict["cursor"]          = self.getCursor()
    exportDict["bookmarks"]       = self.bookmarks

    noteCount = 0
    exportDict["pianoRoll"] = []
    for notesInTrack in self.pianoRoll :
      for notesInPitch in notesInTrack :
        for noteObj in notesInPitch :
          noteCount += 1
          
          noteObjCopy = copy.deepcopy(noteObj)
          noteExportAttr = noteObjCopy.__dict__

          # Filter out some note attributes that need not to be exported
          del noteExportAttr["highlight"]
          del noteExportAttr["upcoming"]
          del noteExportAttr["upcomingDistance"]
          del noteExportAttr["fromKeyboardInput"]
          del noteExportAttr["lookAheadDistance"]
          del noteExportAttr["visible"]

          exportDict["pianoRoll"].append(noteExportAttr)

    if backup :
      (root, _) = os.path.splitext(prFile)
      exportFile = root + ".bak"
    else :
      exportFile = prFile
    
    with open(exportFile, "w") as fileHandler :
      json.dump(exportDict, fileHandler, indent = 2)

    currTime = datetime.datetime.now()
    if backup :
      print(f"[INFO] Saved backup to '{exportFile}'")
    else :
      currTime = datetime.datetime.now()
      print(f"[DEBUG] {noteCount} notes written in .pr file.")
      print(f"[INFO] Saved to '{exportFile}' at {currTime.strftime('%H:%M:%S')}")



  # ---------------------------------------------------------------------------
  # METHOD Score.exportToGQ3File()
  # ---------------------------------------------------------------------------
  def exportToGQ3File(self, gqFile: str, backup = False) -> None :
    """
    Prototype function: export to GQ3 file (GangQin 3)

    Experimenting a format that is hopefully more 'diff' and 'merge' friendly.
    """

    output = {}
    output["revision"]  = f"v{REV_MAJOR}.{REV_MINOR}"
    output["cursor"]    = self.getCursor()
    output["bookmarks"] = self.bookmarks
    output["notelist"]  = []
    output["timecodelist"]  = []

    # Flatten the database
    # NOTE: will be deprecated as soon as the database structure is changed
    noteList = []
    for notesInTrack in self.pianoRoll :
      for notesInPitch in notesInTrack :
        for noteObj in notesInPitch :
          noteList.append(noteObj)

    # Sort the notes chronologically
    noteList.sort(key = lambda obj: obj.startTime)

    noteCount = 0
    for noteObj in noteList :
      noteAsDict = {
        "pitch"   : noteObj.pitch,
        "hand"    : noteObj.hand,
        "finger"  : noteObj.finger,
        "voice"   : noteObj.voice,
        "name"    : noteObj.name
      }
      output["notelist"].append(noteAsDict)
      
      timeMarkAsDict = {
        "starttime" : noteObj.startTime,
        "stoptime"  : noteObj.stopTime
      }
      output["timecodelist"].append(timeMarkAsDict)
      
      noteCount += 1


    if backup :
      (root, _) = os.path.splitext(gqFile)
      exportFile = root + ".bak"
    else :
      (root, _) = os.path.splitext(gqFile)
      exportFile = root + ".gq3"
    
    with open(exportFile, "w") as fileHandler :
      json.dump(output, fileHandler, indent = 2)

    currTime = datetime.datetime.now()
    if backup :
      print(f"[INFO] Saved backup to '{exportFile}'")
    else :
      currTime = datetime.datetime.now()
      print(f"[DEBUG] {noteCount} notes written in .pr file.")
      print(f"[INFO] Saved to '{exportFile}' at {currTime.strftime('%H:%M:%S')}")



  # ---------------------------------------------------------------------------
  # METHOD Score.getCursor()
  # ---------------------------------------------------------------------------
  def getCursor(self) :
    """
    Returns the value of the cursor at the current location in the score.
    """
    
    return self.cursor
  


  # ---------------------------------------------------------------------------
  # METHOD Score.cursorGoto()
  # ---------------------------------------------------------------------------
  def cursorGoto(self, value, force = False) -> None :
    """
    Sets the cursor to a specific location in the score.
    
    The cursor assignment is protected so that:
    - values outside the allowed range are clamped
    - values not aligned with the active hand are adjusted 

    Setting the cursor must be done with this function exclusively.
    Manually setting 'Score.cursor' is discouraged and might cause crashes.

    The parameter 'force' is set, the cursor location will be enforced regardless
    of the active hands.
    The need for this option is yet to be confirmed.
    """

    if (value < 0) :
      cursorNew = 0
    elif (value > self.cursorMax) :
      cursorNew = self.cursorMax
    else :
      cursorNew = value

    if force :
      self.cursor = cursorNew
    else :
      if (self.activeHands == SCORE_ACTIVE_HANDS_BOTH) :
        self.cursor = cursorNew
      elif (self.activeHands == SCORE_ACTIVE_HANDS_LEFT) :
        i = self._getIndexInCursorsLeft(cursorNew)
        self.cursor = self.cursorsLeft[i]
      elif (self.activeHands == SCORE_ACTIVE_HANDS_RIGHT) :
        p = self._getIndexInCursorsRight(cursorNew, force = True)
        self.cursor = self.cursorsRight[p]
      else :
        print("[ERROR] Score.cursorGoto(): unknown active hand specification (possible internal error)")

    

  # ---------------------------------------------------------------------------
  # METHOD Score.cursorBegin()
  # ---------------------------------------------------------------------------
  def cursorBegin(self) -> None :
    """
    Sets the cursor to the beginning of the score.

    If loop practice is active, it jumps to the beginning of the loop.
    """

    # If the loop mode is enabled: go to the beginning of the loop
    if (self.loopEnable and (self.cursor >= self.loopStart)) :
      self.cursorGoto(self.loopStart)
    else :
      self.cursorGoto(0)



  # ---------------------------------------------------------------------------
  # METHOD Score.cursorEnd()
  # ---------------------------------------------------------------------------
  def cursorEnd(self) -> None :
    """
    Sets the cursor to the end of the score.

    If loop practice is active, it jumps to the end of the loop.
    """
    
    # If the loop mode is enabled: go back to the end of the loop
    if (self.loopEnable and (self.cursor <= self.loopEnd)) :
      self.cursorGoto(self.loopEnd)
    else :
      self.cursorGoto(self.cursorMax)



  # ---------------------------------------------------------------------------
  # METHOD Score.cursorStep()
  # ---------------------------------------------------------------------------
  def cursorStep(self, delta: int) -> None :
    """
    Jumps in the score with a relative step (positive or negative)
    
    Jump is done by adding/subtracting the step to the cursor value.
    Jump value is protected, it cannot go out of bounds.
    
    NOTES
    - The jump ignores any loop settings i.e. it does not wrap if the step
      sets the cursor beyond the end of the loop.
      Use <cursorNext> instead to take the loop into account and wrap accordingly.
    - The cursor steps depending on the current hand practice mode. 
      In single hand practice mode, the jump will not be linear!
    """
    
    if (delta > 0) :

      # BOTH HAND PRACTICE
      if (self.activeHands == SCORE_ACTIVE_HANDS_BOTH) :
        self.cursorGoto(self.getCursor() + delta)

      # SINGLE HAND PRACTICE (LEFT)
      elif (self.activeHands == SCORE_ACTIVE_HANDS_LEFT) :
        index = self._getCursorsLeftPointer(self.getCursor())
        
        if (index == -1) :
          print("[INTERNAL ERROR] Left hand practice is active, but there is no event on the left hand at this cursor. Cannot browse from here!")
          
        if ((index + delta) <= (len(self.cursorsLeft)-1)) :
          self.cursor = self.cursorsLeft[index + delta]

      # SINGLE HAND PRACTICE (RIGHT)
      elif (self.activeHands == SCORE_ACTIVE_HANDS_RIGHT) :
        index = self._getCursorsRightPointer(self.getCursor())

        if (index == -1) :
          print("[INTERNAL ERROR] Right hand practice is active, but there is no event on the right hand at this cursor. Cannot browse from here!")
          
        if ((index + delta) <= (len(self.cursorsRight)-1)) :
          self.cursor = self.cursorsRight[index + delta]

      else :
        print("[INTERNAL ERROR] Score.cursorGoto: unknown active hand specification!")



    else :

      # BOTH HAND PRACTICE
      if (self.activeHands == SCORE_ACTIVE_HANDS_BOTH) :
        self.cursorGoto(self.getCursor() + delta)

      # SINGLE HAND PRACTICE (LEFT)
      elif (self.activeHands == SCORE_ACTIVE_HANDS_LEFT) :
        index = self._getCursorsLeftPointer(self.getCursor())
        
        if (index == -1) :
          print("[INTERNAL ERROR] Left hand practice is active, but there is no event on the left hand at this cursor. Cannot browse from here!")
          
        if ((index + delta) >= 0) :
          self.cursor = self.cursorsLeft[index + delta]

      # SINGLE HAND PRACTICE (RIGHT)
      elif (self.activeHands == SCORE_ACTIVE_HANDS_RIGHT) :
        index = self._getCursorsRightPointer(self.getCursor())

        if (index == -1) :
          print("[INTERNAL ERROR] Right hand practice is active, but there is no event on the right hand at this cursor. Cannot browse from here!")
          
        if (index + delta >= 0) :
          self.cursor = self.cursorsRight[index + delta]

      else :
        print("[INTERNAL ERROR] Score.cursorStep: unknown active hand specification!")



  # ---------------------------------------------------------------------------
  # METHOD Score.cursorNext()
  # ---------------------------------------------------------------------------
  def cursorNext(self) :
    """
    Jumps to the next cursor, wraps if looped practice is set.
    
    The function takes the active hands into account (both hands/single hand).
    In single hand practice mode, it jumps automatically to the 'correct' next
    cursor.
    
    Equivalent to 'cursorStep(1)', but includes the loop information.
    """

    if self.loopEnable :
      if ((self.cursor + 1) <= self.loopEnd) :
        self.cursorStep(1)
      else : 
        self.cursorGoto(self.loopStart)

    else :
      self.cursorStep(1)



  # ---------------------------------------------------------------------------
  # METHOD Score.cursorGotoClosestBookmark()
  # ---------------------------------------------------------------------------
  def cursorGotoClosestBookmark(self, direction : int) -> None :
    """
    Sets the cursor to the next closest bookmark.
    Does nothing if there are no bookmarks.

    Indicate the direction using the 'direction' argument:
    - any integer >= 0: goto the next bookmark
    - any integer < 0 : goto the previous bookmark

    In single hand practice, if the destination bookmark does not contain events
    for the current hand, then it will jump to the closest location of the
    requested bookmark.
    """
    
    if self.bookmarks :
      if (direction >= 0) :
        nextBookmarks = [x for x in self.bookmarks if (x > self.cursor)]
        if nextBookmarks :
          self.cursorGoto(nextBookmarks[0])
        else :
          print(f"[INFO] Last bookmark reached")
    
      else :
        prevBookmarks = [x for x in self.bookmarks if (x < self.cursor)]  
        if prevBookmarks :
          self.cursorGoto(prevBookmarks[-1])
        else :
          print(f"[INFO] First bookmark reached")



  # ---------------------------------------------------------------------------
  # METHOD Score.cursorIsBookmarked()
  # ---------------------------------------------------------------------------
  def cursorIsBookmarked(self) :
    """
    Returns True if the current position in the score is bookmarked.
    """

    return (self.cursor in self.bookmarks)
  


  # ---------------------------------------------------------------------------
  # METHOD Score._cursorAlignWithActiveHand()                         [PRIVATE]
  # ---------------------------------------------------------------------------
  def _cursorAlignWithActiveHand(self, hand, direction = 0) :
    """
    Sets the cursor to the closest location that is compatible with the requested
    hand practice mode.

    When the user changes the active hands from 'both hands' to 'single hand' practice,
    the cursor might become invalid.
    E.g. left hand practice requested, but there is no note played on the left hand at 
    the current cursor. 
    
    There are different strategies to find a candidate:
    - direction = 0: look for the closest compatible location (default behaviour)
    - direction > 0: look for a compatible location after the current location.
    - direction < 0: look for a compatible location before the current location.
    'compatible location' means here 'location where a note of the active hand is played'.
    
    The function does not change the 'Score.activeHands' attribute.
    """

    prevCursor = self.getCursor()

    self.cursorGoto(self.getCursor())

    delta = self.getCursor() - prevCursor
    if (delta > 0) :
      print(f"[DEBUG] Cursor changed because it was not aligned with the requested active hand (+{delta})")
    elif (delta < 0) :
      print(f"[DEBUG] Cursor changed because it was not aligned with the requested active hand ({delta})")
    else :
      pass

    # if (hand == NOTE_LEFT_HAND) :
      
    #   # TODO: guards needed here. There are case where the sets can be void.
    #   if (direction > 0) : 
    #     subList = [x >= self.cursor for x in self.cursorsLeft]
    #     self.cursor = subList[0]

    #   elif (direction < 0) : 
    #     subList = [x <= self.cursor for x in self.cursorsLeft]
    #     self.cursor = subList[-1]

    #   else :
    #     minIndex = 0
    #     dist = abs(self.cursor - self.cursorsLeft[0])
    #     for (index, cursorLeft) in enumerate(self.cursorsLeft[1:]) :
    #       if (abs(self.cursor - cursorLeft) < dist) :
    #         dist = abs(self.cursor - cursorLeft)
    #         minIndex = index+1          
    #     self.cursor = self.cursorsLeft[minIndex]


    # if (hand == NOTE_RIGHT_HAND) :
    
    #   if (direction > 0) : 
    #     subList = [x >= self.cursor for x in self.cursorsRight]
    #     self.cursor = subList[0]

    #   elif (direction < 0) : 
    #     subList = [x <= self.cursor for x in self.cursorsRight]
    #     self.cursor = subList[-1]

    #   else :
    #     minIndex = 0
    #     dist = abs(self.cursor - self.cursorsRight[0])
    #     for (index, cursorRight) in enumerate(self.cursorsRight[1:]) :
    #       if (abs(self.cursor - cursorRight) < dist) :
    #         dist = abs(self.cursor - cursorRight)
    #         minIndex = index+1
    #     self.cursor = self.cursorsRight[minIndex]
      
    # delta = self.getCursor() - prevCursor
    # if (delta > 0) :
    #   print(f"[DEBUG] Cursor changed because it was not aligned with the requested active hand (+{delta})")
    # elif (delta < 0) :
    #   print(f"[DEBUG] Cursor changed because it was not aligned with the requested active hand ({delta})")
    # else :
    #   pass



  # ---------------------------------------------------------------------------
  # METHOD Score.loopSetStart()
  # ---------------------------------------------------------------------------
  def loopSetStart(self) :
    """
    Sets the beginning of the loop at the current cursor.
    
    If the end of the loop is already defined, this function also enables
    the loop practice mode.
    """
    
    # Loop end is not yet defined
    if (self.loopEnd == -1) :
      self.loopStart = self.getCursor()
      print(f"[INFO] Start of loop set at {self.loopStart+1}")

    else :
      if (self.getCursor() < self.loopEnd) :
        self.loopStart = self.getCursor()
        self.loopEnable = True
        print(f"[INFO] Loop is now set: start = {self.loopStart+1} / end = {self.loopEnd+1}")



  # ---------------------------------------------------------------------------
  # METHOD Score.loopSetEnd()
  # ---------------------------------------------------------------------------
  def loopSetEnd(self) :
    """
    Sets the end of the loop at the current cursor.
    
    If the beginning of the loop is already defined, this function also enables
    the loop practice mode.
    """
    
    # Loop start is not yet defined
    if (self.loopStart == -1) :
      self.loopEnd = self.getCursor()
      print(f"[INFO] End of loop set at {self.loopEnd+1}")

    else :
      if (self.getCursor() > self.loopStart) :
        self.loopEnd = self.getCursor()
        self.loopEnable = True
        self.cursor = self.loopStart
        print(f"[INFO] Loop is now set: start = {self.loopStart+1} / end = {self.loopEnd+1}")
  


  # ---------------------------------------------------------------------------
  # METHOD Score.loopClear()
  # ---------------------------------------------------------------------------
  def loopClear(self) :
    """
    Clears the loop specification, disables the loop practice mode.
    """
    self.loopStart = -1
    self.loopEnd = -1
    self.loopEnable = False
    print("[INFO] Loop cleared.")



  # ---------------------------------------------------------------------------
  # METHOD Score.bookmarkToggle()
  # ---------------------------------------------------------------------------
  def bookmarkToggle(self) :
    """
    Adds/removes a bookmark at the current cursor.
    """

    # Is it an existing bookmark?
    if self.cursor in self.bookmarks :
      self.bookmarks = [x for x in self.bookmarks if (x != self.cursor)]
      print(f"[INFO] Bookmark removed at cursor {self.getCursor()+1}")
    
    # New bookmark
    else :
      print(f"[INFO] Bookmark added at cursor {self.getCursor()+1}")
      self.bookmarks.append(self.cursor)
      self.bookmarks.sort()

    self.hasUnsavedChanges = True



  
  # ---------------------------------------------------------------------------
  # METHOD Score.getBookmarkIndex()
  # ---------------------------------------------------------------------------
  def getBookmarkIndex(self) :
    """
    Returns the index (i.e. the bookmark number) of the current cursor.
    If the current cursor is not bookmarked, it returns -1.

    Note: the bookmark index is returned in 'friendly' indexing i.e. starting 
    from 1.
    """
    
    if self.cursorIsBookmarked() :      
      return self.bookmarks.index(self.getCursor()) + 1
    else :
      return -1
  


  # ---------------------------------------------------------------------------
  # METHOD Score._getIndexInCursorsLeft()                             [PRIVATE]
  # ---------------------------------------------------------------------------
  def _getIndexInCursorsLeft(self, cursorReq, force = False) -> int :
    """
    Returns the index 'i' such that 'Score.cursorsLeft[i]' is equal to the 
    requested value 'cursorReq'.

    By default, it returns the index that gives the closest cursor to the 
    target value, in case no exact match can be found.
    The closest match can be either before or after the target cursor.

    When force = True, it returns -1 when there is no exact solution.
    """
    
    # An exact solution exists 
    if (cursorReq in self.cursorsLeft) :
      return self.cursorsLeft.index(cursorReq)
    
    # No exact solution
    else :
      if force :
        return -1
      else :
        minDist = abs(cursorReq - self.cursorsLeft[0])
        minIndex = 0
        for (i, cursorLeft) in enumerate(self.cursorsLeft) :
          if (abs(cursorReq - cursorLeft) < minDist) :
            minDist = abs(cursorReq - cursorLeft)
            minIndex = i

        print(f"[DEBUG] Requested cursor: {cursorReq}, closest: {minIndex}")
        return minIndex
    


  # ---------------------------------------------------------------------------
  # METHOD Score._getIndexInCursorsRight()                            [PRIVATE]
  # ---------------------------------------------------------------------------
  def _getIndexInCursorsRight(self, cursorReq, force = False) -> int :
    """
    Returns the index 'i' such that 'Score.cursorsRight[i]' is equal to the 
    requested value 'cursorReq'.

    By default, it returns the index that gives the closest cursor to the 
    target value, in case no exact match can be found.
    The closest match can be either before or after the target cursor.

    When force = True, it returns -1 when there is no exact solution.
    """
    
    # An exact solution exists 
    if (cursorReq in self.cursorsRight) :
      return self.cursorsRight.index(cursorReq)
    
    # No exact solution
    else :
      if force :
        return -1
      else :
        minDist = abs(cursorReq - self.cursorsRight[0])
        minIndex = 0
        for (i, cursorRight) in enumerate(self.cursorsRight) :
          if (abs(cursorReq - cursorRight) < minDist) :
            minDist = abs(cursorReq - cursorRight)
            minIndex = i

        print(f"[DEBUG] Requested cursor: {cursorReq}, closest: {minIndex}")
        return minIndex



  # ---------------------------------------------------------------------------
  # METHOD Score._buildCursorsLR()                                    [PRIVATE]
  # ---------------------------------------------------------------------------
  def _buildCursorsLR(self) :
    """
    Populates the fields 'Score.cursorsLeft' and 'Score.cursorsRight' from the 
    list of timecodes of all note on events ('Score.noteOnTimeCodes' dictionary).
    
    This method is usually called after loading a MIDI or even .gq file, since 
    the information in these fields is redundant and does not bring added
    value to get stored in the file.
    """
    
    self.cursorsLeft = []; self.cursorsRight = []

    for (index, timecode) in enumerate(self.noteOnTimecodes["LR"]) :
      unaffected = True
      if (timecode in self.noteOnTimecodes["L"]) :
        self.cursorsLeft.append(index)
        unaffected = False

      if (timecode in self.noteOnTimecodes["R"]) :
        self.cursorsRight.append(index)
        unaffected = False
      
      if unaffected :
        print("[INTERNAL ERROR] Score._buildCursorsLR: something odd happened!")



  # ---------------------------------------------------------------------------
  # METHOD Score.setActiveHands()
  # ---------------------------------------------------------------------------
  def setActiveHands(self, left:bool, right:bool) -> None :
    """
    Sets the hands i.e. the active channels of the score.
    
    Since gangQin handles piano scores only, it corresponds to the left or 
    right hand channel. 
    
    The active hand attributes restrains the set of possible value the 'cursor'
    attribute might take.

    When the left channel alone is active, the cursor can only take a value
    among the ones where a note starts on the left hand.
    Same for the right channel.
  
    Single active channels can result in jumps in the cursor values when calling 
    'Score.cursorStep(+/-1)' or 'Score.cursorNext()'. This is perfectly normal.
    When both hands are active, the cursor always evolves linearly (no jumps)

    NOTES
    - at least one channel must be active
    - changing the active hands attribute is disabled during looped practice
    """
    
    if not(self.loopEnable) :
      if (not(left) and not(right)) :
        print("[WARNING] Score.setActiveHands(): at least one hand must be active.")
      elif left and not(right) :
        self.activeHands = SCORE_ACTIVE_HANDS_LEFT
      elif not(left) and right :
        self.activeHands = SCORE_ACTIVE_HANDS_RIGHT
      else :
        self.activeHands = SCORE_ACTIVE_HANDS_BOTH
    
      self._cursorAlignWithActiveHand()
      self._resetCache()

    else :
      print("[INFO] Score.setActiveHands(): changing the active hand is disabled during looped practice.")



  # ---------------------------------------------------------------------------
  # METHOD Score.getTimecode()
  # ---------------------------------------------------------------------------
  def getTimecode(self) :
    """
    Returns the MIDI timecode of the current location in the score.
    """
    
    # TODO: incorrect for single hand practice mode
    return self.noteOnTimecodes["LR"][self.getCursor()]



  # ---------------------------------------------------------------------------
  # METHOD Score.getTeacherNotes()
  # ---------------------------------------------------------------------------
  def getTeacherNotes(self) :
    """
    Returns the list of all notes that must be pressed at the current position
    in the score.
    
    Only notes pressed at this cursor are returned.
    Sustained notes (notes that were pressed before and held up to the current 
    cursor) are not included in the list.

    TODO: confirm that sustained notes are not returned
    """
    
    # Cursor hasn't changed since last request: return the cache
    if (self.getCursor() == self.teacherNotesCursor) :
      pass
    
    # Otherwise: regenerate the cache
    else :
      self._calculateTeacherNotes()
      self.teacherNotesCursor = self.getCursor()

    return self.teacherNotes



  # ---------------------------------------------------------------------------
  # METHOD Score._updateTeacherNotes()
  # ---------------------------------------------------------------------------
  def _calculateTeacherNotes(self) :
    """
    Builds the 'teacherNotes' attribute i.e. the list of notes that must be 
    played at the current location in the score.

    'Score.teacherNotes' contains a list of Note objects with appropriate
    properties for the rendering and arbitration.
    """
    
    # Reset the play attributes of the previous notes before deleting them.
    # Note attributes are used for the display and the arbiter.
    # for noteObj in self.teacherNotes :
    #   noteObj.visible = True
    #   noteObj.sustained = False
    #   noteObj.inactive = False

    # Reset the cache
    self.teacherNotes = []
    
    # Loop on all notes in the score
    for channel in range(SCORE_N_STAFF) :
      for pitch in MIDI_CODE_GRAND_PIANO_RANGE :
        for noteObj in self.pianoRoll[channel][pitch] :

          N = note.Note(noteObj.pitch)
          N.startTime = noteObj.startTime
          N.stopTime  = noteObj.stopTime
          N.hand      = noteObj.hand
          N.finger    = noteObj.finger
          N.voice     = noteObj.voice
          N.velocity  = noteObj.velocity
          N.sustained = False
          N.inactive  = False

          # CASE 1: a note is pressed at this timecode
          if (noteObj.startTime == self.getTimecode()) :
            
            # SINGLE HAND PRACTICE
            # Adds the notes with their "inactive" property to "True" 
            # so that it is displayed with the appropriate color.
            if (self.activeHands == SCORE_ACTIVE_HANDS_BOTH) :
              N.inactive = False
              self.teacherNotes.append(N)
            
            elif (self.activeHands == SCORE_ACTIVE_HANDS_LEFT) :
              if (channel != NOTE_LEFT_HAND) : 
                N.inactive = True
                self.teacherNotes.append(N)

            elif (self.activeHands == SCORE_ACTIVE_HANDS_RIGHT) :
              if (channel != NOTE_RIGHT_HAND) :
                N.inactive = True
                self.teacherNotes.append(N)

          # CASE 2: a note is held at this timecode
          elif ((self.getTimecode() > noteObj.startTime) and (self.getTimecode() <= noteObj.stopTime)) :
            N.sustained = True
            self.teacherNotes.append(N)

          # CASE 3: a note is out of the current window
          else :
            pass

    if (len(self.teacherNotes) == 0) :
      print(f"[WARNING] Corrupted database: timecode is listed (t = {self.getTimecode()}), but no note was found starting at that moment.")




  # ---------------------------------------------------------------------------
  # METHOD Score._resetCache()                                        [PRIVATE]
  # ---------------------------------------------------------------------------
  def _resetCache(self) :
    """
    Resets the teacher notes cache.
    Teacher notes are determined once per cursor. Cacheing avoids doing this 
    task multiple times when the cursor hasn't changed.
    """
    
    self.cachedCursor = -1



  # ---------------------------------------------------------------------------
  # METHOD Score.getUpcomingNotes()
  # ---------------------------------------------------------------------------
  def getUpcomingNotes(self) :
    """
    Builds the list of the notes about to come after the current cursor.

    NOTES
    The list contains a copy of the notes.
    Feel free to edit their properties. It will not affect the actual notes of 
    the score.
    """
    
    upcomingNotes = []

    # Lookahead feature: show also the upcoming notes 
    # to help with the hand placement.
    
    # STEP 1: get the N notes that will be triggered 
    # after the current cursor
    # These notes shall be taken within a certain timecode 
    # limit from the current location.
    
    # Don't show the same pitch twice
    activePitches = [x.pitch for x in self.cachedTeacherNotes]
    
    for n in range(1, (self.lookAheadDistance+1)) :
      if ((self.getCursor() + n) < self.cursorMax) :
        for pitch in MIDI_CODE_GRAND_PIANO_RANGE :
          for (staffIndex, _) in enumerate(self.pianoRoll) :
            for noteObj in self.pianoRoll[staffIndex][pitch] :

              # Detect a note pressed at this timecode
              if (noteObj.startTime == (self.noteOnTimecodes["LR"][self.cursor + n])) :
                if not(noteObj.pitch in activePitches) :
                  noteCopy = copy.deepcopy(noteObj)
                  noteCopy.upcoming = True
                  noteCopy.upcomingDistance = n
                  upcomingNotes.append(noteCopy)
                  activePitches.append(noteCopy.pitch)


    return upcomingNotes

    # STEP 2: edit their lookahead property to tell Keyboard
    # that they should be displayed in a certain way.

    # TODO: instead of showing the notes ahead in a certain window,
    # maybe a sort of "slur" function should be added so that 
    # only the notes in the slur are shown in the lookahead.



  # ---------------------------------------------------------------------------
  # METHOD Score.getLookaheadNotes()
  # ---------------------------------------------------------------------------
  def getLookaheadNotes(self) :
    """
    DEPRECATED
    """
    
    if (self.cachedCursor == self.cursor) :
      return self.cachedTeacherNotes
    
    else :
      self._updateLookaheadNotes()
      self.cachedCursor = self.cursor
      self.cachedTeacherNotes = self.teacherNotes
      
      return self.teacherNotes



  # ---------------------------------------------------------------------------
  # METHOD Score._updateLookaheadNotes()
  # ---------------------------------------------------------------------------
  def _updateLookaheadNotes(self) :
    """
    DEPRECATED
    """
    
    print("Score._updateLookaheadNotes is deprecated.")



  # ---------------------------------------------------------------------------
  # METHOD Score.search(noteList, direction)
  # ---------------------------------------------------------------------------
  def search(self, noteList, direction = 1) :
    """
    Finds the next location in the score where all the query notes appear 
    simultaneously.
    Sets the cursor to the first matching location.
    
    Direction of search (before or after the current location) can be specified.
    
    TODO: does it include sustained notes?
    """

    if (direction >= 0) :
      if (self.activeHands == SCORE_ACTIVE_HANDS_RIGHT) :
        timecodeSearchField = [x > self.cursor for x in self.cursorsRight]
      elif (self.activeHands == SCORE_ACTIVE_HANDS_LEFT) :
        timecodeSearchField = [x > self.cursor for x in self.cursorsRight]
      else :
        # TODO: check the boundaries
        timecodeSearchField = [x for x in range(self.cursor+1, self.length)]
    
    else :
      if (self.activeHands == SCORE_ACTIVE_HANDS_RIGHT) :
        timecodeSearchField = [x < self.cursor for x in self.cursorsRight]
      elif (self.activeHands == SCORE_ACTIVE_HANDS_LEFT) :
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
            if (noteObj.startTime == self.noteOnTimecodes["LR"][cursorTry]) :
              foundPitch.append(noteObj.pitch)

      if (len(foundPitch) > 0) :
        isInList = True
        
        for x in pitchList :
          if not(x in foundPitch) :
            isInList = False
            break
        
        if isInList :
          print(f"[INFO] Find: current input was found at cursor = {cursorTry}")
          found = True
          foundCursor = cursorTry
          break
      
    if found :
      # We must prevent the arbiter from taking this as a valid input
      # and move on to the next cursor
      # All notes must be released to exit the 'search' mode.
      self.cursor = foundCursor
      arbiterSuspendReq = True
      arbiterPitchListHold = pitchList.copy()
      return (arbiterSuspendReq, arbiterPitchListHold)
    
    else :
      print("[INFO] Could not find the current MIDI notes in the score!")
      return (False, [])



  # ---------------------------------------------------------------------------
  # METHOD Score.noteHandSwap()
  # ---------------------------------------------------------------------------
  def noteHandSwap(self, noteObj) -> None :
    """
    Changes the hand assigned to the note passed as argument and updates the 
    Score database accordingly.
    
    If the note is assigned to the left hand, it will now be assigned to the right
    hand and vice versa.
    
    NOTES
    Assigning a note from the left to the right hand has more impact than just 
    editing the 'hand' property of the note object. 
    Among others, the list of cursors must be edited too.
    """
    
    if (noteObj.hand == NOTE_LEFT_HAND) :
      
      noteObj.hand = NOTE_RIGHT_HAND

      if (noteObj.startTime in self.noteOnTimecodes["L"]) :
        
        # Note: 'remove' only deletes one occurrence of the element.
        self.noteOnTimecodes["L"].remove(noteObj.startTime)
        self.noteOnTimecodes["R"].append(noteObj.startTime)
        self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
        
        # Note: 'self.noteOnTimecodes["LR_full"]' remains invariant in the process
        # Note: 'self.noteOnTimecodes["LR"]' remains invariant in the process

      else :
        print("[INTERNAL ERROR] Score.toggleNoteHand: database is not consistent.")
        print("The timecode of the note you are trying to remove is not in the list of timecodes!")
        exit()

    elif (noteObj.hand == NOTE_RIGHT_HAND) :
      
      noteObj.hand = NOTE_LEFT_HAND

      if (noteObj.startTime in self.noteOnTimecodes["R"]) :
        
        # Note: 'remove' only deletes one occurrence of the element.
        self.noteOnTimecodes["R"].remove(noteObj.startTime)
        self.noteOnTimecodes["L"].append(noteObj.startTime)
        self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
        
        # Note: 'self.noteOnTimecodes["LR_full"]' remains invariant in the process
        # Note: 'self.noteOnTimecodes["LR"]' remains invariant in the process

      else :
        print("[INTERNAL ERROR] Score.toggleNoteHand: database is not consistent.")
        print("The timecode of the note you are trying to remove is not in the list of timecodes!")
        exit()

    else :
      print("[INTERNAL ERROR] Score.toggleNoteHand: unknown active hand specification!")
      exit()

    # Rebuild the lists of cursors
    self._buildCursorsLR()

    lengthLR = len(self.noteOnTimecodes["LR_full"])
    lengthL = len(self.noteOnTimecodes["L"]); lengthR = len(self.noteOnTimecodes["R"])
    
    # Consistency check
    # TODO: replace with error try/catch, otherwise there is a risk of losing all progression
    # in case assert fails
    assert(lengthLR == (lengthL + lengthR))
    


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
  # METHOD Score.guessScale()
  # ---------------------------------------------------------------------------
  def guessScale(self, startCursor, span = -1) :
    """
    Tries to determine the key a section is in based on statistics. 

    Function is not implemented yet.
    """
    
    pass



  # ---------------------------------------------------------------------------
  # METHOD: Score.setWeakArbitration(cursor)
  # ---------------------------------------------------------------------------
  def setWeakArbitration(self) :
    """
    Sends a weak arbitration request starting/ending at the current cursor.
    
    'Weak arbitration' mode is when the arbiter, for a specific section, 
    waits for the notes in the section to be played but does care about their
    sequencing or timing anymore. In short, notes can be played in any order
    you like in this section.

    Call this function to declare the boundaries of a section with weak 
    arbitration. 
    """

    print("[WARNING] 'setWeakArbitration' is TODO")



  # ---------------------------------------------------------------------------
  # METHOD: Score.render()
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Renders the widget on screen.
    This function is called at every frame of the top level application.
    """

    text.showCursor(self.top.screen, self.getCursor(), self.length)
    text.showBookmark(self.top.screen, self.getBookmarkIndex())
    text.showActiveHands(self.top.screen, self.activeHands)






  # ---------------------------------------------------------------------------
  # METHOD Score._onKeyEvent()                                        [PRIVATE]
  # ---------------------------------------------------------------------------
  def _onKeyEvent(self, key, type, modifier = "") :
    """
    Function triggered by a keypress.
    """
    
    if (type == pygame.KEYDOWN) :
      
      # Simple keypresses (no modifiers)
      if (modifier == "") :
        
        # B: toggle bookmark
        if (key == pygame.K_b) :
          self.bookmarkToggle()

        


# ---------------------------------------------------------------------------
# NOTE_TRACKER CLASS (helper class for the MIDI import)
# ---------------------------------------------------------------------------
class NoteTracker :

  def __init__(self) :
    self._pitch = {
      SCORE_RIGHT_HAND_TRACK_ID : [],
      SCORE_LEFT_HAND_TRACK_ID  : []
    }
    self._dbIndex = {
      SCORE_RIGHT_HAND_TRACK_ID : [],
      SCORE_LEFT_HAND_TRACK_ID  : []
    }



  def begin(self, pitch, channel, index) :
    """
    Declares a note starting in the score.
    """

    if (pitch in self._pitch[channel]) :
      print("[WARNING] NoteTracker.begin(): a note with this pitch is already active in the channel")
    else :
      self._pitch[channel].append(pitch)
      self._dbIndex[channel].append(index)



  def end(self, pitch, channel) :
    """
    Declares a note ending in the score.
    """

    if not(pitch in self._pitch[channel]) :
      print("[WARNING] NoteTracker.end(): trying to terminate a note already terminated or a note that never started.")
    else :
      i = self._pitch[channel].index(pitch)
      del self._pitch[channel][i]
      del self._dbIndex[channel][i]



  def isActive(self, pitch, channel) :
    """
    Checks if a note is active in the channel. 
    """

    return (pitch in self._pitch[channel])
  


  def getIndex(self, pitch, channel) :
    """
    Returns the database index of an active note.
    """

    if not(pitch in self._pitch[channel]) :
      print("[WARNING] NoteTracker.getIndex(): the active note could not be found.")
      return -1
    else :
      i = self._pitch[channel].index(pitch)
      return self._dbIndex[channel][i]



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  print("[INFO] Library 'Score' called as main: running unit tests...")

  # *****************
  # TEST: MIDI IMPORT
  # *****************
  # Try to import all MIDI files available
  midiFiles = [SONG_PATH + "/" + f for f in os.listdir(SONG_PATH) if f.endswith(".mid") and os.path.isfile(os.path.join(SONG_PATH, f))]
  for file in midiFiles :
    scoreNew = Score(None)
    scoreNew.loadMIDIFile(file, ['R', 'L'])


  # *****************************
  # TEST: DATA LOSS IN GQ3 FORMAT
  # *****************************
  # Import and then export a .gq file without any modifications 
  # (under a different name)
  # Compare the input and output file, make sure no information is lost in the 
  # process. 
  songFile = SONG_PATH + "/" + "Rachmaninoff_Piano_Concerto_No2_Op18.pr"
  scoreRef = Score(None)
  scoreRef.loadPRFile(songFile)
  scoreRef.exportToPRFile(songFile, backup = True)

  scoreNew = Score(None)
  scoreNew.loadPRFile(songFile)

  # Now compare attributes between 'scoreNew' and 'scoreOld'
  # No major difference should show, especially in the internal score 
  # database (notes, fingersatz, etc.)
  # ...
  # This section is TODO.
  # ...






  # Experiments with GQ3 file format (gangQin v.3)
  songFile = SONG_PATH + "/" + "Medtner_-_Forgotten Melodies_Op_38_II_Danza_graziosa_rev0.mid"
  score = Score(None)
  score.loadMIDIFile(songFile, ['R', 'L'])
  score.exportToGQ3File(SONG_PATH + "/" + "Medtner0.gq3")

  songFile = SONG_PATH + "/" + "Medtner_-_Forgotten Melodies_Op_38_II_Danza_graziosa_rev1.mid"
  score = Score(None)
  score.loadMIDIFile(songFile, ['R', 'L'])
  score.exportToGQ3File(SONG_PATH + "/" + "Medtner1.gq3")


  songFile = SONG_PATH + "/" + "Rachmaninoff_Piano_Concerto_No2_Op18.pr"
  score = Score(None)
  score.loadPRFile(songFile)
  score.exportToGQ3File(songFile)


