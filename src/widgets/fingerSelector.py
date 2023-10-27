# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : fingerSelector
# File name     : fingerSelector.py
# Purpose       : provides a widget to edit the properties of a given note
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

import pygame
import fontUtils as fu



# =============================================================================
# Constants pool
# =============================================================================
FINGERSEL_UNCHANGED = 0
FINGERSEL_CHANGED = 1



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")



# =============================================================================
# Main code
# =============================================================================

class FingerSelector :

  def __init__(self, loc) :
    (self.locX, self.locY) = loc
    self.textColor = UI_TEXT_COLOR
    self.textColorL = (145, 7, 0)
    self.textColorR = (0, 145, 7)
    self.lineColor = UI_TEXT_COLOR
    
    self.textColorSelL = (244, 13, 0)
    self.textColorSelR = (0, 244, 13)

    # - 0 = left hand, finger 5
    # - 1 = left hand, finger 4
    # ...
    # - 4 = left hand, finger 1
    # - 5 = left hand, finger undefined
    # - 6 = right hand, finger undefined
    # - 7 = right hand, finger 1
    # ...
    # - 11 = right hand, finger 5
    self.currentSel = 5

    self.visible = False

    self.editedNote = None

  # ---------------------------------------------------------------------------
  # METHOD <show>
  #
  # Show the finger selection widget.
  # ---------------------------------------------------------------------------
  def show(self, screen) :
    if (self.visible) :
      labels = ["5 ", "4 ", "3 ", "2 ", "1 ", "- ", "- ", "1 ", "2 ", "3 ", "4 ", "5 "]
      
      # Note: 96 = 8*10 + 8*2, i.e. 8 x char size + 8 x space in-between
      fu.renderText(screen, f"FINGER: ", (self.locX, self.locY), 2, self.textColor)      
      
      for i in range(12) :
        if (i <= 5) :          
          if (self.currentSel == i) :
            fu.renderText(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorSelL)
          else :
            fu.renderText(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorL)

        else :
          if (self.currentSel == i) :
            fu.renderText(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorSelR)
          else :
            fu.renderText(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorR)

      x0 = self.locX + 96 - 7
      yTop = self.locY + 3; yBottom = self.locY + 12
      for i in range(13) :
        if (i == 6) :
          pygame.draw.line(screen, self.lineColor, (x0 + (i*23), yTop-8), (x0 + (i*23), yBottom+6), 1)
        else :
          pygame.draw.line(screen, self.lineColor, (x0 + (i*23), yTop), (x0 + (i*23), yBottom), 1)
    

  # ---------------------------------------------------------------------------
  # METHOD <setEditedNote>
  #
  # Define the note whose properties are shown in the finger selector.
  # ---------------------------------------------------------------------------
  def setEditedNote(self, noteObj) :
    #print(f"[DEBUG] Set note: pitch={noteObj.pitch}, finger={noteObj.finger}, index={noteObj.noteIndex}")
    self._setCurrentSel(noteObj.finger, noteObj.hand)
    if (self.editedNote != None) :
      self.editedNote.highlight = False
    
    self.editedNote = noteObj
    noteObj.highlight = True



  # ---------------------------------------------------------------------------
  # METHOD <getEditedNote>
  #
  # TODO
  # ---------------------------------------------------------------------------
  def getEditedNote(self) :
    return self.editedNote



  # ---------------------------------------------------------------------------
  # METHOD <setFingerWithClick>
  #
  # Update the finger associated to the note being edited using a click on the 
  # widget.
  #
  # The function returns if the click actually hit something relevant on the 
  # widget and it got updated, or the click occured outside the scope and 
  # nothing changed.
  # ---------------------------------------------------------------------------
  def setFingerWithClick(self, clickX, clickY) :
    
    if (self.editedNote == None) :
      print("[WARNING] Attempted to edit the properties of a void note (internal error)")

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
        
        self.editedNote.finger = finger
        # self.editedNote.hand = ...  => switching a note from one hand to the other is not supported yet
        
        return FINGERSEL_CHANGED
      
    return FINGERSEL_UNCHANGED
  

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
      print("[WARNING] Attempted to edit the properties of a void note (internal error)")

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
        self.currentSel = 5-finger
    
    if (hand == RIGHT_HAND) :
      self.currentSel = 6
      if (finger in [1,2,3,4,5]) :
        self.currentSel = finger+6
    
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
      return (RIGHT_HAND, self.currentSel-6)
    
    return (UNDEFINED_FINGER, UNDEFINED_HAND)