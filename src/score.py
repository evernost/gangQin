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
# Project libraries
from src.commons import *
import src.note as note
import src.widgets.widget as widget
import src.text as text

# Standard libraries
import copy       # mostly used in deprecated functions
import datetime
import json       # for .gq3 file database import/export
import mido       # for MIDI file manipulation
import os         # for filename manipulation
import pygame
import time



# =============================================================================
# CONSTANTS
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
   
    self.name = "score"

    # Song (populated after a loadMidiFile / loadPrFile / loadGq3File)
    self.songFile = ""

    # Pointer in the score
    self.cursor       = 0         # Range: 0 ... Score.cursorMax
    self.cursorsLeft  = []
    self.cursorsRight = []
    self.bookmarks    = []
    self.cursorMax    = 0
    self.length       = 0

    # Internal representation
    self.noteList = []
    self.pianoRoll = [[[] for _ in range(128)] for _ in range(SCORE_N_STAFF)]   # Cursed old school format (DEPRECATED)
    self.noteOnTimecodes = {
      "L"       : [],   # Timecodes for the left hand keypresses
      "R"       : [],   # Timecodes for the right hand keypresses
      "LR"      : [],   # Timecodes for the left and right hand keypresses (merged, no duplicates)
      "LR_full" : []    # Timecodes for the left and right hand keypresses (merged, with duplicates)
    }

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
  # METHOD Score.loadMidiFile_DEPRECATED()
  # ---------------------------------------------------------------------------
  def loadMidiFile_DEPRECATED(self, midiFile: str, midiTracks: list[str]) -> None :
    """
    *******
    WARNING: this version generates the old school score database from 
    a MIDI file.
    There is no use for this function anymore. DO NOT USE IT.
    
    This function will be removed in a future release.
    *******
    
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
  # METHOD Score.loadMidiFile()
  # ---------------------------------------------------------------------------
  def loadMidiFile(self, midiFile: str, midiTracks: list[str]) -> None :
    """
    Loads and initialises the Score object from a MIDI file.

    'midiFile' must be the full path to the file with its extension.
    EXAMPLE: midiFile = './songs/Chopin_Etude_Op_10_No_1.mid'

    'midiTracks' is a list of strings containing as many elements as there
    are tracks in the MIDI file.
    Indices containing the string 'L' and/or 'R' indicate the tracks 
    that will be read and assigns them to the corresponding track.
    EXAMPLE: midiTracks = ['R', 'L', '', ''] -> read track 0 and 1.
    """

    self.songFile = midiFile

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
            
            # Create and edit the note             
            N = note.Note(pitch)
            N.hand      = trackID
            N.dbIndex   = insertIndex
            N.velocity  = msg.velocity
            insertIndex += 1
            
            # Register the note in the database
            self.noteList.append(N)
            noteCount += 1
            
            # Start the tracking on this note
            noteTracker.keyPress(N, currTime)

            # Register this timecode
            self.noteOnTimecodes["LR_full"].append(currTime)
            if (trackID == SCORE_LEFT_HAND_TRACK_ID)  : self.noteOnTimecodes["L"].append(currTime)
            if (trackID == SCORE_RIGHT_HAND_TRACK_ID) : self.noteOnTimecodes["R"].append(currTime)
            
          # MIDI EVENT: key release
          elif ((msg.type == "note_off") or ((msg.type == "note_on") and (msg.velocity == 0))) : 
            noteTracker.keyRelease(pitch, trackID, currTime)

          # MIDI EVENT: time signature change
          elif (msg.type == 'time_signature') :
            print(f"- read time signature: {msg.numerator}/{msg.denominator} (timecode = {currTime})")
            #eventTime = mido.tick2second(current_time, ticks_per_beat, tempo) for a display in seconds

          # MIDI EVENT: key signature change
          elif (msg.type == 'key_signature') :
            print(f"- read key signature: {msg.key} (timecode = {currTime})")

          # MIDI EVENT: tempo change (IGNORED: too verbose)
          elif (msg.type == 'set_tempo') :
            #print(f"- read new tempo: {msg.tempo} (timecode = {currTime})")
            currTempo = msg.tempo

          # MIDI EVENT: control change (IGNORED: no use for it)
          elif (msg.type == 'control_change') :
            pass

          # MIDI EVENT: program change (IGNORED: no use for it)
          elif (msg.type == 'program_change') :
            pass
      
      # The track is not assigned to any hand
      else :
        pass
    
    # MIDI read done: inspect the note tracking before closing
    noteTracker.checkOnExit()

    # Tidy up:
    # - sort the timecodes by ascending values
    # - remove duplicate entries
    self.noteOnTimecodes["L"].sort() 
    self.noteOnTimecodes["R"].sort()
    self.noteOnTimecodes["LR_full"].sort()

    self.noteOnTimecodes["LR"] = list(set(self.noteOnTimecodes["LR_full"]))
    self.noteOnTimecodes["LR"].sort()

    # Build the 'cursorsLeft' and 'cursorsRight' attributes
    self._buildCursorsLR()

    # Estimate average note duration (needed for the pianoroll display)
    #self.avgNoteDuration = noteDuration/noteCount
    self.avgNoteDuration = 100
    
    self.length = len(self.noteOnTimecodes["LR"])
    self.cursorMax = self.length-1
    
    print(f"- score length: {self.length} steps")

    stopTime = time.time()
    print(f"[INFO] Loading time: {stopTime-startTime:.2f}s")
    


  # ---------------------------------------------------------------------------
  # METHOD Score.loadPrFile()
  # ---------------------------------------------------------------------------
  def loadPrFile(self, prFile: str) -> None :
    """

    *******
    WARNING: '.pr' files have been deprecated since gangQin version 3.
    Use this function to upgrade from '.pr' to '.gq3' format only.
    Next versions use 'Score.loadGQ3File()' instead.
    *******

    Loads and initialises the Score object from a '.pr' file.

    'prFile' must be the full path to the file.

    Unlike MIDI files, .pr files store all the user annotated information 
    about the score (bookmarks, fingersatz, tempo, etc.)
    """
    
    self.songFile = prFile

    # For statistics
    startTime = time.time()
    
    # Open the file as a JSON
    with open(prFile, "r") as fileHandler :
      importDict = json.load(fileHandler)

    # Read the revision
    rev = importDict["revision"][1:].split(".")
    revMajor = int(rev[0])
    revMinor = int(rev[1])
    print(f"[WARNING] .PR FILES WILL BE DEPRECATED IN FUTURE RELEASES.")
    print(f"[INFO] Reading gangQin v{revMajor}.{revMinor} file...")
    
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
    # Initialise attributes
    self.noteList = []
    self.noteOnTimecodes = {
      "L"       : [],
      "R"       : [],
      "LR"      : [],
      "LR_full" : []
    }
    
    noteCount = 0
    
    #self.pianoRoll = [[[] for _ in range(128)] for _ in range(SCORE_N_STAFF)]
    #self.noteOnTimecodes = {"L": [], "R": [], "LR": [], "LR_full": []}
    noteTracker = NoteTracker()
    #noteCount = 0
    noteListTmp = []
    masteredNoteCount = 0
    for noteAsDict in importDict["pianoRoll"] :

      # Create and edit the note             
      N = note.Note(noteAsDict["pitch"])
      N.hand      = noteAsDict["hand"]
      N.finger    = noteAsDict["finger"]
      N.voice     = noteAsDict["voice"]
      N.velocity  = 64                      # Note velocity was introduced in gangQin v3; '.pr' files don't have it.
      N.startTime = noteAsDict["startTime"]
      N.stopTime  = noteAsDict["stopTime"]
      N.dbIndex   = -1
      N.id        = noteCount
      
      if (N.finger != 0) :
        masteredNoteCount += 1
      
      # Register the note in the database
      noteListTmp.append(N)
      noteCount += 1
      
      # Register this timecode
      self.noteOnTimecodes["LR_full"].append(noteAsDict["startTime"])
      if (noteAsDict["hand"] == SCORE_LEFT_HAND_TRACK_ID)  : self.noteOnTimecodes["L"].append(noteAsDict["startTime"])
      if (noteAsDict["hand"] == SCORE_RIGHT_HAND_TRACK_ID) : self.noteOnTimecodes["R"].append(noteAsDict["startTime"])

    # Sort notes by ascending keypress timecode
    self.noteList = sorted(noteListTmp, key = lambda noteObj: noteObj.startTime)

    # TODO: 
    # At the time, MIDI file import had a very different strategy
    # to deal with multiple keypresses on a given note without prior release.
    # So the following flows:
    # - MIDI import -> '.pr' generation  -> '.pr' import
    # - MIDI import -> '.gq3' generation -> '.gq3' import
    # might produce a slightly different internal database.
    # In particular, the notes will not have the same release timecode.
    #
    # This is can cause an issue in this scenario:
    # 1. The user has a '.pr' file with many metadata
    # 2. The user upgrades to gangQin v3
    # 3. '.pr' file is converted to '.gq3'
    # 4. Original MIDI file got upgraded
    # 5. The user wants to do an incremental upgrade of the .'gq3' from the MIDI file
    # It will be very hard to diff the old '.gq3' with the new '.gq3'.
    #
    # Some processing needs to be done to minimise the differences
    # between the two.

    # Start the tracking on this note
    # for N in self.noteList :
    #   noteTracker.keyPress(N, noteAsDict["startTime"])

    # Tidy up:
    # - sort the timecodes by ascending values
    # - remove duplicate entries
    self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
    self.noteOnTimecodes["LR_full"].sort()

    self.noteOnTimecodes["LR"] = set(self.noteOnTimecodes["LR_full"])
    self.noteOnTimecodes["LR"] = list(self.noteOnTimecodes["LR"])
    self.noteOnTimecodes["LR"].sort()

    # Build "cursorsLeft" and "cursorsRight" arrays.
    # Each one is a list of all cursors where something has to be played 
    # either on the left (cursorsLeft) or right hand (cursorsRight)
    self._buildCursorsLR()

    self.length = len(self.noteOnTimecodes["LR"])
    self.cursorMax = self.length-1

    stopTime = time.time()
    print(f"[INFO] Loading time: {stopTime-startTime:.2f}s")
    print(f"[INFO] {noteCount} notes read from .pr file.")
    print(f"[INFO] Score length: {self.length} steps")
    
    print(f"[INFO] Progress: {masteredNoteCount}/{noteCount} ({100*masteredNoteCount/noteCount:.1f}%)")



  # ---------------------------------------------------------------------------
  # METHOD Score.loadGq3File()
  # ---------------------------------------------------------------------------
  def loadGq3File(self, gq3File: str) -> None :
    """
    Loads and initialises the Score object from a '.gq3' file (gangQin v3 file)

    'gq3File' must be the full path to the file.

    Unlike MIDI files, .pr files store all the user annotated information 
    about the score (bookmarks, fingersatz, tempo, etc.)
    """
    
    self.songFile = gq3File

    # For statistics
    startTime = time.time()
    
    # Open the file as a JSON
    with open(gq3File, "r") as fileHandler :
      importDict = json.load(fileHandler)

    # Fallback dictionary in case some fields do not exist.
    safeDict = {
      "appVersion"                : "v0.0",
      "cursor"                    : 0,
      "bookmarks"                 : [],
      "noteList"                  : [],
      "timecodeList"              : [],
      "tempoSections"             : [(1, 120)],
      "weakArbitrationSections"   : []
    }

    # Read the revision
    rev = importDict["appVersion"][1:].split(".")
    revMajor = int(rev[0])
    revMinor = int(rev[1])
    if (revMajor == 0) :
      print("[INFO] Importing dinosaur .pr file (versions v0.X) has been deprecated since gangQin v1.6")
      exit()

    # Populate fields with the JSON
    for currKey in safeDict :
      if currKey in importDict :
        safeDict[currKey] = importDict[currKey]

    # Initialize the object
    self.cursor     = safeDict["cursor"]
    self.bookmarks  = safeDict["bookmarks"]
    
    if (len(safeDict["noteList"]) != len(safeDict["timecodeList"])) :
      print("[ERROR] Lengths do not match.")
      exit()
    
    noteCount = 0
    annotatedNoteCount = 0
    self.noteOnTimecodes = {"L": [], "R": [], "LR": [], "LR_full": []}
    self.noteList = []
    for (i, noteAsDict) in enumerate(safeDict["noteList"]) :
      N = note.Note(noteAsDict["pitch"])
      N.hand      = noteAsDict["hand"]
      N.finger    = noteAsDict["finger"]
      N.voice     = noteAsDict["voice"]
      N.startTime = safeDict["timecodeList"][i]["startTime"]
      N.stopTime  = safeDict["timecodeList"][i]["stopTime"]
      N.id        = i
      self.noteList.append(N)

      if (N.finger != 0) :
        annotatedNoteCount += 1

      if (N.hand == NOTE_LEFT_HAND) :
        self.noteOnTimecodes["L"].append(N.startTime)
      elif (N.hand == NOTE_RIGHT_HAND) :
        self.noteOnTimecodes["R"].append(N.startTime)

      self.noteOnTimecodes["LR_full"].append(N.startTime)

      noteCount += 1

    # Tidy up:
    # - sort the timecodes by ascending values
    # - remove duplicate entries
    self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
    self.noteOnTimecodes["LR_full"].sort()

    self.noteOnTimecodes["LR"] = set(self.noteOnTimecodes["LR_full"])
    self.noteOnTimecodes["LR"] = list(self.noteOnTimecodes["LR"])
    self.noteOnTimecodes["LR"].sort()

    self._buildCursorsLR()

    self.length = len(self.noteOnTimecodes["LR"])
    self.cursorMax = self.length-1

    stopTime = time.time()
    print(f"[INFO] Loading time: {stopTime-startTime:.2f}s")
    print(f"[INFO] {noteCount} notes read from .gq3 file.")
    print(f"[INFO] Score length: {self.length} steps")
    
    print(f"[INFO] Progress: {annotatedNoteCount}/{noteCount} ({100*annotatedNoteCount/noteCount:.1f}%)")



  # ---------------------------------------------------------------------------
  # METHOD Score.exportToPrFile_DEPRECATED()
  # ---------------------------------------------------------------------------
  def exportToPrFile_DEPRECATED(self, prFile: str, backup = False) -> None :
    """

    *******
    WARNING: '.pr' files have been deprecated since gangQin version 3.
    New files must be saved in '.gq3' format using 'Score.loadGQ3File()'.
    Do not maintain '.pr' file format.
    *******

    Exports the annotated score and all metadata (finger, hand, comments etc.) in 
    a '.pr' file (JSON) that can be imported later to restore the session.

    'prFile' must be the full path to the file.

    Call the function with 'backup = True' to save under a '.bak' extension instead
    so that the original file is not overwritten (used e.g. for autosave)
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
  # METHOD Score.save()
  # ---------------------------------------------------------------------------
  def save(self, gq3File: str = "", backup = False) -> None :
    """
    Exports the annotated score and all metadata (finger, hand, comments etc.) in 
    a '.gq3' file (JSON) that can be imported later to restore the session.

    By default, the song is saved in the same folder, unless a non-empty 
    directory specified.
    'gq3File' must be the full path to the file + file name.

    Call the function with 'backup = True' to save under a '.bak' extension instead
    so that the original file is not overwritten (used e.g. for autosave)
    """

    output = {}
    output["appVersion"]    = f"v{REV_MAJOR}.{REV_MINOR}"
    output["cursor"]        = self.getCursor()
    output["bookmarks"]     = self.bookmarks
    output["noteList"]      = []
    output["timecodeList"]  = []
    
    # Create a copy, we don't want the sorting operations to affect
    # the order in 'self.noteList'.
    L = self.noteList.copy()
    L.sort(key = lambda obj: obj.startTime)

    noteCount = 0
    for noteObj in L :
      noteAsDict = {
        "pitch"   : noteObj.pitch,
        "hand"    : noteObj.hand,
        "finger"  : noteObj.finger,
        "voice"   : noteObj.voice,
        "name"    : noteObj.name
      }
      output["noteList"].append(noteAsDict)
      
      timecodeAsDict = {
        "startTime" : noteObj.startTime,
        "stopTime"  : noteObj.stopTime
      }
      output["timecodeList"].append(timecodeAsDict)

      noteCount += 1

    # TODO
    # Written at the end of the JSON to simplify diff/merges
    output["tempoSections"] = []
    output["weakArbitrationSections"] = []

    # By default, save under the same directory
    if (gq3File == "") :
      gq3File = self.songFile
    
    if backup :
      (root, _) = os.path.splitext(gq3File)
      exportFile = root + ".bak"
    else :
      (root, _) = os.path.splitext(gq3File)
      exportFile = root + ".gq3"

    # Write to the file
    with open(exportFile, "w") as fileHandler :
      json.dump(output, fileHandler, indent = 2)

    currTime = datetime.datetime.now()
    if backup :
      print(f"[INFO] A backup of the current state was saved under '{exportFile}'")
    else :
      currTime = datetime.datetime.now()
      print(f"[DEBUG] {noteCount} notes written in .gq3 file.")
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
    Cursor value is protected, it cannot go out of bounds.
    
    NOTES
    - The jump ignores any loop settings i.e. it does not wrap if the step
      sets the cursor outside the loop boudaries.
      Use 'Score.cursorNext()' instead to take the loop into account and wrap 
      accordingly.
    - The actual jump depends on the current hand practice mode.  
      In single hand practice mode, the cursor can only jump to a location
      when something happens on the active hand.
      So the actual jump can be different from the requested jump. 
    """
    
    if (delta > 0) :

      # BOTH HAND PRACTICE
      if (self.activeHands == SCORE_ACTIVE_HANDS_BOTH) :
        self.cursorGoto(self.getCursor() + delta)

      # SINGLE HAND PRACTICE (LEFT)
      elif (self.activeHands == SCORE_ACTIVE_HANDS_LEFT) :
        index = self._getIndexInCursorsLeft(self.getCursor())
        
        if (index == -1) :
          print("[INTERNAL ERROR] Left hand practice is active, but there is no event on the left hand at this cursor. Cannot browse from here!")
          
        if ((index + delta) <= (len(self.cursorsLeft)-1)) :
          self.cursor = self.cursorsLeft[index + delta]

      # SINGLE HAND PRACTICE (RIGHT)
      elif (self.activeHands == SCORE_ACTIVE_HANDS_RIGHT) :
        index = self._getIndexInCursorsRight(self.getCursor())

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
        index = self._getIndexInCursorsLeft(self.getCursor())
        
        if (index == -1) :
          print("[INTERNAL ERROR] Left hand practice is active, but there is no event on the left hand at this cursor. Cannot browse from here!")
          
        if ((index + delta) >= 0) :
          self.cursor = self.cursorsLeft[index + delta]

      # SINGLE HAND PRACTICE (RIGHT)
      elif (self.activeHands == SCORE_ACTIVE_HANDS_RIGHT) :
        index = self._getIndexInCursorsRight(self.getCursor())

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
  # METHOD Score.cursorGotoNearestBookmark()
  # ---------------------------------------------------------------------------
  def cursorGotoNearestBookmark(self, direction : int) -> None :
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

    In case there is no solution, by default it returns the index that gives 
    the closest cursor to the target value.
    
    The closest match can be either before or after the target cursor.

    When force = True, it returns -1 when there is no exact solution instead
    of giving the nearest solution.
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

    In case there is no solution, by default it returns the index that gives 
    the closest cursor to the target value.
    
    The closest match can be either before or after the target cursor.

    When force = True, it returns -1 when there is no exact solution instead
    of giving the nearest solution.
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
    
    This method is usually called after loading a MIDI or .gq3 file, since 
    the information in these fields is redundant and does not bring added
    value to get stored in the file.
    """
    
    self.cursorsLeft  = []
    self.cursorsRight = []

    for (index, timecode) in enumerate(self.noteOnTimecodes["LR"]) :
      unassigned = True
      if (timecode in self.noteOnTimecodes["L"]) :
        self.cursorsLeft.append(index)
        unassigned = False

      if (timecode in self.noteOnTimecodes["R"]) :
        self.cursorsRight.append(index)
        unassigned = False
      
      if unassigned :
        print("[ERROR] Score._buildCursorsLR: a note was found with an unlisted time code (INTERNAL ERROR)")



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
    
    # TODO: might be incorrect for single hand practice mode
    return self.noteOnTimecodes["LR"][self.getCursor()]



  # ---------------------------------------------------------------------------
  # METHOD Score.getTeacherNotes()
  # ---------------------------------------------------------------------------
  def getTeacherNotes(self, includeSustain = False) :
    """
    Returns a list with all the notes that must be pressed at the current 
    position in the score.
    
    Only notes pressed at this cursor are returned.
    Sustained notes (notes that were pressed before and held up to the current 
    cursor) are not included in the list.
    """
    
    # Cursor hasn't changed since last request: return the cache
    if (self.getCursor() == self.teacherNotesCursor) :
      pass
    
    # Otherwise: regenerate the cache
    else :
      self._calculateTeacherNotes()
      self.teacherNotesCursor = self.getCursor()

    # Return a copy of the elaborated list.
    # We do not want the clients to mess with it
    return self.teacherNotes.copy()



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
    for N in self.teacherNotes :
      N.sustained = False
      # noteObj.visible = True
      # noteObj.inactive = False

    # Reset the cache
    self.teacherNotes = []
    
    for N in self.noteList :

      # TODO: optimise the 'for' loop. 
      # Notes are stored in chronological order in 'Score.noteList'
      # It is not necessary to explore the entire list at each function call.
      # Beyond a certain point, we know for sure that no more
      # note will be added to 'Score.teacherNotes'.

      # CASE 1: a note is pressed at this timecode
      if (N.startTime == self.getTimecode()) :
        
        # SINGLE HAND PRACTICE
        # Adds the notes with their "inactive" property to "True" 
        # so that it is displayed with the appropriate color.
        if (self.activeHands == SCORE_ACTIVE_HANDS_BOTH) :
          N.inactive = False
          self.teacherNotes.append(N)
        
        elif (self.activeHands == SCORE_ACTIVE_HANDS_LEFT) :
          if (N.hand != NOTE_LEFT_HAND) : 
            N.inactive = True
            self.teacherNotes.append(N)

        elif (self.activeHands == SCORE_ACTIVE_HANDS_RIGHT) :
          if (N.hand != NOTE_RIGHT_HAND) :
            N.inactive = True
            self.teacherNotes.append(N)

      # CASE 2: the note is held at this timecode
      elif ((N.startTime < self.getTimecode()) and (N.stopTime >= self.getTimecode())) :
        N.sustained = True
        self.teacherNotes.append(N)

      # CASE 3: the note is out of the current window
      else :
        pass

    # Detect void list of teacher notes
    # This is not supposed to happen
    if (len(self.teacherNotes) == 0) :
      print(f"[WARNING] Empty list of teacher notes (t = {self.getTimecode()}), possible internal error.")

    # TODO: filter out notes with 0 duration.
    # Still not sure why it happens.
    # See https://github.com/evernost/gangQin/issues/22
    filteredList = []
    for N in self.teacherNotes :
      if not(N.fromKeyboardInput) :
        if (N.startTime != N.stopTime):
          filteredList.append(N)
        else :
          print(f"[DEBUG] Score._calculateTeacherNotes(): null duration note detected (cursor = {self.getCursor()})")
      else :
        filteredList.append(N)
    self.teacherNotes = filteredList



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

    # Display the cursor value
    text.render(self.top.screen, f"CURSOR: {self.getCursor()+1} / {self.length}", (12, 20), 2, GUI_TEXT_COLOR)

    # Display the bookmark number
    if self.cursorIsBookmarked() :
      text.render(self.top.screen, f"BOOKMARK #{self.getBookmarkIndex()}", (10, 470), 2, GUI_TEXT_COLOR)

    # Display the active hands
    text.render(self.top.screen, self.activeHands, (1288, 470), 2, GUI_TEXT_COLOR)



  # ---------------------------------------------------------------------------
  # METHOD Score._onKeyEvent()                                      [INHERITED]
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

  """
  NOTE_TRACKER object
  
  The NoteTracker class is a helper to keep track of the active notes while 
  reading a MIDI file.

  The MIDI file format has an intrisic flaw that causes ambiguity on the 
  exact moment a note stops if it is pressed multiple times before being 
  released. Although you cannot press a note twice, it makes sense in 
  musical notation, but it translates poorly to a MIDI file. 
  
  The NoteTracker takes this into account and gives the possibility to 
  restore the proper way to play based on the information in the MIDI file.

  Attributes:
  - active: list of note objects that are/have been pressed with 
    an overlap condition
    Most of the time, there is 1 note in the array per pitch and track.
    For overlapping notes (pressed again without prior release), there can be 2.
    So far, no MIDI file made this counter go higher than 2.

  In case of overlapping notes, it is not possible to tell what note
  in the overlapping ones is targeted by the note off event.
  The strategy for overlapping notes is the following:
  - a note off message closes the latest note that was pressed
  - the first note to be pressed will be the last one to be closed.

  The strategy assumes that some MIDI files could contain 3 or more overlapping
  notes (!) even though none were found with more than 2. 
  """

  def __init__(self) :

    self.active = {
      SCORE_RIGHT_HAND_TRACK_ID : [[] for _ in range(128)],
      SCORE_LEFT_HAND_TRACK_ID  : [[] for _ in range(128)]
    }



  def keyPress(self, noteObj, timecode: int) -> None :
    """
    Declares a note starting in the score.
    Takes a Note object as argument and:
    - edits its start time
    - adds it to the active note database
    """

    # Set the note start time
    noteObj.start(timecode)

    # Register the keypress
    self.active[noteObj.hand][noteObj.pitch].append(noteObj)

    

  def keyRelease(self, pitch: int, channel: int, timecode: int) -> None :
    """
    Declares a note ending in the score.
    """

    if (len(self.active[channel][pitch]) == 0) :
      print(f"[WARNING] NoteTracker.keyRelease(): read a 'keyRelease' with no matching 'keyPress'. Note will be ignored (timecode = {timecode})")
    
    else :
      
      # One note is active
      if (len(self.active[channel][pitch]) == 1) :  
        self.active[channel][pitch][0].stop(timecode)
        self.active[channel][pitch] = []
      
      # More than one note are active
      # Close the latest notes first
      else :
        
        nNotes = len(self.active[channel][pitch])
        if (nNotes > 2) :
          print("[WARNING] NoteTracker: found an unusual number of overlapping keypresses (odd MIDI file)")

        # Close the notes    
        for i in range(1, nNotes) :
          self.active[channel][pitch][i].stop(timecode)
      
        # Remove them
        self.active[channel][pitch][1:] = []


  def checkOnExit(self) -> None :
    """
    Checks the database before closing the MIDI file.
    """

    isValid = True

    for channel in self.active :
      for pitch in range(128) :
        if (len(self.active[channel][pitch]) > 0) :
          isValid = False

    if isValid :
      print("[INFO] NoteTracker: check OK (no pending notes)")
    else :
      print("[WARNING] NoteTracker: MIDI file processing is done, but some notes were pressed and never released (odd MIDI file)")



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  print("[INFO] Library 'Score' called as main: running unit tests...")

  # *****************
  # TEST: MIDI IMPORT
  # *****************
  # List all MIDI files
  midiFiles = [SONG_PATH + "/" + f for f in os.listdir(SONG_PATH) if f.endswith(".mid") and os.path.isfile(os.path.join(SONG_PATH, f))]
  
  # Test the import on all of them
  for file in midiFiles :
    print("")
    print(f"***** FILE: {file} *****")
    print("")
    scoreNew = Score(top = None)
    scoreNew.loadMidiFile(file, ['R', 'L', '', '', '', '', '', '', ''])


  # *****************************
  # TEST: DATA LOSS IN GQ3 FORMAT
  # *****************************
  # Import a '.gq3' file, export a copy without any modifications.
  # Compare the input and output file. No information shall be lost in the 
  # process. 
  songFile = SONG_PATH + "/" + "Rachmaninoff_Piano_Concerto_No2_Op18.gq3"
  scoreRef = Score(top = None)
  scoreRef.loadGq3File(songFile)
  scoreRef.save(songFile, backup = True)

  scoreNew = Score(top = None)
  scoreNew.save(songFile)

  # Compare attributes between 'scoreNew' and 'scoreOld'
  # No major difference should show, especially in the internal score 
  # database (notes, fingersatz, etc.)
  # ...
  # This section is TODO.
  # ...


  # Experiments with GQ3 file format (gangQin v.3)
  songFile = SONG_PATH + "/" + "Medtner_-_Forgotten Melodies_Op_38_II_Danza_graziosa_rev0.mid"
  score = Score(top = None)
  score.loadMIDIFile(songFile, ['R', 'L'])
  score.save(SONG_PATH + "/" + "Medtner0.gq3")

  songFile = SONG_PATH + "/" + "Medtner_-_Forgotten Melodies_Op_38_II_Danza_graziosa_rev1.mid"
  score = Score(top = None)
  score.loadMIDIFile(songFile, ['R', 'L'])
  score.save(SONG_PATH + "/" + "Medtner1.gq3")


  songFile = SONG_PATH + "/" + "Rachmaninoff_Piano_Concerto_No2_Op18.pr"
  score = Score(top = None)
  score.loadPRFile(songFile)
  score.save(songFile)


