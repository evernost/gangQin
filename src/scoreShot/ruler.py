# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : ruler
# File name     : ruler.py
# Purpose       : ruler widget for scoreShot capture window
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 29 September 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs 
# =============================================================================
import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab, ImageTk, Image



# =============================================================================
# Constants pool
# =============================================================================
HANDLE_LENGTH = 20
HANDLE_HEIGHT = 10



# =============================================================================
# Main code
# =============================================================================
class Ruler :
  def __init__(self, canvasArray) :
    self.canvasArray = canvasArray
    
    # Lines for the rulers
    self.rulerLeft  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (2, 4))
    self.rulerRight = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (2, 4))
    self.rulerUp    = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (2, 4))
    self.rulerDown  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (4, 4))

    # Handles to drag and drop the rulers
    self.handleLeft   = self.canvasArray[3].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleRight  = self.canvasArray[5].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleUp     = self.canvasArray[1].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleDown   = self.canvasArray[7].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")

    # Attach a management function to each handle 
    self.bindHandle(self.handleLeft, canvasId = 3)
    self.bindHandle(self.handleRight, canvasId = 5)
    self.bindHandle(self.handleUp, canvasId = 1)
    self.bindHandle(self.handleDown, canvasId = 7)
    self.dragData = {"x": 0, "y": 0, "id": None}

    # Visible property
    self._visible = True

    # Initialisation
    self._initDone = False




  def update(self) :
    """
    This function is called every time the capture window is resized or moved.
    """
    captureHeight = self.canvasArray[4].winfo_height()
    captureWidth = self.canvasArray[4].winfo_width()
  
    # If the transparent canvas has a weird size, it has probably not been initialised yet.
    if ((captureWidth <= 1) or (captureHeight <= 1)) :
      pass
    
    else :
      
      # At init: give a first plausible position for the rulers/handles.
      if not(self._initDone) :
        self.canvasArray[4].coords(self.rulerUp,     (0, 50, captureWidth, 50))
        self.canvasArray[4].coords(self.rulerDown,   (0, captureHeight-50, captureWidth, captureHeight-50))
        self.canvasArray[4].coords(self.rulerLeft,   (50, 0, 50, captureHeight))
        self.canvasArray[4].coords(self.rulerRight,  (captureWidth-50, 0, captureWidth-50, captureHeight))

        self.canvasArray[1].coords(self.handleUp,    (50-5, 80, 50+5, 99))
        self.canvasArray[7].coords(self.handleDown,  (captureWidth-50-5, 0, captureWidth-50+5, 19))
        self.canvasArray[3].coords(self.handleLeft,  (80, 45, 99, 55))
        self.canvasArray[5].coords(self.handleRight, (0, captureHeight-50-5, 19, captureHeight-50+5))
        self._initDone = True
      
      # Afterwards: clamp the values to avoid losing the rulers/handles.
      else :
        (_,y,_,_) = self.canvasArray[4].coords(self.rulerUp)
        y = min(y, captureHeight-10)
        y = max(y, 10)
        self.canvasArray[4].coords(self.rulerUp,     (0, y, captureWidth, y))
        self.canvasArray[3].coords(self.handleLeft,  (80, y-5, 99, y+5))
        
        (_,y,_,_) = self.canvasArray[4].coords(self.rulerDown)
        y = min(y, captureHeight-10)
        y = max(y, 10)
        self.canvasArray[4].coords(self.rulerDown,   (0, y, captureWidth, y))
        self.canvasArray[5].coords(self.handleRight, (0, y-5, 19, y+5))
        
        (x,_,_,_) = self.canvasArray[4].coords(self.rulerLeft)
        x = min(x, captureWidth-10)
        x = max(x, 10)
        self.canvasArray[4].coords(self.rulerLeft,   (x, 0, x, captureHeight))
        self.canvasArray[1].coords(self.handleUp,    (x-5, 80, x+5, 99))
        
        (x,_,_,_) = self.canvasArray[4].coords(self.rulerRight)
        x = min(x, captureWidth-10)
        x = max(x, 10)
        self.canvasArray[4].coords(self.rulerRight,  (x, 0, x, captureHeight))
        self.canvasArray[7].coords(self.handleDown,  (x-5, 0, x+5, 19))
        
        





  def bindHandle(self, handle, canvasId) :
    self.canvasArray[canvasId].tag_bind(handle, "<Button-1>", lambda event, id = canvasId : self.CLBK_onClick(event, id))
    self.canvasArray[canvasId].tag_bind(handle, "<B1-Motion>", lambda event, id = canvasId : self.CLBK_onDrag(event, id))



  # ---------------------------------------------------------------------------
  # Callbacks methods
  # ---------------------------------------------------------------------------
  def CLBK_onClick(self, event, canvasId) :
    self.dragData["x"] = event.x
    self.dragData["y"] = event.y
    self.dragData["id"] = canvasId



  def CLBK_onDrag(self, event, canvasId) :
    dx = event.x - self.dragData["x"]
    dy = event.y - self.dragData["y"]
    
    if (canvasId == 1) :
      self.canvasArray[1].move(self.handleUp, dx, 0)
      self.canvasArray[4].move(self.rulerLeft, dx, 0)
    elif (canvasId == 3) :
      self.canvasArray[3].move(self.handleLeft, 0, dy)
      self.canvasArray[4].move(self.rulerUp, 0, dy)
    elif (canvasId == 5) :
      self.canvasArray[5].move(self.handleRight, 0, dy)
      self.canvasArray[4].move(self.rulerDown, 0, dy)
    elif (canvasId == 7) :
      self.canvasArray[7].move(self.handleDown, dx, 0)
      self.canvasArray[4].move(self.rulerRight, dx, 0)

    self.dragData["x"] = event.x
    self.dragData["y"] = event.y

  @property
  def visible(self) :
    return self._visible

  @visible.setter
  def visible(self, val) :
    """
    Setter for the 'visible' attribute.
    This function is called every time the 'visible' attribute is set.
    """
    if val :
      self.canvasArray[4].itemconfig(self.rulerLeft, state = "normal")
      self.canvasArray[4].itemconfig(self.rulerRight, state = "normal")
      self.canvasArray[4].itemconfig(self.rulerUp, state = "normal")
      self.canvasArray[4].itemconfig(self.rulerDown, state = "normal")
      
      self.canvasArray[3].itemconfig(self.handleLeft, state = "normal")
      self.canvasArray[5].itemconfig(self.handleRight, state = "normal")
      self.canvasArray[1].itemconfig(self.handleUp, state = "normal")
      self.canvasArray[7].itemconfig(self.handleDown, state = "normal")





    else :
      self.canvasArray[4].itemconfig(self.rulerLeft, state = "hidden")
      self.canvasArray[4].itemconfig(self.rulerRight, state = "hidden")
      self.canvasArray[4].itemconfig(self.rulerUp, state = "hidden")
      self.canvasArray[4].itemconfig(self.rulerDown, state = "hidden")
      
      self.canvasArray[3].itemconfig(self.handleLeft, state = "hidden")
      self.canvasArray[5].itemconfig(self.handleRight, state = "hidden")
      self.canvasArray[1].itemconfig(self.handleUp, state = "hidden")
      self.canvasArray[7].itemconfig(self.handleDown, state = "hidden")


      # Change the "highlightbackground" property: it will show in the screeshot otherwise.
    
    self._visible = val



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'ruler.py'")



