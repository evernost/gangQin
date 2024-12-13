# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : stats
# File name     : stats.py
# File type     : Python script (Python 3)
# Purpose       : generates statistics about the user practice of the song.
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 15 September 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

import datetime
import json
import os
import time



# =============================================================================
# Constants pool
# =============================================================================
TICK_INTERVAL_MS = 500



# =============================================================================
# Main code
# =============================================================================
class Stats :

  """
  Monitors the activity, right/wrong notes to provide some statistics.
  It gives access to various hindsights relative to the performance on the song like:
  - active time spent learning the score
  - number of practice sessions
  - average practice time per session 
  - etc.

  All information are stored in a human readable log file in ./logs

  NOTE: all information is stored LOCALLY for the sole purpose of the user ONLY. 
  Nothing is sent to a server for telemetry mumbo jumbo or any "improving user experience"
  kind of crap.
  """

  def __init__(self) :
    self.logName = ""
    self.logFile = ""
    
    self.scoreLength = 0

    self.isEmpty = True             # True if a new statistics file has been created

    self.sessionCount = 0           # Session counter, incremented at the beginning of the session.
    self.sessionLog = []            # Each entry is a string with the time, date and duration of the session
    self.sessionStartTime = 0
    self.sessionStopTime = 0
    self.sessionAvgPracticeTime = 0

    self.totalPracticeTimeSec = 0

    self.comboCount = 0
    self.comboDrop = 0
    self.comboDropHistogram = []    # For each cursor value, keeps track of how many times there was a combo drop
    self.comboFell = False
    self.comboHighestSession = 0
    self.comboHighestAllTime = 0

    self.cursorHistogram = []       # For a given cursor: how many times this location was hit
    self.cursorWrongNoteCount = []  # For a given cursor: how many times a wrong note was played
    self.cursorIdleTimer = 0        # Timer detecting a session on idle (user does not play anymore)
    
    self.playedNotes = 0            # Total number of correct notes played, regardless of the arbiter's decision
    self.playedNotesValid = 0       # Total number of correct notes played i.e. valid keyboard input that incremented the cursor

    self.tickInterval_ms = 0

    # UI interaction queues
    self.msgQueueIn = []
    self.msgQueueOut = []



  # ---------------------------------------------------------------------------
  # METHOD Stats.load(<.pr filename string>)
  # ---------------------------------------------------------------------------
  def load(self, songFile) :
    """
    Loads the statistics associated with the input song 'songFile'.
    The statistics are read from a .log file whose name is automatically 
    derived from 'songFile'.

    If no .log exists, a new one will be created.
    """

    # Build the name for the log file 
    # File is stored in './logs'
    (_, rootNameExt) = os.path.split(songFile)
    (rootName, _) = os.path.splitext(rootNameExt)
    self.songName   = rootName
    self.songFile   = rootNameExt
    self.logName    = rootName + ".log"         # Example: "my_song.log"
    self.logFile    = f"./logs/{self.logName}"  # Example: "./logs/my_song.log"
    
    # Log file exists: load it
    if os.path.isfile(self.logFile) :
      print(f"[DEBUG] Stats: reading from '{self.logName}'...")
      with open(self.logFile, "r") as jsonFile :
        data = json.load(jsonFile)
 
      self._safePopulate(data)
      self.isEmpty = False

    # Log file does not exist: create it
    else :
      print("[INFO] Stats: no log file found. A new one will be created.")
      self._safePopulate()
      self.isEmpty = True

    # Initialise the fields of this new session
    self._sessionInit()



  # ---------------------------------------------------------------------------
  # METHOD Stats._safePopulate(json Object)
  # ---------------------------------------------------------------------------
  def _safePopulate(self, data = {}) :
    """
    Populates the fields of the object from an imported json data structure.
    If none is given, it is initialised with default values.

    The function adds safety measures to handle missing fields and give them 
    a default value.
    The feature is handy to maintain compatibility accross different versions
    of gangQin, since the stat fields are very likely to evolve.
    """
    
    # Define a 'fallback' dictionary, in case some fields do not exist.
    attributesRef = {
      "logName"                 : self.logName,
      "logFile"                 : self.logFile,
      "scoreLength"             : 0,
      "sessionCount"            : 0,
      "sessionLog"              : [],
      "sessionStartTime"        : 0,
      "sessionStopTime"         : 0,
      "sessionAvgPracticeTime"  : 0,
      "totalPracticeTimeSec"    : 0,
      "comboCount"              : 0,
      "comboDrop"               : 0,
      "comboFell"               : False,
      "comboHighestSession"     : 0,
      "comboHighestAllTime"     : 0,
      "cursorHistogram"         : [],
      "cursorWrongNoteCount"    : [],
      "cursorIdleTimer"         : 0,
      "playedNotes"             : 0,
      "playedNotesValid"        : 0,
      "tickInterval_ms"         : 0
    }

    # Try to load each field
    for attr in attributesRef :
      if attr in data :
        attributesRef[attr] = data[attr]

      else :
        print(f"[INFO] Stats: field '{attr}' is missing in the log file and will get a default value.")


    # There might be a cleaner version to do that.
    self.logName                = attributesRef["logName"]
    self.logFile                = attributesRef["logFile"]
    self.scoreLength            = attributesRef["scoreLength"]        
    self.sessionCount           = attributesRef["sessionCount"]
    self.sessionLog             = attributesRef["sessionLog"]
    self.sessionStartTime       = attributesRef["sessionStartTime"]
    self.sessionStopTime        = attributesRef["sessionStopTime"]
    self.sessionAvgPracticeTime = attributesRef["sessionAvgPracticeTime"]
    self.totalPracticeTimeSec   = attributesRef["totalPracticeTimeSec"]
    self.comboCount             = attributesRef["comboCount"]
    self.comboDrop              = attributesRef["comboDrop"]
    self.comboFell              = attributesRef["comboFell"]
    self.comboHighestSession    = attributesRef["comboHighestSession"]
    self.comboHighestAllTime    = attributesRef["comboHighestAllTime"]
    self.cursorHistogram        = attributesRef["cursorHistogram"]
    self.cursorWrongNoteCount   = attributesRef["cursorWrongNoteCount"]
    self.cursorIdleTimer        = attributesRef["cursorIdleTimer"]
    self.playedNotes            = attributesRef["playedNotes"]
    self.playedNotesValid       = attributesRef["playedNotesValid"]
    self.tickInterval_ms        = attributesRef["tickInterval_ms"]



  # ---------------------------------------------------------------------------
  # METHOD Stats._sessionInit()
  # ---------------------------------------------------------------------------
  def _sessionInit(self) :
    """
    Initialises the attributes.
    This function must be called at the app start-up (new session)
    """
    
    self.sessionStartTime = datetime.datetime.now()
    self.sessionStopTime = -1

    self.sessionCount += 1
    if (self.sessionCount > 1) :
      self.sessionAvgPracticeTime = round(self.totalPracticeTimeSec/(60*self.sessionCount))
    else :
      self.sessionAvgPracticeTime = 0.0



  # ---------------------------------------------------------------------------
  # METHOD Stats.showIntroSummary()
  # ---------------------------------------------------------------------------
  def showIntroSummary(self) :
    """
    Prints a short summary of the current stats as introduction.
    This is usually called right after loading the practice session.
    """

    print("")
    print(f"[INFO] Get ready for session #{self.sessionCount}!")
    print(f"[INFO] Total practice time so far: {round(self.totalPracticeTimeSec/60)} minutes")
    if (self.sessionAvgPracticeTime > 0.0) :
      print(f"[INFO] Average session time: {self.sessionAvgPracticeTime} minutes")



  # ---------------------------------------------------------------------------
  # METHOD Stats.correctNote()
  # ---------------------------------------------------------------------------
  def correctNote(self) :
    """
    Updates the combo counter when the input is valid and triggers the next 
    cursor.
    """

    self.comboCount += 1
    self.isComboBroken = False
    if (self.comboCount > self.comboHighestSession) :
      self.comboHighestSession = self.comboCount

    if (self.comboCount > self.comboHighestAllTime) :
      self.comboHighestAllTime = self.comboCount



  # ---------------------------------------------------------------------------
  # METHOD Stats.wrongNote()
  # ---------------------------------------------------------------------------
  def wrongNote(self) :
    """
    Update the combo counter when an incorrect keyboard input is given.
    Partial but correct inputs do not trigger a "wrong note" condition.
    """

    self.isComboBroken = (self.comboCount != 0)
    self.comboCount = 0
    
    

  # ---------------------------------------------------------------------------
  # METHOD Stats.tick()
  # ---------------------------------------------------------------------------
  def tick(self) :
    """
    Updates the statistics.
    This function needs to be called by the main app periodically, at the rate 
    defined by 'TICK_INTERVAL_MS'.

    The function is used to detect inactivity periods, measure time spent in a 
    given section etc.
    """

    #print("tictoc!")
    pass



  # ---------------------------------------------------------------------------
  # METHOD Score.getSessionLog()
  # ---------------------------------------------------------------------------
  def getSessionLog(self) :
    """
    Packs the information of the current session in a human-readable string.
    """

    day = self.sessionStartTime.day
    
    if ((4 <= day <= 20) or (24 <= day <= 30)) :
      daySuffix = "th"
    else:
      daySuffix = ["st", "nd", "rd"][day % 10 - 1]

    duration = self.sessionStopTime - self.sessionStartTime
    duration = int(round(duration.total_seconds()))
    durationStr = f"{duration // 60}min{duration % 60}s"
    outputStr = self.sessionStartTime.strftime(f"Session {self.sessionCount}: %A, %B %d{daySuffix} at %H:%M. Duration: {durationStr}")

    return outputStr



  # ---------------------------------------------------------------------------
  # METHOD Score.updateStats()
  # ---------------------------------------------------------------------------
  # def updateStats(self) :
  #   """
  #   Add the current cursor to the statistics.
  #   """
    
  #   if (self.getCursor() != self.statsLastCursor) :
  #     self.statsSteadyCount = 0
  #     self.statsLastCursor = self.getCursor()

  #   else :
  #     if (self.statsSteadyCount < CURSOR_STEADY_COUNT_LIMIT) :
  #       self.statsCursor[self.getCursor()] += 1
  #       self.statsSteadyCount += 1

  #     elif (self.statsSteadyCount == CURSOR_STEADY_COUNT_LIMIT) :
  #       print(f"[DEBUG] Steady limit reached! (cursor = {self.getCursor()+1})")
  #       self.statsSteadyCount += 1

  #     else :
  #       pass



  # ---------------------------------------------------------------------------
  # METHOD Stats.resetIdleTimer()
  # ---------------------------------------------------------------------------
  def resetIdleTimer(self) :
    """
    Resets the idle timer (inactivity detection) e.g. when activity shows on 
    the input keyboard.
    """
    self.cursorIdleTimer = 0



  # ---------------------------------------------------------------------------
  # METHOD Stats.save()
  # ---------------------------------------------------------------------------
  def save(self) :
    """
    Saves the new statistics.
    The saving process updates the underlying .log file (json) that stores all 
    the info.
    """

    print("[INFO] Exporting stats...")

    self.sessionStopTime = datetime.datetime.now()
    duration = self.sessionStopTime - self.sessionStartTime
    
    exportDict = {}
    exportDict["sessionCount"]              = self.sessionCount
    exportDict["sessionLog"]                = self.sessionLog + [self.getSessionLog()]
    exportDict["sessionAvgPracticeTime"]    = self.sessionAvgPracticeTime
    exportDict["totalPracticeTimeSec"]      = self.totalPracticeTimeSec + round(duration.total_seconds())
    
    with open(self.logFile, "w") as jsonFile :
      json.dump(exportDict, jsonFile, indent = 2)

    print(f"[INFO] Saved to '{self.logFile}'")



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'stats.py'")

