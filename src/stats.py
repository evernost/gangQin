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
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'session.py'")



# =============================================================================
# Constants pool
# =============================================================================
TICK_INTERVAL_MS = 500



# =============================================================================
# Main code
# =============================================================================
class Stats :

  """
  Monitors the activity, user inputs for statistic purposes.
  It provides various hindsights relative to the performance on the song like:
  - active time spent learning the score
  - number of practice sessions
  - average practice time per session 
  - etc.

  All information are stored in a human readable log file.

  Note: all information is stored LOCALLY for the sole purpose of the user ONLY. 
  Nothing is sent to a server for telemetry mumbo jumbo or any "improving user experience"
  kind of crap.
  """
  def __init__(self, songFile) :
    self.logFile = ""
    
    self.scoreLength = 0

    self.sessionCount = 1
    self.sessionLog = []            # Each entry is a string with the time, date and duration of the session
    self.sessionStartTime = datetime.datetime.now()
    self.sessionStopTime = 0
    self.sessionAvgPracticeTime = 0

    self.totalPracticeTimeSec = 0

    self.comboCount = 0
    self.comboDrop = False
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

    self._initFromFile(songFile)



  # ---------------------------------------------------------------------------
  # METHOD Stats._initFromFile()
  # ---------------------------------------------------------------------------
  def _initFromFile(self, songFile) :
    """
    Initialises the log: load from a log file if it exists, otherwise create 
    a new one.
    """
    
    # Build the name for the log file
    (_, rootNameExt) = os.path.split(songFile)
    (rootName, _) = os.path.splitext(rootNameExt)
    self.logFile = os.path.join(".", "logs", rootName + ".log")
    
    if os.path.isfile(self.logFile) :
      with open(self.logFile, "r") as jsonFile:
        data = json.load(jsonFile)

      # Load the fields
      self.sessionCount = data["sessionCount"]
      self.sessionLog = data["sessionLog"]

      self.totalPracticeTimeSec = data["totalPracticeTimeSec"]

      self.comboHighestAllTime = data["comboHighestAllTime"]

      self.cursorHistogram = data["cursorHistogram"]
      self.cursorWrongNoteCount = []

      self.cursorStats = -1
      self.statsSteadyCount = 0
      self.statsCursor = []

      # Prepare the new session
      self.sessionCount += 1
      if (self.sessionCount > 1) :
        self.sessionAvgPracticeTime = round(self.totalPracticeTimeSec/(60*self.sessionCount))
      else :
        self.sessionAvgPracticeTime = 0.0



    else :
      print("[NOTE] No log file exists for this song. A new one will be created.")


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
    print("tictoc!")








  # ---------------------------------------------------------------------------
  # METHOD Stats.resetIdleTimer()
  # ---------------------------------------------------------------------------
  def resetIdleTimer(self) :
    """
    Resets the idle timer (inactivity detection) e.g. when activity shows on 
    the input keyboard.
    """
    self.cursorIdleTimer = 0




