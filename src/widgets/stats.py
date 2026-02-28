# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : stats
# File name     : stats.py
# File type     : Python script (Python 3)
# Purpose       : generates statistics about the user practice of the song.
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 15 September 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project specific constants
from src.commons import *
import src.widgets.widget as widget

# Standard libraries
import datetime
import json
import os
import time
import re       # For fancy markdown array generation from formatted logs



# =============================================================================
# CONSTANTS
# =============================================================================
TICK_INTERVAL_MS = 500                # Deprecated.
MINIMAL_SESSION_DURATION_SEC = 60*5   # Minimal duration required for a session to have its stats saved
IDLE_TIME_THRESHOLD_SEC = 20          # After this amount of time without any user activity, the inactivity time is deduced from the session time



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Stats(widget.Widget) :

  """
  STATS Object
  
  Monitors the activity, right/wrong notes to provide some statistics.
  It gives access to various hindsights relative to the performance on the song like:
  - active time spent learning the score
  - number of practice sessions
  - average practice time per session 
  - etc.

  All information are stored in a human readable log file in ./logs

  NOTE: all information is stored locally for the sole purpose of the user ONLY. 
  Nothing is sent to a server for telemetry mumbo jumbo or any "improving user experience"
  kind of crap.
  """

  def __init__(self, top) :
    
    # Call the Widget init method
    super().__init__(top, loc = WIDGET_LOC_UNDEFINED)
   
    self.name = "stats"

    self.logName = ""
    self.logFile = ""
    self.mdName = ""                # Name of the report file (Markdown) e.g. "my_song.md"
    self.mdFile = ""                # Path to the report file (Markdown) e.g. "./logs/my_song.md"
    
    self.scoreLength = 0

    self.isEmpty = True             # True if a new statistics file has been created

    self.sessionCount = 0           # Session counter, incremented at the beginning of the session.
    self.sessionLog = []            # Each entry is a string with the time, date and duration of the session
    self.sessionStartTime = 0
    self.sessionStopTime = 0
    self.sessionAvgPracticeTime_sec = 0

    self.totalPracticeTime_sec = 0
    self.totalPracticeTime_hms = 0

    self.comboCount = 0
    self.comboDrop = 0
    self.comboDropHistogram = {}    # For each cursor value, keeps track of how many times there was a combo drop (deprecated?)
    self.comboFell = False
    self.comboHighestSession = 0
    self.comboHighestAllTime = 0

    self.cursorHistogram = {}       # For a given cursor: how many times this location was hit
    self.cursorWrongNoteCount = {}  # For a given cursor: how many times a wrong note was played
    self.cursorIdleTimer = 0        # Timer detecting a session on idle (user does not play anymore)
    self.cursorLastWrongReport = -1
    
    self.playedNotes = 0            # Total number of correct notes played, regardless of the arbiter's decision
    self.playedNotesValid = 0       # Total number of correct notes played i.e. valid keyboard input that incremented the cursor

    self.tickInterval_ms = 0

    self.intervalStartTime = -1
    self.intervalStartTimecode = -1
    self.intervalTimerTicking = False
    self.intervalMeasureCount = 0
    self.intervalRatioSum = 0
    self.intervalRatioAvg = 0

    self.lastActivity = time.perf_counter()
    self.totalInactivity_sec = 0

    # UI interaction queues
    self.msgQueueIn = []
    self.msgQueueOut = []



  # ---------------------------------------------------------------------------
  # METHOD Stats.load()
  # ---------------------------------------------------------------------------
  def load(self, songFile) :
    """
    Loads the statistics associated with the input song 'songFile'.

    'songFile' must be the full path to the song file.
    The name of the log file is automatically derived from it.
    EXAMPLE: songFile = './logs/Beethoven_Fuer_Elise.gq3'

    If the .log doesn't exist, a new one will be created.
    """

    # Build the name for the log file 
    # File is stored in './logs'
    (_, songNameWithExt) = os.path.split(songFile)
    (songName, _) = os.path.splitext(songNameWithExt)
    self.songName     = songName
    self.songFile     = songNameWithExt
    self.logName      = songName + ".log"         # Example: "my_song.log"
    self.logFile      = f"./logs/{self.logName}"  # Example: "./logs/my_song.log"
    self.mdName       = songName + ".md"          # Example: "my_song.md"
    self.mdFile       = f"./logs/{self.mdName}"   # Example: "./logs/my_song.md"
    
    self.scoreLength  = self.top.widgets[WIDGET_ID_SCORE].getScoreLength()
    
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
  def _safePopulate(self, data = {}) -> None :
    """
    Populates the stats from a json object.
    If none is given, it initialises with default values.

    The function handles possible missing fields, since the stats' content may
    evolve a lot throughout the revisions.
    """
    
    # All these fields will be loaded from the file if they exist.
    # Also, it defines a 'fallback' dictionary in case some fields don't exist.    
    fieldsRef = {
      "sessionCount"                : 0,
      "sessionLog"                  : [],
      "sessionAvgPracticeTime_sec"  : 0,
      "totalPracticeTime_sec"       : 0,
      "comboCount"                  : 0,
      "comboDrop"                   : 0,
      "comboFell"                   : False,
      "comboHighestAllTime"         : 0,
      "cursorHistogram"             : {},
      "cursorWrongNoteCount"        : {},
      "cursorIdleTimer"             : 0,
      "playedNotes"                 : 0,
      "playedNotesValid"            : 0,
      "tickInterval_ms"             : 0
    }

    for field in fieldsRef :
      if field in data :
        fieldsRef[field] = data[field]
      else :
        print(f"[INFO] Stats._safePopulate(): field '{field}' is doesn't exist in this log file and will get a default value.")

    # There might be a cleaner version to do that.
    self.sessionCount               = fieldsRef["sessionCount"]
    self.sessionLog                 = fieldsRef["sessionLog"]
    self.sessionAvgPracticeTime_sec = fieldsRef["sessionAvgPracticeTime_sec"]
    self.totalPracticeTime_sec      = fieldsRef["totalPracticeTime_sec"]
    self.comboCount                 = fieldsRef["comboCount"]
    self.comboDrop                  = fieldsRef["comboDrop"]
    self.comboFell                  = fieldsRef["comboFell"]
    self.comboHighestAllTime        = fieldsRef["comboHighestAllTime"]
    self.cursorHistogram            = fieldsRef["cursorHistogram"]
    self.cursorWrongNoteCount       = fieldsRef["cursorWrongNoteCount"]
    self.cursorIdleTimer            = fieldsRef["cursorIdleTimer"]
    self.playedNotes                = fieldsRef["playedNotes"]
    self.playedNotesValid           = fieldsRef["playedNotesValid"]
    self.tickInterval_ms            = fieldsRef["tickInterval_ms"]



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
      self.sessionAvgPracticeTime = round(self.totalPracticeTime_sec/(60*self.sessionCount))
    else :
      self.sessionAvgPracticeTime = 0.0



  # ---------------------------------------------------------------------------
  # METHOD Stats.printIntroSummary()
  # ---------------------------------------------------------------------------
  def printIntroSummary(self) :
    """
    Prints a short summary of the current stats as introduction.
    This is usually called right after loading the practice session.
    """

    print("")
    print(f"[INFO] Get ready for session #{self.sessionCount}!")
    print(f"[INFO] Total practice time so far: {round(self.totalPracticeTime_sec/60)} minutes")
    if (self.sessionAvgPracticeTime > 0.0) :
      print(f"[INFO] Average session time: {self.sessionAvgPracticeTime} minutes")



  # ---------------------------------------------------------------------------
  # METHOD Stats.logUserActivity()
  # ---------------------------------------------------------------------------
  def logUserActivity(self) :
    """
    Resets the idle timer (inactivity detection) whenever the user shows he's 
    still alive.
    This function is typically called every time there is MIDI activity.
    """
    
    idleTime = round(time.perf_counter() - self.lastActivity)
    if (idleTime > IDLE_TIME_THRESHOLD_SEC) :
      self.totalInactivity_sec += idleTime

    if (idleTime > 180) :
      print("Welcome back, Sleeping Beauty :)")

    self.lastActivity = time.perf_counter()



  # ---------------------------------------------------------------------------
  # METHOD Stats.logCorrectNote()
  # ---------------------------------------------------------------------------
  def logCorrectNote(self) :
    """
    This function must be called every time the user plays a correct input.
    
    Updates the stats with a correct input:
    - increase the combo counter
    - update the highest combo value ever reached
    """

    self.comboCount += 1
    self.isComboBroken = False
    if (self.comboCount > self.comboHighestSession) :
      self.comboHighestSession = self.comboCount

    if (self.comboCount > self.comboHighestAllTime) :
      self.comboHighestAllTime = self.comboCount
    
    self.cursorLastWrongReport = -1



  # ---------------------------------------------------------------------------
  # METHOD Stats.logWrongNote()
  # ---------------------------------------------------------------------------
  def logWrongNote(self, cursor) :
    """
    This function must be called every time the user plays an incorrect input.
    
    Updates the stats with an incorrect input:
    - reset the combo counter
    - update the wrong note counter at this cursor
    """

    self.isComboBroken = (self.comboCount != 0)
    self.comboCount = 0
    
    if (cursor != self.cursorLastWrongReport) :
      if not(cursor in self.cursorWrongNoteCount) :
        self.cursorWrongNoteCount[cursor] = 1
      else :
        self.cursorWrongNoteCount[cursor] += 1
      
      self.cursorLastWrongReport = cursor
      print(f"[DEBUG] Wrong note! Total count: {self.cursorWrongNoteCount[cursor]}")
    
    

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
  # METHOD Score.generateSessionLog()
  # ---------------------------------------------------------------------------
  def generateSessionLog(self) :
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
    outputStr = self.sessionStartTime.strftime(f"Session {self.sessionCount}: %A, %B %d{daySuffix} (%Y) at %H:%M. Duration: {durationStr}")

    return outputStr



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
  # METHOD Stats.intervalTimerTick()
  # ---------------------------------------------------------------------------
  def intervalTimerUpdate(self, scoreTimecode, loopWrap = False) :
    """
    Updates the interval time tracker with the current timecode in the score.
    This function must be called on every correct note (i.e. cursor increase).
    
    In looped practice, set the flag 'loopWrap' to True when the loop wraps 
    back to the beginning to avoid an erroneous measurement.
    """
    
    if self.intervalTimerTicking :
      elapsedTime = time.perf_counter() - self.intervalStartTime
      elapsedTimecode = scoreTimecode - self.intervalStartTimecode
      
      if (elapsedTimecode > 0) :
        intervalRatio = elapsedTime/elapsedTimecode
        
        # Note: use a windowed average instead
        self.intervalRatioSum += intervalRatio
        self.intervalMeasureCount += 1
        self.intervalRatioAvg = self.intervalRatioSum/self.intervalMeasureCount
        
        print(f"[DEBUG] Normalised interval ratio = {intervalRatio/self.intervalRatioAvg:.2f} (avg = {self.intervalRatioAvg:.5f})")
        
      else :
        print(f"[DEBUG] Stats.stopIntervalTimer(): null variation in the timecodes")  

    else :
      self.intervalTimerTicking = True

    self.intervalStartTime = time.perf_counter()
    self.intervalStartTimecode = scoreTimecode



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

    print(f"[INFO] Inactivity time: {self.totalInactivity_sec}s")

    self.sessionStopTime = datetime.datetime.now()
    delta = self.sessionStopTime - self.sessionStartTime
    duration = round(delta.total_seconds())
    
    # Save log only if the session has a decent duration, otherwise it does not 
    # make much sense.
    if (duration > MINIMAL_SESSION_DURATION_SEC) :
    #if (True) :
      exportDict = {}
      exportDict["logName"]                 = self.logName
      exportDict["logFile"]                 = self.logFile
      exportDict["scoreLength"]             = self.scoreLength
      exportDict["sessionCount"]            = self.sessionCount
      exportDict["sessionLog"]              = self.sessionLog + [self.generateSessionLog()]
      exportDict["sessionAvgPracticeTime"]  = self.sessionAvgPracticeTime
      exportDict["totalPracticeTime_sec"]   = self.totalPracticeTime_sec + duration
      exportDict["totalPracticeTime_hms"]   = self.totalPracticeTime_sec + duration    # TODO!
      exportDict["cursorHistogram"]         = self.cursorHistogram
      exportDict["cursorWrongNoteCount"]    = self.cursorWrongNoteCount
      exportDict["comboHighestSession"]     = self.comboHighestSession
      exportDict["comboHighestAllTime"]     = self.comboHighestAllTime
      exportDict["playedNotes"]             = self.playedNotes
      exportDict["playedNotesValid"]        = self.playedNotesValid
      
      with open(self.logFile, "w") as jsonFile :
        json.dump(exportDict, jsonFile, indent = 2)
      print(f"[INFO] Session stats saved to '{self.logFile}'")

      self._saveMarkdownFile()
    
    else :
      print(f"[INFO] Stats for this session won't be saved (shorter than {MINIMAL_SESSION_DURATION_SEC}s) to keep logs meaningful.")



  # ---------------------------------------------------------------------------
  # METHOD Stats._saveMarkdownFile()                                        [PRIVATE]
  # ---------------------------------------------------------------------------
  def _saveMarkdownFile(self) :
    """
    Generates the report markdown file report.
    """

    with open(self.mdFile, "w", encoding = "utf-8") as fileHandler :
      fileHandler.write(f"# _{self.songName.replace('_', ' ')}_\n\n")
      fileHandler.write(f"## In a nutshell\n")
      fileHandler.write(f"- Score length: {self.scoreLength}\n")
      fileHandler.write(f"- Sessions: {self.sessionCount}\n")
      fileHandler.write(f"- Average practice time: -\n")
      fileHandler.write(f"- Fingered notes: {self.top.widgets[WIDGET_ID_SCORE].fingeredNoteCount}\n")
      fileHandler.write(f"- Date of first practice: -\n")
      fileHandler.write(f"## Session history\n")
      fileHandler.write(f"| Session | Date | Time | Duration |\n")
      fileHandler.write(f"|---------|------|------|----------|\n")
      fileHandler.write(self._logToMarkdown())



  # ---------------------------------------------------------------------------
  # METHOD Stats._saveMdFile()                                        [PRIVATE]
  # ---------------------------------------------------------------------------
  def _logToMarkdown(self) :
    """
    Generates a markdown array from the list of sessions.
    """

    q = self.sessionLog + [self.generateSessionLog()]

    pattern = re.compile(r"Session (\d+): (.+?) at (\d{2}:\d{2})\. Duration: (\d+min\d+s)")

    rows = []

    for entry in q:
      match = pattern.search(entry)
      if match :
        (session, date, time, duration) = match.groups()
        rows.append((int(session), date, time, duration))

    # Sort by descending session number
    rows.sort(reverse = True, key = lambda x: x[0])

    # Build markdown table
    md = []
    for session, date, time, duration in rows:
      md.append(f"| {session} | {date} | {time} | {duration} |")

    return "\n".join(md)


 



# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'stats.py'")

