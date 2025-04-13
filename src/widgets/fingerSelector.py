# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : fingerSelector
# File name     : fingerSelector.py
# Purpose       : widget to edit the 'finger' property of a note.
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from src.commons import *

import src.widgets.widget as widget
import text

# Standard libs
import pygame




# =============================================================================
# Constants pool
# =============================================================================
FINGERSEL_NONE_SELECTED = -1
FINGERSEL_UNCHANGED = 0
FINGERSEL_CHANGED = 1
FINGERSEL_HAND_CHANGE = 3



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class FingerSelector(widget.Widget) :

  def __init__(self, top, loc) :
    
    # Call the Widget init method
    super().__init__(top, loc)

    # Define the events the widgets must react to
    self.uiSensivityList = [pygame.K_TAB]

    # UI interaction queues
    self.msgQueueIn = []
    self.msgQueueOut = []

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
    self.currentSel = FINGERSEL_NONE_SELECTED

    self.visible = False

    self.editedNote = None
    self.editedCursor = -1

    # *** Graphical properties ***
    (self.locX, self.locY) = loc
    self.textColor = GUI_TEXT_COLOR
    self.textColorL = (145, 7, 0)
    self.textColorR = (0, 145, 7)
    self.lineColor = GUI_TEXT_COLOR
    
    self.textColorSelL = (244, 13, 0)
    self.textColorSelR = (0, 244, 13)



  # ---------------------------------------------------------------------------
  # METHOD Metronome.keyPress(pygameKeys)
  # ---------------------------------------------------------------------------
  def keyPress(self, pygameKeys) :
    """
    TODO
    """

    if pygameKeys[pygame.K_TAB] :      
      print("[DEBUG] Fingersatz edition using (shift) tab is not done yet!")
      self.msgQueueIn.append("TAB")



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.show()
  # ---------------------------------------------------------------------------
  def show(self, screen) :
    """
    Render the finger selection widget on screen.
    Screen object (in a Pygame sense) must be provided as argument.
    """
    if (self.visible) :
      labels = ["5 ", "4 ", "3 ", "2 ", "1 ", "- ", "- ", "1 ", "2 ", "3 ", "4 ", "5 "]
      
      # Note: 96 = 8*10 + 8*2, i.e. 8 x char size + 8 x space in-between
      text.render(screen, f"FINGER: ", (self.locX, self.locY), 2, self.textColor)      
      
      for i in range(12) :
        if (i <= 5) :          
          if (self.currentSel == i) :
            text.render(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorSelL)
          else :
            text.render(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorL)

        else :
          if (self.currentSel == i) :
            text.render(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorSelR)
          else :
            text.render(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorR)

      x0 = self.locX + 96 - 7
      yTop = self.locY + 3; yBottom = self.locY + 12
      for i in range(13) :
        if (i == 6) :
          pygame.draw.line(screen, self.lineColor, (x0 + (i*23), yTop-8), (x0 + (i*23), yBottom+6), 1)
        else :
          pygame.draw.line(screen, self.lineColor, (x0 + (i*23), yTop), (x0 + (i*23), yBottom), 1)
    


  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.setEditedNote()
  # ---------------------------------------------------------------------------
  def setEditedNote(self, noteObj, cursor = -1) :
    """
    Defines the note whose properties are shown in the finger selector.
    A cursor value can be stored along with the note so that it is easier to 
    show/hide the widget in a specific context.
    """
    self._setCurrentSel(noteObj.finger, noteObj.hand)
    if (self.editedNote != None) :
      self.editedNote.highlight = False
    
    self.editedNote = noteObj
    self.editedCursor = cursor
    noteObj.highlight = True



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.getEditedNote()
  # ---------------------------------------------------------------------------
  def getEditedNote(self) :
    """
    todo
    """
    
    return self.editedNote



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.resetEditedNote()
  # ---------------------------------------------------------------------------
  def resetEditedNote(self) :
    """
    todo
    """
    
    self.editedNote.highlight = False
    self.editedNote = None
    self.editedCursor = -1
    self.currentSel = -1



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.setFingerWithClick(clickCoordinates)
  # ---------------------------------------------------------------------------
  def setFingerWithClick(self, clickCoord) :
    """
    Update the finger associated to the note being edited using a click on the 
    widget.

    The function returns if the click actually hit something relevant on the 
    widget and it got updated, or the click occured outside the scope and 
    nothing changed.
    """

    (clickX, clickY) = clickCoord
    x0 = self.locX + 96 - 7
    yTop = self.locY + 3; yBottom = self.locY + 12
    
    # Loop on the members of the widgets, test if any was hit with the click
    for i in range(12) :
      xMin = x0 + (i*23) + 1
      xMax = x0 + ((i+1)*23) - 1
      yMin = yTop - 6
      yMax = yBottom + 4

      # If the click is in this current hit box
      if ((clickX >= xMin) and (clickX <= xMax) and (clickY >= yMin) and (clickY <= yMax)) :
        
        self.currentSel = i
        (hand, finger) = self._getFingerfromSel()
        
        if (self.editedNote == None) :
          print("[WARNING] No note selected!")
          
        else :
          self.editedNote.finger = finger
          
          if (hand != self.editedNote.hand) :
            return FINGERSEL_HAND_CHANGE
          
          return FINGERSEL_CHANGED
      
    return FINGERSEL_UNCHANGED
  


  # ---------------------------------------------------------------------------
  # METHOD <FingerSelector.setFingerAutoHighlight>
  # ---------------------------------------------------------------------------
  def setFingerAutoHighlight(self, fingerNumber, teacherNotes, activeHands) :
    """
    Takes a finger index, the context. Assigns the finger index to the relevant
    note.
    
    
    """

    # Sustained notes are not eligible to the note auto highlight
    activeNotes = [x for x in teacherNotes if not(x.sustained)]

    # Find a note that does not have a finger assigned yet
    if (len(activeNotes) > 1) :
      singleHandContent = True
      for x in activeNotes[1:] :
        if (x.hand != activeNotes[0].hand) :
          singleHandContent = False
          break
    
    else :
      singleHandContent = True
    
    if ((activeHands != "LR") or singleHandContent) :
      
      # Sort by ascending pitch
      activeNotes.sort(key = lambda x: x.pitch)
      
      # Keep notes not yet assigned
      tmp = [x for x in activeNotes if (x.finger == UNDEFINED_FINGER)]
      
      # Are all notes already assigned to a finger? -> start over
      if (len(tmp) == 0) :
        print("[DEBUG] Not handled yet.")
      
      else :
        self.setEditedNote(tmp[0])
        self.setFinger(fingerNumber)
        fingerNumber = -1



  # ---------------------------------------------------------------------------
  # METHOD <FingerSelector.highlightWithTab>
  # ---------------------------------------------------------------------------
  def highlightWithTab(self, teacherNotes) :
    """
    Highlights the editable notes one after the other every time the 'tab' or
    'shift' + 'tab' combination is pressed.
    """

    # Sustained notes are not editable through this mode 
    # (is it supposed to be a shortcut)
    activeNotes = [x for x in teacherNotes if not(x.sustained)]

    print("todo!")



  # ---------------------------------------------------------------------------
  # METHOD <setFinger>
  #
  # Update the finger associated to the note being edited by passing the 
  # finger number directly.
  #
  # This will also update the widget
  # ---------------------------------------------------------------------------
  def setFinger(self, finger) :
    
    if (self.editedNote == None) :
      print("[WARNING] No note selected!")

    else :
      if finger in [1,2,3,4,5] :
        self.editedNote.finger = finger
        self._setCurrentSel(finger, self.editedNote.hand)



  # ---------------------------------------------------------------------------
  # METHOD <_setCurrentSel> (private)
  #
  # TODO
  # ---------------------------------------------------------------------------
  def _setCurrentSel(self, finger, hand) :
    
    if (hand == LEFT_HAND) :
      self.currentSel = 5
      if (finger in [1,2,3,4,5]) :
        self.currentSel = 5 - finger
    
    if (hand == RIGHT_HAND) :
      self.currentSel = 6
      if (finger in [1,2,3,4,5]) :
        self.currentSel = finger + 6
    


  # ---------------------------------------------------------------------------
  # METHOD <_getFingerfromSel> (private)
  #
  # TODO
  # ---------------------------------------------------------------------------
  def _getFingerfromSel(self) :
        
    if (self.currentSel <= 4) :
      return (LEFT_HAND, 5-self.currentSel)

    if (self.currentSel == 5) :
      return (LEFT_HAND, UNDEFINED_FINGER)
      # self.editedNote.hand = ku.LEFT_HAND  => not supported yet
    
    if (self.currentSel == 6) :
      return (RIGHT_HAND, UNDEFINED_FINGER)
      # self.editedNote.hand = ku.RIGHT_HAND  => not supported yet
    
    if (self.currentSel >= 7) :
      return (RIGHT_HAND, self.currentSel - 6)
    
    return (UNDEFINED_FINGER, UNDEFINED_HAND)
  



  # ---------------------------------------------------------------------------
  # METHOD: FingerSelector.uiEvent()
  # ---------------------------------------------------------------------------
  def uiEvent(self, pygameEvent) :
    """
    This function is called every time a pygame event listed in 'uiSensitivityList'
    happens.
    """
    
    if pygameEvent in self.uiSensivityList :
      pass





  # ---------------------------------------------------------------------------
  # METHOD FingerSelector.keyRelease(pygameKeys)
  # ---------------------------------------------------------------------------
  def keyRelease(self, key) :
    """
    Updates the finger selector widget status (ON, OFF, increase tempo, etc.) 
    based on the keys that have been released.
    """

    #TODO!

    if (key == pygame.K_m) :
      pass




# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'fingerSelector.py'")

