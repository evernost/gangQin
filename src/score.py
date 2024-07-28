# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : score
# File name     : score.py
# File type     : Python script (Python 3)
# Purpose       : provides the functions to interact with the music score
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

import note

import json   # for JSON database import/export
import os     # for file manipulation
import mido   # for MIDI file manipulation

import datetime
import time
import re



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This lib is not intended to be called as a main.")



# =============================================================================
# Constants pool
# =============================================================================
SET_CURSOR_SUCCESS = 0



class Score :

  """
  DESCRIPTION
  
  The Score objects contains the music score, but also stores all the settings 
  of the practice session.
  
  Score is read from a MIDI file
  
  In a MIDI file, each event (note on/note off) has a timestamp attached.
  
  The value of the timestamp depends on the tempo that has been defined, the duration
  of the note, etc.
  
  The Score abstracts these timecodes and browses in the song using a 'cursor'.
  Every time a note starts playing in the song, a cursor is assigned to it.
  
  
  
  ATTRIBUTES
  
  - <noteOnTimecodes>: dictionary containing the following subsets:
    - "LR_full" : full list of the note start timecodes (including duplicates)
    - "LR"      : same as "LR", without the duplicate values
    - "L"       : list of the note start timecodes (left hand only), duplicates removed
    - "R"       : list of the note start timecodes (right hand only), duplicates removed
    
    
  - <cursorsLeft>   : list of cursors values where a note is pressed on the left hand
  - <cursorsRight>  : list of cursors values where a note is pressed on the right hand


  """
  def __init__(self) :
    
    # General information about the score
    self.nStaffs = 2
    self.avgNoteDuration = 0
    self.hasUnsavedChanges = False
    
    self.cursor = 0
    self.cursorMax = 0
    self.scoreLength = 0

    self.pianoRoll = [[[] for _ in range(128)] for _ in range(self.nStaffs)]

    self.noteOnTimecodes = {"L": [], "R": [], "LR": [], "LR_full": []}
    
    self.cursorsLeft = []
    self.cursorsRight = []

    self.bookmarks = []
    
    self.activeHands = "LR"
    
    self.teacherNotes = []
    self.sustainedNotes = []

    self.cachedCursor = -1
    self.cachedTeacherNotes = []

    # Key scales used throughout the song
    # List of tuples: (scaleObject, startTimeCode)
    self.keyList = []

    self.progressEnable = True
    
    # Combo!
    # Resets every time a wrong note is played.
    # Keeps track of the best scores achieved
    # TODO: remove it from the Score class
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
    


  # ---------------------------------------------------------------------------
  # METHOD Score.getCursorsRightPointer()
  # ---------------------------------------------------------------------------
  def getCursorsRightPointer(self, cursor, force = False) :
    """
    Returns the value <p> such that cursorsRight[p] is equal to the query <cursor>.

    If no such value exists, the function returns:
    - -1 when <force> is False (default)
    - <p> such that cursorsRight[p] is the closest possible to <cursor> otherwise.
    """
    if (cursor in self.cursorsRight) :
      index = self.cursorsRight.index(cursor)
      return index

    else :
      if force :
        minDist = abs(cursor - self.cursorsRight[0]); minIndex = 0
        for (idx, cursorLeft) in enumerate(self.cursorsRight) :
          if (abs(cursor - cursorLeft) < minDist) :
            minDist = abs(cursor - cursorLeft)
            minIndex = idx

        print(f"[DEBUG] Requested cursor: {cursor}, closest: {minIndex}")
        return minIndex

      else :
        return -1



  # ---------------------------------------------------------------------------
  # METHOD Score._buildCursorsLR()
  # ---------------------------------------------------------------------------
  def _buildCursorsLR(self) :
    """
    todo
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
  # METHOD Score.setCursor(value)
  # ---------------------------------------------------------------------------
  def setCursor(self, value, ignoreActiveHand = False) :
    """
    Sets the cursor to the given value.
    
    The function is protected so that:
    - values outside the score's range are clamped
    - values not aligned with the active hand are adjusted

    Setting the cursor must be done with this function exclusively.
    Manually setting the <cursor> attribute might cause crashes.

    """

    if (value < 0) :
      valueClamped = 0
    elif (value > self.cursorMax) :
      valueClamped = self.cursorMax
    else :
      valueClamped = value



    if (self.activeHands == ACTIVE_HANDS_BOTH) :
      self.cursor = valueClamped

    elif (self.activeHands == ACTIVE_HANDS_LEFT) :
      if ignoreActiveHand :
        self.cursor = valueClamped
      else: 
        p = self.getCursorsLeftPointer(valueClamped, force = True)
        self.cursor = self.cursorsLeft[p]

    elif (self.activeHands == ACTIVE_HANDS_RIGHT) :
      if ignoreActiveHand :
        self.cursor = valueClamped
      else: 
        p = self.getCursorsRightPointer(valueClamped, force = True)
        self.cursor = self.cursorsRight[p]

    else :
      print("[INTERNAL ERROR] Score.setCursor: unknown active hand specification!")

    


  # ---------------------------------------------------------------------------
  # METHOD Score.getCurrentTimecode()
  # ---------------------------------------------------------------------------
  def getCurrentTimecode(self) :
    """
    Returns the MIDI timecode of the current location in the score.
    """
    
    # TODO: incorrect for single hand practice mode
    return self.noteOnTimecodes["LR"][self.cursor]



  # ---------------------------------------------------------------------------
  # METHOD Score.cursorBegin()
  # ---------------------------------------------------------------------------
  def cursorBegin(self) :
    """
    Sets the cursor to the beginning of the score.

    If loop practice is active, it jumps to the beginning of the loop.
    """

    # If the loop mode is enabled: go back to the beginning of the loop
    if (self.loopEnable and (self.cursor >= self.loopStart)) :
      self.setCursor(self.loopStart)
    
    else :
      self.setCursor(0)



  # ---------------------------------------------------------------------------
  # METHOD Score.cursorEnd()
  # ---------------------------------------------------------------------------
  def cursorEnd(self) :
    """
    Sets the cursor to the end of the score.

    If loop practice is active, it jumps to the end of the loop.
    """
    
    # If the loop mode is enabled: go back to the end of the loop
    if (self.loopEnable and (self.cursor <= self.loopEnd)) :
      
      # TODO: setting the cursor shall be protected depending on the active hand.
      # Directly setting the cursor is dangerous.
      self.cursor = self.loopEnd
    
    # Otherwise just set the cursor to the end
    else :
      self.setCursor(self.cursorMax)



  # ---------------------------------------------------------------------------
  # METHOD Score.cursorStep(delta)
  # ---------------------------------------------------------------------------
  def cursorStep(self, delta) :
    """
    Jumps in the score with a step (positive or negative)
    
    Jump is done by adding/subtracting the step to the cursor value.
    Cursor value clamps to the allowed range no matter the step given.
    
    NOTES
    - The jump ignores any loop settings i.e. it does not wrap if the step
      sets the cursor beyond the end of the loop.
      Use <cursorNext> instead to take the loop into account and wrap accordingly.
    - The cursor steps depending on the current hand practice mode. 
      In single hand practice mode, the jump will not be linear!
    """
    
    if (delta > 0) :

      # BOTH HAND PRACTICE
      if (self.activeHands == ACTIVE_HANDS_BOTH) :
        self.setCursor(self.getCursor() + delta)

      # SINGLE HAND PRACTICE (LEFT)
      elif (self.activeHands == ACTIVE_HANDS_LEFT) :
        index = self.getCursorsLeftPointer(self.getCursor())
        
        if (index == -1) :
          print("[INTERNAL ERROR] Left hand practice is active, but there is no event on the left hand at this cursor. Cannot browse from here!")
          
        if ((index + delta) <= (len(self.cursorsLeft)-1)) :
          self.cursor = self.cursorsLeft[index + delta]

      # SINGLE HAND PRACTICE (RIGHT)
      elif (self.activeHands == ACTIVE_HANDS_RIGHT) :
        index = self.getCursorsRightPointer(self.getCursor())

        if (index == -1) :
          print("[INTERNAL ERROR] Right hand practice is active, but there is no event on the right hand at this cursor. Cannot browse from here!")
          
        if ((index + delta) <= (len(self.cursorsRight)-1)) :
          self.cursor = self.cursorsRight[index + delta]

      else :
        print("[INTERNAL ERROR] Score.setCursor: unknown active hand specification!")



    else :

      # BOTH HAND PRACTICE
      if (self.activeHands == ACTIVE_HANDS_BOTH) :
        self.setCursor(self.getCursor() + delta)

      # SINGLE HAND PRACTICE (LEFT)
      elif (self.activeHands == ACTIVE_HANDS_LEFT) :
        index = self.getCursorsLeftPointer(self.getCursor())
        
        if (index == -1) :
          print("[INTERNAL ERROR] Left hand practice is active, but there is no event on the left hand at this cursor. Cannot browse from here!")
          
        if ((index + delta) >= 0) :
          self.cursor = self.cursorsLeft[index + delta]

      # SINGLE HAND PRACTICE (RIGHT)
      elif (self.activeHands == ACTIVE_HANDS_RIGHT) :
        index = self.getCursorsRightPointer(self.getCursor())

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
    Jumps to the next cursor, wraps if any loop applies.
    
    The jump takes into account the active hands.
    
    The function takes into account the practice hands (both or single).
    In single hand practice mode, it jumps automatically to the 'correct' next
    cursor.
    
    Equivalent to 'cursorStep(1)', but takes the loop into account.
    """

    if self.loopEnable :
      if ((self.cursor + 1) <= self.loopEnd) :
        self.cursorStep(1)
      else : 
        self.cursor = self.loopStart

    else :
      self.cursorStep(1)


    # Combo tracking
    # TODO: move outside the Score object.
    # Return a status instead
    self.comboCount += 1
    if (self.comboCount > self.comboHighestSession) :
      self.comboHighestSession = self.comboCount

    if (self.comboCount > self.comboHighestAllTime) :
      self.comboHighestAllTime = self.comboCount



  # ---------------------------------------------------------------------------
  # METHOD Score.cursorAlignToActiveHand()
  # ---------------------------------------------------------------------------
  def cursorAlignToActiveHand(self, hand, direction = 0) :
    """
    Sets the cursor to the closest location that is compatible with the requested
    hand practice mode.

    When the user changes the active hands from 'both hands' to 'single hand' practice,
    the cursor might becoome invalid.
    E.g.: left hand practice requested, but there is no note played on the left hand at 
    the current cursor. 
    
    There are different strategies to find a candidate:
    If direction == 0, it looks for the closest compatible location (default behaviour)
    If direction > 0, it looks for a compatible location after the current location.
    If direction < 0, it looks for a compatible location before the current location.
    'compatible location' meaning 'location where a note of the active hand is played'.
    
    """
    
    prevCursor = self.getCursor()

    if (hand == LEFT_HAND) :
      
      # TODO: guards needed here. There are case where the sets can be void.
      if (direction > 0) : 
        subList = [x >= self.cursor for x in self.cursorsLeft]
        self.cursor = subList[0]

      elif (direction < 0) : 
        subList = [x <= self.cursor for x in self.cursorsLeft]
        self.cursor = subList[-1]

      else :
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

      elif (direction < 0) : 
        subList = [x <= self.cursor for x in self.cursorsRight]
        self.cursor = subList[-1]

      else :
        minIndex = 0
        dist = abs(self.cursor - self.cursorsRight[0])
        for (index, cursorRight) in enumerate(self.cursorsRight[1:]) :
          if (abs(self.cursor - cursorRight) < dist) :
            dist = abs(self.cursor - cursorRight)
            minIndex = index+1
        self.cursor = self.cursorsRight[minIndex]
      
    delta = self.getCursor() - prevCursor
    if (delta > 0) :
      print(f"[DEBUG] Cursor had to be adjusted because not aligned with the active hand (+{delta})")
    elif (delta < 0) :
      print(f"[DEBUG] Cursor had to be adjusted because not aligned with the active hand ({delta})")
    else :
      pass



  # ---------------------------------------------------------------------------
  # METHOD Score.setLoopStart()
  # ---------------------------------------------------------------------------
  def setLoopStart(self) :
    """
    Sets the beginning of the loop at the current cursor.
    
    If the end of the loop is already defined, this function also enables
    the loop practice mode.
    """
    
    # Loop end is not yet defined
    if (self.loopEnd == -1) :
      self.loopStart = self.getCursor()
      print(f"[NOTE] Start of loop set at {self.loopStart+1}")

    else :
      if (self.getCursor() < self.loopEnd) :
        self.loopStart = self.getCursor()
        self.loopEnable = True
        print(f"[NOTE] Loop is now set: start = {self.loopStart+1} / end = {self.loopEnd+1}")



  # ---------------------------------------------------------------------------
  # METHOD Score.setLoopEnd()
  # ---------------------------------------------------------------------------
  def setLoopEnd(self) :
    """
    Sets the end of the loop at the current cursor.
    
    If the beginning of the loop is already defined, this function also enables
    the loop practice mode.
    """
    
    # Loop start is not yet defined
    if (self.loopStart == -1) :
      self.loopEnd = self.getCursor()
      print(f"[NOTE] End of loop set at {self.loopEnd+1}")

    else :
      if (self.getCursor() > self.loopStart) :
        self.loopEnd = self.getCursor()
        self.loopEnable = True
        self.cursor = self.loopStart
        print(f"[NOTE] Loop is now set: start = {self.loopStart+1} / end = {self.loopEnd+1}")
  


  # ---------------------------------------------------------------------------
  # METHOD Score.clearLoop()
  # ---------------------------------------------------------------------------
  def clearLoop(self) :
    """
    Clears the loop information, disables the loop practice mode.
    """
    self.loopStart = -1
    self.loopEnd = -1
    self.loopEnable = False
    print("[NOTE] Loop cleared.")



  # ---------------------------------------------------------------------------
  # METHOD Score.toggleBookmark()
  # ---------------------------------------------------------------------------
  def toggleBookmark(self) :
    """
    Adds/removes a bookmark at the current cursor.
    """

    # Is it an existing bookmark?
    if self.cursor in self.bookmarks :
      self.bookmarks = [x for x in self.bookmarks if (x != self.cursor)]
      print(f"[NOTE] Bookmark removed at cursor {self.getCursor()+1}")
    
    # New bookmark
    else :
      print(f"[NOTE] Bookmark added at cursor {self.getCursor()+1}")
      self.bookmarks.append(self.cursor)
      self.bookmarks.sort()

    self.hasUnsavedChanges = True



  # ---------------------------------------------------------------------------
  # METHOD Score.gotoNextBookmark()
  # ---------------------------------------------------------------------------
  def gotoNextBookmark(self) :
    """
    Sets the cursor to the next closest bookmark.
    Does nothing if there are no bookmarks.
    """
    
    if (len(self.bookmarks) > 0) :
      
      # TODO: the set has to be restricted further in single hand practice
      tmp = [x for x in self.bookmarks if (x > self.cursor)]
      if (len(tmp) > 0) :
        
        if (self.activeHands == ACTIVE_HANDS_LEFT) :
          self.setCursor(tmp[0], ignoreActiveHand = True)
          if not(tmp[0] in self.cursorsLeft) :
            print(f"[WARNING] Bookmark #{self.bookmarks.index(tmp[0])} has nothing on the left hand.")
        
        elif (self.activeHands == ACTIVE_HANDS_RIGHT) :
          self.setCursor(tmp[0], ignoreActiveHand = True)
          if not(tmp[0] in self.cursorsRight) :
            print(f"[WARNING] Bookmark #{self.bookmarks.index(tmp[0])} has nothing on the right hand.")
        
        else :
          self.setCursor(tmp[0])
      
      
      else :
        print(f"[NOTE] Last bookmark reached")
    


  # ---------------------------------------------------------------------------
  # METHOD Score.gotoNextBookmark()
  # ---------------------------------------------------------------------------
  def gotoPreviousBookmark(self) :
    """
    Sets the cursor to the previous closest bookmark.
    Does nothing if there are no bookmarks.
    """

    if (len(self.bookmarks) > 0) :
      tmp = [x for x in self.bookmarks if (x < self.cursor)]
      if (len(tmp) > 0) :

        if (self.activeHands == ACTIVE_HANDS_LEFT) :
          self.setCursor(tmp[-1], ignoreActiveHand = True)
          if not(tmp[-1] in self.cursorsLeft) :
            print(f"[WARNING] Bookmark #{self.bookmarks.index(tmp[-1])} has nothing on the left hand.")
        
        elif (self.activeHands == ACTIVE_HANDS_RIGHT) :
          self.setCursor(tmp[-1], ignoreActiveHand = True)
          if not(tmp[-1] in self.cursorsRight) :
            print(f"[WARNING] Bookmark #{self.bookmarks.index(tmp[-1])} has nothing on the right hand.")

        else :
          self.cursor = tmp[-1]
      
      
      else :
        print(f"[NOTE] First bookmark reached")



  # ---------------------------------------------------------------------------
  # METHOD Score.isBookmarked()
  # ---------------------------------------------------------------------------
  def isBookmarked(self) :
    """
    Returns True if the current position in the score is bookmarked.
    """
    return (self.cursor in self.bookmarks)
  


  # ---------------------------------------------------------------------------
  # METHOD Score.getTeacherNotes()
  # ---------------------------------------------------------------------------
  def getTeacherNotes(self) :
    """
    Returns the list of all notes that must be pressed at the current cursor
    location in the score.
    
    Only notes that are pressed at this very cursor are returned.
    The notes that were pressed before and held up to the current cursor are
    not included.
    """
    
    if (self.cachedCursor == self.cursor) :
      return self.cachedTeacherNotes
    
    else :
      self._updateTeacherNotes()
      self.cachedCursor = self.cursor
      self.cachedTeacherNotes = self.teacherNotes
      
      return self.teacherNotes



  # ---------------------------------------------------------------------------
  # METHOD Score.resetCache()
  # ---------------------------------------------------------------------------
  def resetCache(self) :
    """
    Resets the cache of teacher notes.
    """
    
    self.cachedCursor = -1



  # ---------------------------------------------------------------------------
  # METHOD Score._updateTeacherNotes()
  # ---------------------------------------------------------------------------
  def _updateTeacherNotes(self) :
    """
    Builds the list <teacherNotes> of current expected notes to be played at 
    the current cursor.
    """
    
    # Reset the play attributes of the previous notes before deleting them.
    # Note attributes are used for the display and the arbiter.
    for noteObj in self.teacherNotes :
      noteObj.visible = True
      noteObj.sustained = False
      noteObj.inactive = False

    self.teacherNotes = []
    
    # Loop on all notes in the score
    for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
      for (staffIndex, _) in enumerate(self.pianoRoll) :
        for noteObj in self.pianoRoll[staffIndex][pitch] :

          # Detect a note pressed at this timecode
          if (noteObj.startTime == self.getCurrentTimecode()) :
            
            # SINGLE HAND PRACTICE
            # Adds the notes of the inactive hand to the list.
            # Sets their "inactive" property to "True" so that it is displayed with the appropriate color.
            if ((self.activeHands == ACTIVE_HANDS_LEFT) and (staffIndex == RIGHT_HAND)) :
              noteObj.inactive = True
              self.teacherNotes.append(noteObj)

            elif ((self.activeHands == ACTIVE_HANDS_RIGHT) and (staffIndex == LEFT_HAND)) :
              noteObj.inactive = True
              self.teacherNotes.append(noteObj)

            else :
              self.inactive = False
              self.teacherNotes.append(noteObj)

          # Detect a note held at this timecode
          if ((self.getCurrentTimecode() > noteObj.startTime) and (self.getCurrentTimecode() <= noteObj.stopTime)) :
            noteObj.sustained = True
            self.teacherNotes.append(noteObj)

    if (len(self.teacherNotes) == 0) :
      print(f"[WARNING] Corrupted database: timecode is listed (t = {self.getCurrentTimecode()}), but no note was found starting at that moment.")



  # ---------------------------------------------------------------------------
  # METHOD Score.getLookaheadNotes()
  # ---------------------------------------------------------------------------
  def getLookaheadNotes(self) :
    """
    todo
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
    todo
    """
    
    print("todo!")



  # ---------------------------------------------------------------------------
  # METHOD Score.search(noteList, direction)
  # ---------------------------------------------------------------------------
  def search(self, noteList, direction = 1) :
    """
    Sets the cursor to the next location where the given query notes appear 
    simultaneously in the score.
    
    Direction of search (before or after the current location) can be specified.
    
    TODO: does it include sustained notes?
    """

    if (direction >= 0) :
      if (self.activeHands == ACTIVE_HANDS_RIGHT) :
        timecodeSearchField = [x > self.cursor for x in self.cursorsRight]
      elif (self.activeHands == ACTIVE_HANDS_LEFT) :
        timecodeSearchField = [x > self.cursor for x in self.cursorsRight]
      else :
        # TODO: check the boundaries
        timecodeSearchField = [x for x in range(self.cursor+1, self.scoreLength)]
    
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
            if (noteObj.startTime == self.noteOnTimecodes["LR"][cursorTry]) :
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
      arbiterSuspendReq = True
      arbiterPitchListHold = pitchList.copy()
      return (arbiterSuspendReq, arbiterPitchListHold)
    
    else :
      print("[NOTE] Could not find the current MIDI notes in the score!")
      return (False, [])


  # ---------------------------------------------------------------------------
  # METHOD Score.toggleLeftHandPractice()
  # ---------------------------------------------------------------------------
  def toggleLeftHandPractice(self) :
    """
    Activates/deactivates the left hand practice.
    """

    if ((self.activeHands == ACTIVE_HANDS_BOTH) or (self.activeHands == ACTIVE_HANDS_RIGHT)) :
      self.activeHands = ACTIVE_HANDS_LEFT
      self.cursorAlignToActiveHand(LEFT_HAND)
    
    else :
      self.activeHands = ACTIVE_HANDS_BOTH

    self.resetCache()



  # ---------------------------------------------------------------------------
  # METHOD Score.toggleRightHandPractice()
  # ---------------------------------------------------------------------------
  def toggleRightHandPractice(self) :
    """
    Activates/deactivates the right hand practice.
    """
      
    if ((self.activeHands == ACTIVE_HANDS_BOTH) or (self.activeHands == ACTIVE_HANDS_LEFT)) :
      self.activeHands = ACTIVE_HANDS_RIGHT
      self.cursorAlignToActiveHand(RIGHT_HAND)
    
    else :
      self.activeHands = ACTIVE_HANDS_BOTH

    self.resetCache()



  # ---------------------------------------------------------------------------
  # METHOD Score.toggleNoteHand(noteObject)
  # ---------------------------------------------------------------------------
  def toggleNoteHand(self, noteObj) :
    """
    Toggles the hand assigned to the note passed as argument and update the score
    accordingly.
    
    If the note is assigned to the left hand, it will now be assigned to the right
    hand and vice versa.
    
    NOTES
    Assigning a note from the left to the right hand has more impact than just 
    editing the <hand> property of the note object. 
    Among others, the list of cursors must be edited too.
    """
    
    if (noteObj.hand == LEFT_HAND) :
      
      noteObj.hand = RIGHT_HAND

      if (noteObj.startTime in self.noteOnTimecodes["L"]) :
        
        # Note: 'remove' only deletes one occurrence of the element.
        self.noteOnTimecodes["L"].remove(noteObj.startTime)
        self.noteOnTimecodes["R"].append(noteObj.startTime)
        self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
        
        # Note: <self.noteOnTimecodes["LR_full"]> remains invariant in the process
        # Note: <self.noteOnTimecodes["LR"]> remains invariant in the process

      else :
        print("[INTERNAL ERROR] Score.toggleNoteHand: database is not consistent.")
        print("The timecode of the note you are trying to remove is not in the list of timecodes!")
        exit()

    elif (noteObj.hand == RIGHT_HAND) :
      
      noteObj.hand = LEFT_HAND

      if (noteObj.startTime in self.noteOnTimecodes["R"]) :
        
        # Note: 'remove' only deletes one occurrence of the element.
        self.noteOnTimecodes["R"].remove(noteObj.startTime)
        self.noteOnTimecodes["L"].append(noteObj.startTime)
        self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
        
        # Note: <self.noteOnTimecodes["LR_full"]> remains invariant in the process
        # Note: <self.noteOnTimecodes["LR"]> remains invariant in the process

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
    assert(lengthLR == (lengthL + lengthR))
    


  # ---------------------------------------------------------------------------
  # METHOD Score.importFromFile(fileName)
  # ---------------------------------------------------------------------------
  def importFromFile(self, inputFile) :
    """
    Loads the internal piano roll from an external file (.mid or .pr)
    """
  
    if (os.path.splitext(inputFile)[-1] == ".mid") :
      self._importFromMIDIFile(inputFile)
    elif (os.path.splitext(inputFile)[-1] == ".pr") :
      self._importFromPrFile(inputFile)
    else :
      print("[ERROR] This file extension is not recognized.")
      exit()

    self.hasUnsavedChanges = False



  # ---------------------------------------------------------------------------
  # METHOD Score.importFromMIDIFile(midiFileName)
  # ---------------------------------------------------------------------------
  def _importFromMIDIFile(self, midiFile) :
    """
    Builds the internal score structure from a MIDI file.
    
    A score is stored in the object in the <pianoRoll> variable and looks like:
    pianoRoll.noteArray[t][p] = [note0, note1, ...]
    
    It is basically the list of all notes played on track <t>, on pitch <p>. 
    
    Each element of the list is a Note object.
    
    A Note() object has attributes:
    - noteXXX.start/.end (integer) : timestamp of its beginning/end
    - noteXXX.hand (string: "l", "r" or ""): hand used to play the note.
    Please refer to note.py for more information on the Note objects.
    
    pianoRoll.noteOntimecodes[t] = [t0, t1, ...]
    """

    print("[INFO] Processing .mid file... ", end = "")
    startTime = time.time()

    mid = mido.MidiFile(midiFile)

    # TODO: give more flexibility when opening MIDI files
    # It is assumed here that the MIDI file has 2 tracks.
    # But in general MIDI files might contain more than that.
    # And in general, the user might want to map specific tracks to the staffs
    # and not only track 0 and 1.
    # print(f"[NOTE] [MIDI import] Tracks found: {len(mid.tracks)}")
    
    # Only 2 staves are supported for now.
    # The app focuses on piano practice: there is no plan to support more than
    # 2 staves in the near future.
    if (len(mid.tracks) > 2) :
      print("[WARNING] The MIDI file has more than 2 tracks. Tracks beyond the first 2 will be ignored.")
    self.nStaffs = 2
    
    # Allocate outputs
    self.pianoRoll = [[[] for _ in range(128)] for _ in range(self.nStaffs)]
    self.noteOnTimecodes = {"L": [], "R": [], "LR": [], "LR_full": []}

    nNotes = 0; noteDuration = 0
    
    # Each note is assigned to a unique identifier (simple counter)
    id = 0

    # Loop on the tracks, decode the MIDI messages
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
                print(f"[WARNING] Ambiguous note at t = {currTime} ({note.getFriendlyName(pitch)}): a keypress overlaps a hanging keypress on the same note.")

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
            self.pianoRoll[trackNumber][pitch].append(note.Note(pitch, hand = trackNumber, noteIndex = insertIndex, startTime = currTime, stopTime = NOTE_END_UNKNOWN))
            
            # Append the timecode of this keypress
            # TODO: not sure this check on every single note is efficient
            # if not(currTime in self.noteOntimecodes[trackNumber]) : 
            #   self.noteOntimecodes[trackNumber].append(currTime)
            if (trackNumber == LEFT_HAND) :
              self.noteOnTimecodes["L"].append(currTime)
            elif (trackNumber == RIGHT_HAND) :
              self.noteOnTimecodes["R"].append(currTime)
            else :
              print("[INTERNAL ERROR] Invalid track number.")

            self.noteOnTimecodes["LR_full"].append(currTime)
          
          # First note with this pitch
          else :
            
            # Append the new note to the list
            # Its duration is unknown for now, so set its endtime to NOTE_END_UNKNOWN = -1
            insertIndex = len(self.pianoRoll[trackNumber][pitch])
            self.pianoRoll[trackNumber][pitch].append(note.Note(pitch, hand = trackNumber, noteIndex = insertIndex, startTime = currTime, stopTime = NOTE_END_UNKNOWN))
            
            # Append the timecode of this keypress
            # if not(currTime in self.noteOntimecodes[trackNumber]) : 
            #   self.noteOntimecodes[trackNumber].append(currTime)

            if (trackNumber == LEFT_HAND) :
              self.noteOnTimecodes["L"].append(currTime)
            elif (trackNumber == RIGHT_HAND) :
              self.noteOnTimecodes["R"].append(currTime)
            else :
              print("[INTERNAL ERROR] Invalid track number.")

            self.noteOnTimecodes["LR_full"].append(currTime)

        # Keyrelease event ----------------------------------------------------
        # NOTE: in some files, 'NOTE OFF' message is mimicked using a 'NOTE ON' with null velocity.
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
          #   print(f"[WARNING] [MIDI import] MIDI note {pitch} ({note.getFriendlyName(pitch)}) has null duration (start time = stop time = {noteObj.startTime})")
          #   self.pianoRoll[trackNumber][pitch].pop()



        # Others --------------------------------------------------------------
        # Other MIDI events are ignored.


    # Tidy up:
    # - sort the timecodes by ascending values
    # - remove duplicate entries
    self.noteOnTimecodes["L"].sort(); self.noteOnTimecodes["R"].sort()
    self.noteOnTimecodes["LR_full"].sort()

    self.noteOnTimecodes["LR"] = set(self.noteOnTimecodes["LR_full"])
    self.noteOnTimecodes["LR"] = list(self.noteOnTimecodes["LR"])
    self.noteOnTimecodes["LR"].sort()

    # Build <cursorsLeft> and <cursorsRight>
    self._buildCursorsLR()


    # Merge note ON time codes from both staves
    # timecodesMerged = [item for sublist in self.noteOntimecodes for item in sublist]    # What the hell is that?
    # timecodesMerged = list(set(timecodesMerged))
    # self.noteOntimecodesMerged = sorted(timecodesMerged)
    
    # The variable pointing in the <noteOntimecodesMerged> is called the "cursor" of the score.
    # This section lists the values of the cursor for which a noteOn event occured 
    # specifically on one hand or the other.
    # This is needed for the single hand practice mode.
    # self.cursorsLeft = []; self.cursorsRight = []
    # for (cursor, timecode) in enumerate(self.noteOntimecodesMerged) :
    #   if (timecode in self.noteOntimecodes[RIGHT_HAND]) :
    #     self.cursorsRight.append(cursor)

    #   if (timecode in self.noteOntimecodes[LEFT_HAND]) :
    #     self.cursorsLeft.append(cursor)

    # Estimate average note duration (needed for the piano roll display)
    self.avgNoteDuration = noteDuration/nNotes
    
    self.scoreLength = len(self.noteOnTimecodes["LR"])
    self.cursorMax = self.scoreLength-1
    
    print("OK")

    # DEBUG
    print(f"[DEBUG] Score length: {self.scoreLength} steps")


    stopTime = time.time()
    print(f"[NOTE] Loading time: {stopTime-startTime:.2f}s")
    
    

  # ---------------------------------------------------------------------------
  # METHOD Score._importFromPrFile(fileName)
  # ---------------------------------------------------------------------------
  def _importFromPrFile(self, pianoRollFile) :
    """
    Imports the score and all metadata (finger, hand, bookmarks etc.)
    from a .pr file (JSON) and restores the last session.
    """
    
    startTime = time.time()
    with open(pianoRollFile, "r") as fileHandler :
      importDict = json.load(fileHandler)

    # Read the revision
    versionMatch = re.match(r"^v(\d+)\.(\d+)$", importDict["revision"])
    if versionMatch :
      (majorRev, minorRev) = (int(versionMatch.group(1)), int(versionMatch.group(2)))

    else :
      print(f"[WARNING] No version could be read from the .pr file. Is it corrupted?")
      # At that point, the rest of the parsing might fail.

    # if (f"v{REV_MAJOR}.{REV_MINOR}" != importDict["revision"]) :
    #   print(f"[WARNING] [.pr import] Piano roll file was made in version {importDict['revision']}. Current version is v{REV_MAJOR}.{REV_MINOR}")

    # Safe loading feature
    safeDict = {
      "revision"              : "v0.0",
      "nStaffs"               : 2,
      "avgNoteDuration"       : 100.0,
      "cursor"                : 0,
      "cursorsLeft"           : [],
      "cursorsRight"          : [],
      "bookmarks"             : [],
      "activeHands"           : "LR",
      "comboHighestAllTime"   : 0
    }
    
    for currKey in safeDict :
      if currKey in importDict :
        safeDict[currKey] = importDict[currKey]

    # Load the properties of the score from the dictionary
    self.nStaffs                = safeDict["nStaffs"]
    self.avgNoteDuration        = safeDict["avgNoteDuration"]
    self.cursor                 = safeDict["cursor"]
    self.bookmarks              = safeDict["bookmarks"]
    self.activeHands            = safeDict["activeHands"]
    self.comboHighestAllTime    = safeDict["comboHighestAllTime"]

    # self.noteOntimecodes        = safeDict["noteOntimecodes"]
    # self.noteOntimecodesMerged  = safeDict["noteOntimecodesMerged"]
    # self.cursorsLeft            = safeDict["cursorsLeft"]
    # self.cursorsRight           = safeDict["cursorsRight"]

    # TODO: import the scales
    # TODO: import the loops

    # -----------------------------
    # Pianoroll import - v0.X style
    # -----------------------------
    if (majorRev == 0) :
      print("[INFO] Importing old school .pr file (versions v0.X)")

      # Note() objects were converted to a dictionary. Convert them back to a Note object
      self.pianoRoll = [[[] for noteList in trackList] for trackList in importDict["pianoRoll"]]

      for track in range(self.nStaffs) :
        for pitch in GRAND_PIANO_MIDI_RANGE :
          for noteDict in importDict["pianoRoll"][track][pitch] :
            noteObj = note.Note(noteDict['pitch'])
            
            for noteAttr in noteObj.__dict__ :
              setattr(noteObj, noteAttr, noteDict[noteAttr])
            
            self.pianoRoll[track][pitch].append(noteObj)



    # ---------------------------------
    # Pianoroll import - v1.0 and above
    # ---------------------------------
    # From version 1.0, the pianoroll is flattened.
    # From version 1.3, the variables:
    # - <noteOntimecodes>, 
    # - <noteOntimecodesMerged>, 
    # - <cursorsLeft>, 
    # - <cursorsRight>
    # are rebuilt from the notes properties in the pianoroll.
    else :
      
      self.pianoRoll = [[[] for _ in range(128)] for _ in range(self.nStaffs)]
      self.noteOnTimecodes = {"L": [], "R": [], "LR": [], "LR_full": []}

      noteCount = 0
      for noteObjImported in importDict["pianoRoll"] :
        
        noteObj = note.Note(noteObjImported["pitch"])
        
        # List of all properties in a Note object, make a dictionary out of it.
        noteAttrDict = noteObj.__dict__.copy()
        
        # TODO: not sure why the ID had to be treated differently
        # noteObj.id = noteObjImported["id"]; del noteAttrDict["id"]

        # Loop on the attributes of the Note object
        for noteAttr in noteAttrDict :
          
          # CHECK: rectify inconsistencies between <pitch> and <name> attributes.
          if (noteAttr == "name") :
            expectedNoteName = note.getFriendlyName(noteObjImported["pitch"])
            actualNoteName   = noteObjImported["name"]
            if (expectedNoteName != actualNoteName) :
              print(f"[WARNING] Note ID {noteObj.id}: MIDI pitch ({noteObjImported['pitch']}) and note name ({actualNoteName}) do not agree. The pitch takes precedence, name will be overwritten to {expectedNoteName}.")
          
          # Call the attribute by its name (as string), and assign it.
          setattr(noteObj, noteAttr, noteObjImported[noteAttr])
        
        
        self.pianoRoll[noteObjImported["hand"]][noteObjImported["pitch"]].append(noteObj)
        
        if (noteObjImported["hand"] == LEFT_HAND) :
          self.noteOnTimecodes["L"].append(noteObj.startTime)
        elif (noteObjImported["hand"] == RIGHT_HAND) :
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

      # Build <cursorsLeft> and <cursorsRight>
      self._buildCursorsLR()

      self.scoreLength = len(self.noteOnTimecodes["LR"])
      self.cursorMax = self.scoreLength-1

      # DEBUG
      print(f"[DEBUG] Left hand cursors   : {len(self.cursorsLeft)} / ref: {len(safeDict['cursorsLeft'])}")
      print(f"[DEBUG] Right hand cursors  : {len(self.cursorsRight)} / ref: {len(safeDict['cursorsRight'])}")
      
      print(f"[DEBUG] {noteCount} notes read from .pr file.")
      print(f"[DEBUG] Score length: {self.scoreLength} steps")


    stopTime = time.time()
    print(f"[NOTE] Loading time: {stopTime-startTime:.2f}s")



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
    exportDict["bookmarks"]             = self.bookmarks
    exportDict["activeHands"]           = self.activeHands
    exportDict["comboHighestAllTime"]   = self.comboHighestAllTime

    # TODO: export the scales
    # exportDict["scale"] = self.scale

    noteCount = 0
    exportDict["pianoRoll"] = []
    for notesInTrack in self.pianoRoll :
      for notesInPitch in notesInTrack :
        for noteObj in notesInPitch :
          noteCount += 1
          exportDict["pianoRoll"].append(noteObj.__dict__)

    with open(pianoRollFile, "w") as fileHandler :
      json.dump(exportDict, fileHandler, indent = 4)

    currTime = datetime.datetime.now()
    print(f"[DEBUG] {noteCount} notes written in .pr file.")
    print(f"[NOTE] Saved to '{pianoRollFile}' at {currTime.strftime('%H:%M:%S')}")



  # ---------------------------------------------------------------------------
  # METHOD Score.hasUnsavedChanges()
  # ---------------------------------------------------------------------------
  def hasUnsavedChanges(self) :
    """
    Returns True if there are any unsaved changes in the current session.
    """
    
    print("TODO")


  
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
    print("TODO")



  # ---------------------------------------------------------------------------
  # METHOD Score.toggleRehearsalMode()
  # ---------------------------------------------------------------------------
  def toggleRehearsalMode(self) :
    """
    Turns ON/OFF the rehearsal mode, i.e. enable/disable progressing in the score
    based on the MIDI input.
    
    An arbiter inspects the keyboard input, looks if it matches with the score, and 
    decides whether to move forward or stay in the current location.
    
    This function toggles the arbiter. 
    When off, no more progress in the score is allowed.
    """
    
    self.progressEnable = not(self.progressEnable)
    print("[NOTE] Rehearsal mode will be available in a future release.")





