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
import time



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'session.py'")



# =============================================================================
# Constants pool
# =============================================================================
# None.



class Stats :

  """
  todo
  """
  def __init__(self) :
    
    self.sessionCount = 0
    self.sessionStartTime = datetime.datetime.now()
    self.sessionStopTime = 0
    self.sessionTotalPracticeTimeSec = 0
    self.sessionLogString = []

    self.comboCount = 0
    self.comboDrop = False
    self.comboHighestSession = 0
    self.comboHighestAllTime = 0

    self.cursorStats = -1
    self.statsSteadyCount = 0
    self.statsCursor = []







  # ---------------------------------------------------------------------------
  # METHOD Score.getCursor()
  # ---------------------------------------------------------------------------
  def getCursor(self) :
    """
    Returns the value of the cursor at the current location in the score.
    """
    return self.cursor
  


  # ---------------------------------------------------------------------------
  # METHOD Score.getCursorsLeftPointer()
  # ---------------------------------------------------------------------------
  def getCursorsLeftPointer(self, cursor, force = False) :
    """
    Returns the value <p> such that cursorsLeft[p] is equal to the query <cursor>.

    If no such value exists, the function returns:
    - -1 when <force> is False (default)
    - <p> such that cursorsLeft[p] is the closest possible to <cursor> otherwise.
    """
    if (cursor in self.cursorsLeft) :
      index = self.cursorsLeft.index(cursor)
      return index

    else :
      if force :
        minDist = abs(cursor - self.cursorsLeft[0]); minIndex = 0
        for (idx, cursorLeft) in enumerate(self.cursorsLeft) :
          if (abs(cursor - cursorLeft) < minDist) :
            minDist = abs(cursor - cursorLeft)
            minIndex = idx

        print(f"[DEBUG] Requested cursor: {cursor}, closest: {minIndex}")
        return minIndex

      else :
        return -1
    
