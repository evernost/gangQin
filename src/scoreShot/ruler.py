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


HANDLE_LEFT_CANVAS_ID   = 3
HANDLE_RIGHT_CANVAS_ID  = 5
HANDLE_UP_CANVAS_ID     = 1
HANDLE_DOWN_CANVAS_ID   = 7

CAPTURE_CANVAS_ID = 4



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
    self.lineLeft  = self.canvasArray[CAPTURE_CANVAS_ID].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (2, 4))
    self.lineRight = self.canvasArray[CAPTURE_CANVAS_ID].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (2, 4))
    self.lineUp    = self.canvasArray[CAPTURE_CANVAS_ID].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (2, 4))
    self.lineDown  = self.canvasArray[CAPTURE_CANVAS_ID].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (4, 4))

    # Handles to drag and drop the rulers
    self.handleLeft   = self.canvasArray[HANDLE_LEFT_CANVAS_ID].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleRight  = self.canvasArray[HANDLE_RIGHT_CANVAS_ID].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleUp     = self.canvasArray[HANDLE_UP_CANVAS_ID].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")
    self.handleDown   = self.canvasArray[HANDLE_DOWN_CANVAS_ID].create_rectangle(0, 0, 0, 1, fill = "grey", outline = "grey")

    # Attach a management function to each handle 
    self.linkDragDropCallback(self.handleLeft , canvasId = HANDLE_LEFT_CANVAS_ID)
    self.linkDragDropCallback(self.handleRight, canvasId = HANDLE_RIGHT_CANVAS_ID)
    self.linkDragDropCallback(self.handleUp   , canvasId = HANDLE_UP_CANVAS_ID)
    self.linkDragDropCallback(self.handleDown , canvasId = HANDLE_DOWN_CANVAS_ID)
    self.dragData = {"x": 0, "y": 0, "id": None}

    # Visible property
    self._visible = True

    # Initialisation
    self._initDone = False



  # ---------------------------------------------------------------------------
  # METHOD Ruler.updateOnResize()
  # ---------------------------------------------------------------------------
  def updateOnResize(self) :
    """
    Updates the position of the rulers after a window resize.
    """
    
    captureHeight = self.canvasArray[CAPTURE_CANVAS_ID].winfo_height()
    captureWidth  = self.canvasArray[CAPTURE_CANVAS_ID].winfo_width()
  
    # If the transparent canvas has a weird size, it has probably not been initialised yet.
    if ((captureWidth <= 1) or (captureHeight <= 1)) :
      pass
    
    else :
      
      # At init: give a default position for the rulers/handles.
      if not(self._initDone) :
        self.setHandlesDefault()
        self._initDone = True
      
      # Afterwards: clamp the values to avoid losing the rulers/handles.
      else :
        (_,y,_,_) = self.canvasArray[CAPTURE_CANVAS_ID].coords(self.lineUp)
        self._setHandle("left", y)
        
        (_,y,_,_) = self.canvasArray[CAPTURE_CANVAS_ID].coords(self.lineDown)
        self._setHandle("right", y)
        
        (x,_,_,_) = self.canvasArray[CAPTURE_CANVAS_ID].coords(self.lineLeft)
        self._setHandle("up", x)
        
        (x,_,_,_) = self.canvasArray[CAPTURE_CANVAS_ID].coords(self.lineRight)
        self._setHandle("down", x)
        
        

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
      self.canvasArray[CAPTURE_CANVAS_ID].itemconfig(self.lineLeft  , state = "normal")
      self.canvasArray[CAPTURE_CANVAS_ID].itemconfig(self.lineRight , state = "normal")
      self.canvasArray[CAPTURE_CANVAS_ID].itemconfig(self.lineUp    , state = "normal")
      self.canvasArray[CAPTURE_CANVAS_ID].itemconfig(self.lineDown  , state = "normal")
      
      self.canvasArray[3].itemconfig(self.handleLeft, state = "normal")
      self.canvasArray[5].itemconfig(self.handleRight, state = "normal")
      self.canvasArray[1].itemconfig(self.handleUp, state = "normal")
      self.canvasArray[7].itemconfig(self.handleDown, state = "normal")

    else :
      self.canvasArray[CAPTURE_CANVAS_ID].itemconfig(self.lineLeft  , state = "hidden")
      self.canvasArray[CAPTURE_CANVAS_ID].itemconfig(self.lineRight , state = "hidden")
      self.canvasArray[CAPTURE_CANVAS_ID].itemconfig(self.lineUp    , state = "hidden")
      self.canvasArray[CAPTURE_CANVAS_ID].itemconfig(self.lineDown  , state = "hidden")
      
      self.canvasArray[3].itemconfig(self.handleLeft, state = "hidden")
      self.canvasArray[5].itemconfig(self.handleRight, state = "hidden")
      self.canvasArray[1].itemconfig(self.handleUp, state = "hidden")
      self.canvasArray[7].itemconfig(self.handleDown, state = "hidden")



  # ---------------------------------------------------------------------------
  # METHOD Ruler.linkDragDropCallback()
  # ---------------------------------------------------------------------------
  def linkDragDropCallback(self, handle, canvasId) :
    """
    Attaches a drag'n'drop callback function to an "handle" object in the GUI.
    """
    self.canvasArray[canvasId].tag_bind(handle, "<Button-1>", lambda event, id = canvasId : self.CLBK_onClick(event, id))
    self.canvasArray[canvasId].tag_bind(handle, "<B1-Motion>", lambda event, id = canvasId : self.CLBK_onDrag(event, id))




  # ---------------------------------------------------------------------------
  # METHOD Ruler._setHandle
  # ---------------------------------------------------------------------------
  def _setHandle(self, id, loc) :
    """
    todo
    """
    
    captureHeight = self.canvasArray[CAPTURE_CANVAS_ID].winfo_height()
    captureWidth  = self.canvasArray[CAPTURE_CANVAS_ID].winfo_width()

    if (id == "left") :
      y = min(loc, captureHeight-10)
      y = max(y, 10)
      self.canvasArray[HANDLE_LEFT_CANVAS_ID].coords(self.handleLeft, (80, y-5, 99, y+5))
      self.canvasArray[CAPTURE_CANVAS_ID].coords(self.lineUp, (0, y, captureWidth, y))
      
    elif (id == "right") :
      y = min(loc, captureHeight-10)
      y = max(y, 10)
      self.canvasArray[HANDLE_RIGHT_CANVAS_ID].coords(self.handleRight , (0, y-5, 19, y+5))
      self.canvasArray[CAPTURE_CANVAS_ID].coords(self.lineDown, (0, y, captureWidth, y))
      
    elif (id == "up") :
      x = min(loc, captureWidth-10)
      x = max(x, 10)
      self.canvasArray[HANDLE_UP_CANVAS_ID].coords(self.handleUp, (x-5, 80, x+5, 99))
      self.canvasArray[CAPTURE_CANVAS_ID].coords(self.lineLeft, (x, 0, x, captureHeight))
      
    elif (id == "down") :
      x = min(loc, captureWidth-10)
      x = max(x, 10)
      self.canvasArray[HANDLE_DOWN_CANVAS_ID].coords(self.handleDown, (x-5, 0, x+5, 19))
      self.canvasArray[CAPTURE_CANVAS_ID].coords(self.lineRight, (x, 0, x, captureHeight))
      
    else : 
      print(f"[DEBUG] Ruler._setHandle: unsupported id '{id}'")



  # ---------------------------------------------------------------------------
  # METHOD Ruler.setHandlesDefault
  # ---------------------------------------------------------------------------
  def setHandlesDefault(self) :
    """
    todo
    """    
    captureHeight = self.canvasArray[CAPTURE_CANVAS_ID].winfo_height()
    captureWidth  = self.canvasArray[CAPTURE_CANVAS_ID].winfo_width()
    
    self._setHandle("left"  , 50)
    self._setHandle("right" , captureHeight-50)
    self._setHandle("up"    , 50)
    self._setHandle("down"  , captureWidth-50)



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
    
    self._setHandle("left"  , left)
    self._setHandle("right" , right)
    self._setHandle("up"    , up)
    self._setHandle("down"  , down)



  # ---------------------------------------------------------------------------
  # METHOD Ruler.getHandles
  # ---------------------------------------------------------------------------
  def getHandles(self) :
    """
    One-liner to get the position of all the handles.
    This is primarily used to restore the app configuration after loading a
    database.
    """
    
    (_,yDown,_,yUp) = self.canvasArray[HANDLE_LEFT_CANVAS_ID].coords(self.handleLeft)
    left = int((yDown + yUp) // 2)

    (_,yDown,_,yUp) = self.canvasArray[HANDLE_RIGHT_CANVAS_ID].coords(self.handleRight)
    right = int((yDown + yUp) // 2)

    (xLeft,_,xRight,_) = self.canvasArray[HANDLE_UP_CANVAS_ID].coords(self.handleUp)
    up = int((xLeft + xRight) // 2)

    (xLeft,_,xRight,_) = self.canvasArray[HANDLE_DOWN_CANVAS_ID].coords(self.handleDown)
    down = int((xLeft + xRight) // 2)

    return (left, right, up, down)



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
    CALLBACK: function is called when an handle is dragged.
    """
    captureHeight = self.canvasArray[4].winfo_height()
    captureWidth = self.canvasArray[4].winfo_width()
    
    dx = event.x - self.dragData["x"]
    dy = event.y - self.dragData["y"]
    
    if (canvasId == HANDLE_UP_CANVAS_ID) :
      (lineLeft_x, _, _, _) = self.canvasArray[4].coords(self.lineLeft)
      if (((lineLeft_x + dx) >= 0) and ((lineLeft_x + dx) < captureWidth)) :
        self.canvasArray[1].move(self.handleUp, dx, 0)
        self.canvasArray[4].move(self.lineLeft, dx, 0)
    elif (canvasId == HANDLE_LEFT_CANVAS_ID) :
      (_, lineUp_y, _, _) = self.canvasArray[4].coords(self.lineUp)
      if (((lineUp_y + dy) >= 0) and ((lineUp_y + dy) < captureHeight)) :
        self.canvasArray[3].move(self.handleLeft, 0, dy)
        self.canvasArray[4].move(self.lineUp, 0, dy)
    elif (canvasId == HANDLE_RIGHT_CANVAS_ID) :
      (_, lineDown_y, _, _) = self.canvasArray[4].coords(self.lineDown)
      if (((lineDown_y + dy) >= 0) and ((lineDown_y + dy) < captureHeight)) :
        self.canvasArray[5].move(self.handleRight, 0, dy)
        self.canvasArray[4].move(self.lineDown, 0, dy)
    elif (canvasId == HANDLE_DOWN_CANVAS_ID) :
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



