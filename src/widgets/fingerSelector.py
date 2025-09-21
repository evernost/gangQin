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
    Renders the finger selection buttons and graphical elements on screen.
    """

    # Hide the widget as soon as the cursor changes
    # A cursor change assumes that the finger edition is done
    if (self.top.widgets[WIDGET_ID_SCORE].getCursor() != self.editedCursor) :
      #self.reset()          # Reset state, remove note hilighting etc.
      self.visible = False



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
    Requests the active notes in the Score from the 'Score' widget.
    Sort the notes in ascending order in 'activeNotes'.

    This function is called during the processing of a 'tab' keypress.
    """
    
    # Read the active notes
    includeSustainedNotes = True
    self.activeNotes = self.top.widgets[WIDGET_ID_SCORE].getTeacherNotes(includeSustainedNotes)
    
    # Read the cursor
    cursor = self.top.widgets[WIDGET_ID_SCORE].getCursor()

    # If the cursor has changed since the last request, the process has to be
    # done again
    if (cursor != self.editedCursor) :
      self.editedCursor = cursor
      if self.activeNotes :
        self.activeNotes.sort(key = lambda N: N.pitch)

        for N in self.activeNotes :
          print(f"- {N.pitch}")

    # Otherwise, just read from cache.
    else :
      print(f"[DEBUG] Reading active notes from cache")



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._highlightNext()                           [PRIVATE]
  # ---------------------------------------------------------------------------
  def _highlightNext(self) :
    """
    Highlights the next active note (in ascending order) currently shown on the 
    keyboard.
    Wraps around after the last note.
    """
    
    self.visible = True
    self._getActiveNotes()

    if self.activeNotes :
      if (self.editedIndex == -1) :
        self.editedIndex = 0
        N = self.activeNotes[self.editedIndex]
        N.highlight = True
        
        self._setSelector(N.finger, N.hand)

      else :
        N = self.activeNotes[self.editedIndex]
        N.highlight = False

        if (self.editedIndex == (len(self.activeNotes)-1)) :
          self.editedIndex = 0
        else :
          self.editedIndex += 1

        N = self.activeNotes[self.editedIndex]
        N.highlight = True



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._highlightPrevious()                       [PRIVATE]
  # ---------------------------------------------------------------------------
  def _highlightPrevious(self) :
    """
    Highlights the previous active note (in ascending order) currently shown on 
    the keyboard.
    Wraps around after the first note.
    """
    
    self.visible = True
    self._getActiveNotes()



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._highlightClear()                          [PRIVATE]
  # ---------------------------------------------------------------------------
  def _highlightClear(self) :
    """
    Clears the current highlighted note.
    """
    
    self.activeNotes = []
    self.activeCursor = -1
    self.activeIndex = -1



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.setEditedNote()
  # ---------------------------------------------------------------------------
  def setEditedNote(self, noteObj, cursor = -1) :
    """
    Defines the note whose properties are shown in the finger selector.
    A cursor value can be stored along with the note so that it is easier to 
    show/hide the widget in a specific context.
    """

    self._setSelector(noteObj.finger, noteObj.hand)
    if (self.editedNote != None) :
      self.editedNote.highlight = False
    
    self.editedNote = noteObj
    self.editedCursor = cursor
    noteObj.highlight = True
    self.visible = True



  # # ---------------------------------------------------------------------------
  # # METHOD: FingerSelector.getEditedNote()
  # # ---------------------------------------------------------------------------
  # def getEditedNote(self) :
  #   """
  #   todo
  #   """
    
  #   return self.editedNote



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.resetEditedNote()
  # ---------------------------------------------------------------------------
  def resetEditedNote(self) :
    """
    todo
    """
    
    self.sel = -1
    self.editedNote.highlight = False
    self.editedNote = None
    self.editedCursor = -1



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._selectorHitTest()                         [PRIVATE]
  # ---------------------------------------------------------------------------
  def _selectorHitTest(self, clickCoord) :
    """
    Indicates if the click's coordinates hit the finger selector.

    Returns (status, index)
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
  # METHOD <FingerSelector.setFingerAutoHighlight>
  # ---------------------------------------------------------------------------
  # def setFingerAutoHighlight(self, fingerNumber, teacherNotes, activeHands) :
  #   """
  #   Takes a finger index, the context. Assigns the finger index to the relevant
  #   note.
  #   """

  #   # Sustained notes are not eligible to the note auto highlight
  #   activeNotes = [x for x in teacherNotes if not(x.sustained)]

  #   # Find a note that does not have a finger assigned yet
  #   if (len(activeNotes) > 1) :
  #     singleHandContent = True
  #     for x in activeNotes[1:] :
  #       if (x.hand != activeNotes[0].hand) :
  #         singleHandContent = False
  #         break
    
  #   else :
  #     singleHandContent = True
    
  #   if ((activeHands != "LR") or singleHandContent) :
      
  #     # Sort by ascending pitch
  #     activeNotes.sort(key = lambda x: x.pitch)
      
  #     # Keep notes not yet assigned
  #     tmp = [x for x in activeNotes if (x.finger == NOTE_UNDEFINED_FINGER)]
      
  #     # Are all notes already assigned to a finger? -> start over
  #     if (len(tmp) == 0) :
  #       print("[DEBUG] Not handled yet.")
      
  #     else :
  #       self.setEditedNote(tmp[0])
  #       self.setFinger(fingerNumber)
  #       fingerNumber = -1



  # ---------------------------------------------------------------------------
  # METHOD <setFinger>
  #
  # Update the finger associated to the note being edited by passing the 
  # finger number directly.
  #
  # This will also update the widget
  # ---------------------------------------------------------------------------
  # def setFinger(self, finger) :
    
  #   if (self.editedNote == None) :
  #     print("[WARNING] No note selected!")

  #   else :
  #     if finger in [1,2,3,4,5] :
  #       self.editedNote.finger = finger
  #       self._setSelector(finger, self.editedNote.hand)



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector._setSelector()                             [PRIVATE]
  # ---------------------------------------------------------------------------
  def _setSelector(self, finger, hand) :
    
    #self.sel = index
    #finger, hand = (0,0)

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
  # METHOD <_getFingerfromSel> (private)
  #
  # TODO
  # ---------------------------------------------------------------------------
  def _getFingerfromSel(self) :
        
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
        (isNoteHit, N) = self.top.widgets[WIDGET_ID_KEYBOARD].clickHitTest(pygame.mouse.get_pos())
        if isNoteHit :
          print(f"[DEBUG] FingerSelector._onMouseEvent(): that's a {N.name}")
          self.setEditedNote(N)
        
        # Click on the selector
        (isSelectorHit, selectorIndex) = self._selectorHitTest(pygame.mouse.get_pos())
        if isSelectorHit :
          print(f"[DEBUG] FingerSelector._onMouseEvent(): you hit the selector (index = {selectorIndex})")
          self.sel = selectorIndex
          # (hand, finger) = self._getFingerfromSel()
          
          # if (self.editedNote == None) :
          #   print("[WARNING] No note selected!")
            
          # else :
          #   self.editedNote.finger = finger
            
          #   if (hand != self.editedNote.hand) :
          #     return FINGERSEL_HAND_CHANGE
            
          #   return FINGERSEL_CHANGED
          
        

  # ---------------------------------------------------------------------------
  # METHOD FingerSelector._onKeyEvent()                             [INHERITED]
  # ---------------------------------------------------------------------------
  def _onKeyEvent(self, key, type, modifier = "") :
    """
    Function triggered by a keypress.
    """
    
    if (type == pygame.KEYDOWN) :
      
      # Simple keypresses (no modifiers)
      if (modifier == "") :
        
        # Tab: highlight the next note for edition
        if (key == pygame.K_TAB) :
          self._highlightNext()

        elif (key == pygame.K_KP_0) :
          print("[NOTE] FingerSelector._onKeyEvent(): delete finger, keep current hand")

        elif (key == pygame.K_KP_1) :
          print("[NOTE] FingerSelector._onKeyEvent(): set to finger 1")



      elif (modifier == "shift") :
        
        # Tab: highlight the previous note for edition
        if (key == pygame.K_TAB) :
          self._highlightPrevious()










# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'fingerSelector.py'.")



