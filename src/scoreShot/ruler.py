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



# =============================================================================
# Constants pool
# =============================================================================
HANDLE_LENGTH = 20
HANDLE_HEIGHT = 10



# =============================================================================
# Main code
# =============================================================================
class Ruler :
  
  """
  Defines the class for Ruler widgets in the capture window.
  """  
  def __init__(self, canvasArray) :
    self.canvasArray = canvasArray
    
    # Lines for the rulers
    self.lineLeft  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (2, 4))
    self.lineRight = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (2, 4))
    self.lineUp    = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (2, 4))
    self.lineDown  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (4, 4))

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



  # ---------------------------------------------------------------------------
  # METHOD Ruler.update()
  # ---------------------------------------------------------------------------
  def update(self) :
    """
    Updates the position of the rulers.
    This function must be called every time the capture window is resized or moved.
    """
    captureHeight = self.canvasArray[4].winfo_height()
    captureWidth = self.canvasArray[4].winfo_width()
  
    # If the transparent canvas has a weird size, it has probably not been initialised yet.
    if ((captureWidth <= 1) or (captureHeight <= 1)) :
      pass
    
    else :
      
      # At init: give a first plausible position for the rulers/handles.
      if not(self._initDone) :
        self.canvasArray[4].coords(self.lineUp,     (0, 50, captureWidth, 50))
        self.canvasArray[4].coords(self.lineDown,   (0, captureHeight-50, captureWidth, captureHeight-50))
        self.canvasArray[4].coords(self.lineLeft,   (50, 0, 50, captureHeight))
        self.canvasArray[4].coords(self.lineRight,  (captureWidth-50, 0, captureWidth-50, captureHeight))

        self.canvasArray[1].coords(self.handleUp,    (50-5, 80, 50+5, 99))
        self.canvasArray[7].coords(self.handleDown,  (captureWidth-50-5, 0, captureWidth-50+5, 19))
        self.canvasArray[3].coords(self.handleLeft,  (80, 45, 99, 55))
        self.canvasArray[5].coords(self.handleRight, (0, captureHeight-50-5, 19, captureHeight-50+5))
        self._initDone = True
      
      # Afterwards: clamp the values to avoid losing the rulers/handles.
      else :
        (_,y,_,_) = self.canvasArray[4].coords(self.lineUp)
        y = min(y, captureHeight-10)
        y = max(y, 10)
        self.canvasArray[4].coords(self.lineUp,     (0, y, captureWidth, y))
        self.canvasArray[3].coords(self.handleLeft,  (80, y-5, 99, y+5))
        
        (_,y,_,_) = self.canvasArray[4].coords(self.lineDown)
        y = min(y, captureHeight-10)
        y = max(y, 10)
        self.canvasArray[4].coords(self.lineDown,   (0, y, captureWidth, y))
        self.canvasArray[5].coords(self.handleRight, (0, y-5, 19, y+5))
        
        (x,_,_,_) = self.canvasArray[4].coords(self.lineLeft)
        x = min(x, captureWidth-10)
        x = max(x, 10)
        self.canvasArray[4].coords(self.lineLeft,   (x, 0, x, captureHeight))
        self.canvasArray[1].coords(self.handleUp,    (x-5, 80, x+5, 99))
        
        (x,_,_,_) = self.canvasArray[4].coords(self.lineRight)
        x = min(x, captureWidth-10)
        x = max(x, 10)
        self.canvasArray[4].coords(self.lineRight,  (x, 0, x, captureHeight))
        self.canvasArray[7].coords(self.handleDown,  (x-5, 0, x+5, 19))
        


  # ---------------------------------------------------------------------------
  # GETTER Ruler.visible
  # ---------------------------------------------------------------------------
  @property
  def visible(self) :
    return self._visible

  # ---------------------------------------------------------------------------
  # SETTER Ruler.visible
  # ---------------------------------------------------------------------------
  @visible.setter
  def visible(self, val) :
    """
    Setter for the 'visible' attribute.
    This function is called every time the 'visible' attribute is set.
    """
    self._visible = val
    
    if val :
      self.canvasArray[4].itemconfig(self.lineLeft, state = "normal")
      self.canvasArray[4].itemconfig(self.lineRight, state = "normal")
      self.canvasArray[4].itemconfig(self.lineUp, state = "normal")
      self.canvasArray[4].itemconfig(self.lineDown, state = "normal")
      
      self.canvasArray[3].itemconfig(self.handleLeft, state = "normal")
      self.canvasArray[5].itemconfig(self.handleRight, state = "normal")
      self.canvasArray[1].itemconfig(self.handleUp, state = "normal")
      self.canvasArray[7].itemconfig(self.handleDown, state = "normal")

    else :
      self.canvasArray[4].itemconfig(self.lineLeft, state = "hidden")
      self.canvasArray[4].itemconfig(self.lineRight, state = "hidden")
      self.canvasArray[4].itemconfig(self.lineUp, state = "hidden")
      self.canvasArray[4].itemconfig(self.lineDown, state = "hidden")
      
      self.canvasArray[3].itemconfig(self.handleLeft, state = "hidden")
      self.canvasArray[5].itemconfig(self.handleRight, state = "hidden")
      self.canvasArray[1].itemconfig(self.handleUp, state = "hidden")
      self.canvasArray[7].itemconfig(self.handleDown, state = "hidden")



  # ---------------------------------------------------------------------------
  # METHOD Ruler.bindHandle()
  # ---------------------------------------------------------------------------
  def bindHandle(self, handle, canvasId) :
    """
    TODO
    """
    self.canvasArray[canvasId].tag_bind(handle, "<Button-1>", lambda event, id = canvasId : self.CLBK_onClick(event, id))
    self.canvasArray[canvasId].tag_bind(handle, "<B1-Motion>", lambda event, id = canvasId : self.CLBK_onDrag(event, id))



  # ---------------------------------------------------------------------------
  # METHOD Ruler.setHandles
  # ---------------------------------------------------------------------------
  def setHandles(self, left, right, up, down) :
    """
    One-liner to set the position of all the handles.
    Position for each handle is given as argument.
    This is primarily used to restore the app configuration after loading a
    database.
    """
    
    print("[DEBUG] Ruler.setHandles: function is TODO")



  # ---------------------------------------------------------------------------
  # METHOD Ruler.getHandles
  # ---------------------------------------------------------------------------
  def getHandles(self) :
    """
    One-liner to get the position of all the handles.
    This is primarily used to restore the app configuration after loading a
    database.
    """
    
    print("[DEBUG] Ruler.getHandles: function is TODO")
    return (0,0,0,0)





  # ---------------------------------------------------------------------------
  # Callbacks methods
  # ---------------------------------------------------------------------------
  def CLBK_onClick(self, event, canvasId) :
    """
    Records the click position (used for the drag'n'drop)
    """
    self.dragData["x"] = event.x
    self.dragData["y"] = event.y
    self.dragData["id"] = canvasId



  def CLBK_onDrag(self, event, canvasId) :
    """
    TODO
    """
    captureHeight = self.canvasArray[4].winfo_height()
    captureWidth = self.canvasArray[4].winfo_width()
    
    dx = event.x - self.dragData["x"]
    dy = event.y - self.dragData["y"]
    
    if (canvasId == 1) :
      (lineLeft_x, _, _, _) = self.canvasArray[4].coords(self.lineLeft)
      if (((lineLeft_x + dx) >= 0) and ((lineLeft_x + dx) < captureWidth)) :
        self.canvasArray[1].move(self.handleUp, dx, 0)
        self.canvasArray[4].move(self.lineLeft, dx, 0)
    elif (canvasId == 3) :
      (_, lineUp_y, _, _) = self.canvasArray[4].coords(self.lineUp)
      if (((lineUp_y + dy) >= 0) and ((lineUp_y + dy) < captureHeight)) :
        self.canvasArray[3].move(self.handleLeft, 0, dy)
        self.canvasArray[4].move(self.lineUp, 0, dy)
    elif (canvasId == 5) :
      (_, lineDown_y, _, _) = self.canvasArray[4].coords(self.lineDown)
      if (((lineDown_y + dy) >= 0) and ((lineDown_y + dy) < captureHeight)) :
        self.canvasArray[5].move(self.handleRight, 0, dy)
        self.canvasArray[4].move(self.lineDown, 0, dy)
    elif (canvasId == 7) :
      (lineRight_x, _, _, _) = self.canvasArray[4].coords(self.lineRight)
      if (((lineRight_x + dx) >= 0) and ((lineRight_x + dx) < captureWidth)) :
        self.canvasArray[7].move(self.handleDown, dx, 0)
        self.canvasArray[4].move(self.lineRight, dx, 0)

    self.dragData["x"] = event.x
    self.dragData["y"] = event.y

  
    


# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'ruler.py'")



