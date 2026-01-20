# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : fingerSelector
# File name     : fingerSelector.py
# File type     : Python script (Python 3)
# Purpose       : widget to edit the 'finger' property of a note.
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
from src.commons import *
import src.widgets.widget as widget
import src.text as text

# Standard libraries
import pygame



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class FingerSelector(widget.Widget) :

  """
  FINGER_SELECTOR object

  Class definition for the fingerSelector widget.
  
  The fingerSelector viewer displays shows the UI element interacting with
  the user to define the finger to use on a selected note.
  
  It also provides some shorthand functions:
  - auto-increment
  - fingersatz recommendations for chords
  
  The selector is not shown by default, and gets invoked as a key is selected 
  on screen for edition.

  The FingerSelector class derives from the Widget class.
  """

  def __init__(self, top, loc) :
    
    # Call the Widget init method
    super().__init__(top, loc)

    self.name = "finger selector"

    self.visible = False

    # -1 = nothing is selected
    #  0 = left hand, finger 5
    #  1 = left hand, finger 4
    # ...
    #  4 = left hand, finger 1
    #  5 = left hand, finger undefined
    #  6 = right hand, finger undefined
    #  7 = right hand, finger 1
    # ...
    # 11 = right hand, finger 5
    self.sel    = -1
    self.hand   = FingerSel_hand.UNDEFINED
    self.finger = FingerSel_finger.UNDEFINED

    self.activeNotes = []
    
    self.editedNote   = None    # Reference to the note being edited
    self.editedIndex  = -1      # Index of the note being edited in 'activeNotes' array
    self.editedCursor = -1      # Cursor value where the note was requested to be edited



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.render()
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Renders the finger selector widget on screen.
    """

    # Hide the widget as soon as the cursor changes
    # The cursor changing is a sign that the finger edition is done.
    if (self.top.widgets[WIDGET_ID_SCORE].getCursor() != self.editedCursor) :
      self.editedNote   = None
      self.editedIndex  = -1
      self.editedCursor = -1
      self.visible      = False

    if (self.visible) :
      (locX, locY) = self.loc  
      text.render(self.top.screen, f"FINGER: ", self.loc, 2, FINGER_SELECTOR_TEXT_COLOR)
      
      for (i, label) in enumerate(["5 ", "4 ", "3 ", "2 ", "1 ", "- ", "- ", "1 ", "2 ", "3 ", "4 ", "5 "]) :
        if (i <= 5) :
          if (self.sel == i) :
            # Note: 96 = 8*10 + 8*2, i.e. 8 x char size + 8 x space in-between
            text.render(self.top.screen, label, (locX + 96 + (i*23), locY), 2, FINGER_SELECTOR_TEXT_COLOR_SEL_L)
          else :
            text.render(self.top.screen, label, (locX + 96 + (i*23), locY), 2, FINGER_SELECTOR_TEXT_COLOR_L)

        else :
          if (self.sel == i) :
            text.render(self.top.screen, label, (locX + 96 + (i*23), locY), 2, FINGER_SELECTOR_TEXT_COLOR_SEL_R)
          else :
            text.render(self.top.screen, label, (locX + 96 + (i*23), locY), 2, FINGER_SELECTOR_TEXT_COLOR_R)

      x0 = locX + 96 - 7
      yTop = locY + 3; yBottom = locY + 12
      for i in range(13) :
        if (i == 6) :
          pygame.draw.line(self.top.screen, FINGER_SELECTOR_SEP_LINE_COLOR, (x0 + (i*23), yTop-8), (x0 + (i*23), yBottom+6), 1)
        else :
          pygame.draw.line(self.top.screen, FINGER_SELECTOR_SEP_LINE_COLOR, (x0 + (i*23), yTop), (x0 + (i*23), yBottom), 1)
    


  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._getActiveNotes()                          [PRIVATE]
  # ---------------------------------------------------------------------------
  def _getActiveNotes(self) :
    """
    Requests the list of active notes in the Score from the 'Score' widget.
    Sort the notes in ascending pitch order.

    Result is stored in 'activeNotes'.

    This function is usually called during the processing of a 'tab' keypress.
    """
    
    includeSustainedNotes = True

    # Read the cursor
    cursor = self.top.widgets[WIDGET_ID_SCORE].getCursor()

    # If the cursor has changed since the last request, the process has to be
    # done again
    if (cursor != self.editedCursor) :
      self.editedCursor = cursor

      self.activeNotes = self.top.widgets[WIDGET_ID_SCORE].getTeacherNotes(includeSustainedNotes)
      if self.activeNotes :
        self.activeNotes.sort(key = lambda N: N.pitch)



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._highlightNext()                           [PRIVATE]
  # ---------------------------------------------------------------------------
  def _highlightNext(self) :
    """
    Highlights the next active note (in ascending pitch order) currently shown 
    on the keyboard.
    Wraps around after the last note.
    """
    
    self.visible = True
    self._getActiveNotes()

    if self.activeNotes :
      if (self.editedNote == None) :
        self.highlightByIndex(0)
      else :
        self.highlightByIndex((self.editedIndex + 1) % len(self.activeNotes))



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._highlightPrevious()                       [PRIVATE]
  # ---------------------------------------------------------------------------
  def _highlightPrevious(self) :
    """
    Highlights the previous active note (in ascending pitch order) currently 
    shown on the keyboard.
    Wraps around after the first note.
    """
    
    self.visible = True
    self._getActiveNotes()

    if self.activeNotes :
      if (self.editedNote == None) :
        self.highlightByIndex(len(self.activeNotes)-1)
      else :
        self.highlightByIndex((self.editedIndex - 1) % len(self.activeNotes))



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._highlightClear()                          [PRIVATE]
  # ---------------------------------------------------------------------------
  def _highlightClear(self) :
    """
    Clears the current highlighted note.
    """
    
    self.editedNote   = None
    self.editedIndex  = -1
    self.editedCursor = -1



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.highlightByObject()
  # ---------------------------------------------------------------------------
  def highlightByObject(self, noteObj) :
    """
    Defines the hightlighted note using a reference to a note object.
    The note must be in the 'activeNotes' property (you can only edit the finger
    of a note that is shown on screen for simplicity)

    Also:
    - The "highlight" attribute of the note gets set to True.
    - The selector widget turns ON and tracks the selected note.
    
    This function is usually called from the click event handler.

    Reference to notes that are not in 'activeNotes' are ignored.
    """
    
    self._getActiveNotes()
    for (i, N) in enumerate(self.activeNotes) :
      if (noteObj.id == N.id) :
        self.highlightByIndex(i)
        break



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.highlightByIndex()
  # ---------------------------------------------------------------------------
  def highlightByIndex(self, index) :
    """
    Highlights the note on keyboard using an index (given as argument) that 
    points in the 'activeNotes' array.

    Also:
    - The 'highlight' attribute of the note is set to True.
    - The selector widget turns ON and tracks the selected note.

    Out of range indices are ignored.
    """

    if not(self.visible) :
      self.visible = True

    if ((index >= 0) and (index < len(self.activeNotes))) :
      if (self.editedNote != None) :
        self.editedNote.highlight = False
    
      self.editedIndex = index
      self.editedNote = self.activeNotes[self.editedIndex]
      self.editedNote.highlight = True
      self._setSelector(self.editedNote.finger, self.editedNote.hand)
    else :
      print("[WARNING] FingerSelector.highlightByIndex(): ignoring out of range index")



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.highlightReset()
  # ---------------------------------------------------------------------------
  def highlightReset(self) :
    """
    Turns off the selector Widget
    Sets the 'highlight' attribute of the note to False.
    """

    print("Function is TODO.")



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.assign()
  # ---------------------------------------------------------------------------
  def assign(self, finger, hand = NOTE_UNDEFINED_HAND) :
    """
    Description is TODO.
    """

    if self.activeNotes :
      print("[DEBUG] Method 'FingerSelector.assign()' just woke up.")
    else :
      print("To assign a finger to a note, please select the note you want to edit first.")



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._selectorHitTest()                         [PRIVATE]
  # ---------------------------------------------------------------------------
  def _selectorHitTest(self, clickCoord) :
    """
    Indicates if the mouse click coordinates hit the finger selector widget.

    Returns (status, index) where:
    - 'status' returns the test result (True/False)
    - 'index' returns the index of the element that has been hit
    """

    (locX, locY) = self.loc

    (clickX, clickY) = clickCoord
    x0 = locX + 96 - 7
    yTop    = locY + 3; 
    yBottom = locY + 12
    
    # Loop on the members of the widgets
    for i in range(12) :
      xMin = x0 + (i*23) + 1
      xMax = x0 + ((i+1)*23) - 1
      yMin = yTop - 6
      yMax = yBottom + 4

      # If the click is in this current hit box
      if ((clickX >= xMin) and (clickX <= xMax) and (clickY >= yMin) and (clickY <= yMax)) :
        return (True, i)
        
    return (False, -1)
  


  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._selectorSet()                             [PRIVATE]
  # ---------------------------------------------------------------------------
  def _selectorSet(self, finger, hand) :
    """
    Description is TODO.
    """
    
    #self.sel = index
    #finger, hand = (0,0)
    #self.sel = selectorIndex
    print(f"[DEBUG] FingerSelector._onMouseEvent(): you hit the selector (index = {index})")

    if (hand == NOTE_LEFT_HAND) :
      # Default assignment (hand set, finger unknown)
      self.sel = 5
      if (finger in [1,2,3,4,5]) :
        self.sel = 5 - finger
    
    if (hand == NOTE_RIGHT_HAND) :
      self.sel = 6
      if (finger in [1,2,3,4,5]) :
        self.sel = finger + 6
    


  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._selectorGet()                             [PRIVATE]
  # ---------------------------------------------------------------------------
  def _selectorGet(self, index) :
    """
    Returns the (hand, finger) of the current selection on the finger selector.
    """
    
    if (self.currentSel <= 4) :
      return (NOTE_LEFT_HAND, 5-self.currentSel)

    if (self.currentSel == 5) :
      return (NOTE_LEFT_HAND, NOTE_UNDEFINED_FINGER)
      # self.editedNote.hand = ku.LEFT_HAND  => not supported yet
    
    if (self.currentSel == 6) :
      return (NOTE_RIGHT_HAND, NOTE_UNDEFINED_FINGER)
      # self.editedNote.hand = ku.RIGHT_HAND  => not supported yet
    
    if (self.currentSel >= 7) :
      return (NOTE_RIGHT_HAND, self.currentSel - 6)
    
    return (NOTE_UNDEFINED_FINGER, NOTE_UNDEFINED_HAND)
  


  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._onMouseEvent()                          [INHERITED]
  # ---------------------------------------------------------------------------
  def _onMouseEvent(self, button, type) :
    """
    Mouse event callback.
    
    This function is inherited from the Widget class.
    """
    
    if (type == pygame.MOUSEBUTTONDOWN) :
      if (button == MOUSE_LEFT_CLICK) :
        
        # Click on an active note
        (isNoteHit, noteObj) = self.top.widgets[WIDGET_ID_KEYBOARD].clickHitTest(pygame.mouse.get_pos())
        if isNoteHit :
          self.highlightByObject(noteObj)
        
        # Click on the selector
        (isHit, index) = self._selectorHitTest(pygame.mouse.get_pos())
        if isHit :
          self._selectorSet(index)

      elif (button == MOUSE_SCROLL_UP) :
        pass

      elif (button == MOUSE_SCROLL_DOWN) :
        pass



  # ---------------------------------------------------------------------------
  # METHOD FingerSelector._onKeyEvent()                             [INHERITED]
  # ---------------------------------------------------------------------------
  def _onKeyEvent(self, key, type, modifier = "") :
    """
    Function triggered by a keypress.
    """
    
    if (type == pygame.KEYDOWN) :
      
      # SIMPLE KEYPRESS
      if (modifier == "") :
        if (key == pygame.K_KP_0) :
          print("[NOTE] FingerSelector._onKeyEvent(): delete finger, keep current hand")
        elif (key == pygame.K_KP_1) :
          self.assign(finger = 1)
        elif (key == pygame.K_KP_2) :
          self.assign(finger = 2)
        elif (key == pygame.K_TAB) :
          self._highlightNext()
        elif (key == pygame.K_DELETE) :
          print("[NOTE] FingerSelector._onKeyEvent(): delete finger, keep current hand")

      # SHIFT + KEYPRESS
      elif (modifier == "shift") :
        if (key == pygame.K_TAB) :
          self._highlightPrevious()










# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'fingerSelector.py'.")



