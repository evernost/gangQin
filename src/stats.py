# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : stats
# File name     : stats.py
# File type     : Python script (Python 3)
# Purpose       : generates statistics about the user practice of the song.
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : September 15th, 2024
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
  todo
  """
  def __init__(self, songFile) :
    self.logFile = ""
    
    self.scoreLength = 0

    self.sessionCount = 0
    self.sessionStartTime = datetime.datetime.now()
    self.sessionStopTime = 0

    self.totalPracticeTimeSec = 0

    self.comboCount = 0
    self.comboDrop = False
    self.comboHighestSession = 0
    self.comboHighestAllTime = 0

    self.cursorHistogram = []
    self.cursorWrongNoteCount = []

    self.cursorStats = -1
    self.statsSteadyCount = 0
    self.statsCursor = []

    self._initFile(songFile)



  # ---------------------------------------------------------------------------
  # METHOD Stats._initFile()
  # ---------------------------------------------------------------------------
  def _initFile(self, songFile) :
    """
    Initialises the log file: load the log file if it exists or create a new 
    one if it does not exist yet.
    """
    
    (_, rootNameExt) = os.path.split(songFile)
    (rootName, _) = os.path.splitext(rootNameExt)
    self.logFile = './logs/' + rootName + ".log"
    
    if os.path.isfile(self.logFile) :
      print(f"That does not exist")



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
    Resets the idle timer, i.e. the timer that detects inactivity on the app.
    """
    print("TODO!")




