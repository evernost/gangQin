# -*- coding: utf-8 -*-
# =============================================================================
# Module name     : gui
# File name       : gui.py
# Purpose         : lib for the widgets on screen
# Author          : Quentin Biache
# Creation date   : September 22nd, 2023
# =============================================================================

# =============================================================================
# Imports 
# =============================================================================
import fontUtils as fu
import pygame
import keyboardUtils as ku

# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This lib is not intended to be called as a main.")



# Pool of constants
FINGERSEL_UNCHANGED = 0
FINGERSEL_CHANGED = 1


# =============================================================================
# Main code 
# =============================================================================

class FingerSelector :

  def __init__(self, loc) :
    (self.locX, self.locY) = loc
    self.textColor = (41, 67, 132)
    self.textColorL = (145, 7, 0)
    self.textColorR = (0, 145, 7)
    self.lineColor = (41, 67, 132)
    
    self.textColorSelL = (244, 13, 0)
    self.textColorSelR = (0, 244, 13)

    self.currentSel = 0

    self.visible = False



  def show(self, screen) :
    if (self.visible) :
      labels = ["5 ", "4 ", "3 ", "2 ", "1 ", "- ", "- ", "1 ", "2 ", "3 ", "4 ", "5 "]
      
      # Note: 96 = 8*10 + 8*2, i.e. 8 x char size + 8 x space in-between
      fu.render(screen, f"FINGER: ", (self.locX, self.locY), 2, self.textColor)      
      
      for i in range(12) :
        if (i <= 5) :          
          if (self.currentSel == i) :
            fu.render(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorSelL)
          else :
            fu.render(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorL)

        else :
          if (self.currentSel == i) :
            fu.render(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorSelR)
          else :
            fu.render(screen, labels[i], (self.locX + 96 + (i*23), self.locY), 2, self.textColorR)

      x0 = self.locX + 96 - 7
      yTop = self.locY + 3; yBottom = self.locY + 12
      for i in range(13) :
        if (i == 6) :
          pygame.draw.line(screen, self.lineColor, (x0 + (i*23), yTop-8), (x0 + (i*23), yBottom+6), 1)
        else :
          pygame.draw.line(screen, self.lineColor, (x0 + (i*23), yTop), (x0 + (i*23), yBottom), 1)
    


  def setNote(self, activeNote) :
    self.activeNote = activeNote



  def getNote(self) :
    return self.activeNote



  def updateWithClick(self, clickX, clickY) :
    x0 = self.locX + 96 - 7
    yTop = self.locY + 3; yBottom = self.locY + 12
    for i in range(12) :
      xMin = x0 + (i*23) + 1
      xMax = x0 + ((i+1)*23) - 1
      yMin = yTop - 6
      yMax = yBottom + 4

      if ((clickX >= xMin) and (clickX <= xMax) and (clickY >= yMin) and (clickY <= yMax)) :
        self.currentSel = i
        
        if (i == 5) :
          self.activeNote.finger = 0
          # self.activeNote.hand = ku.LEFT_HAND  => not supported yet
        
        if (i == 6) :
          self.activeNote.finger = 0
          # self.activeNote.hand = ku.RIGHT_HAND  => not supported yet
        
        if (i <= 4) :
          self.activeNote.finger = 5-i

        if (i >= 7) :
          self.activeNote.finger = i-6
        
        return FINGERSEL_CHANGED
      
    return FINGERSEL_UNCHANGED
  
