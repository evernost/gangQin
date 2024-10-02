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



# =============================================================================
# Main code
# =============================================================================
class Ruler :
  def __init__(self, canvasArray) :
    self.canvasArray = canvasArray
    
    # Lines for the rulers
    # Coordinates can't be specified at that point: they depend on the window properties
    # that is not initialised yet
    self.rulerLeft  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerRight = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerUp    = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))
    self.rulerDown  = self.canvasArray[4].create_line(0, 0, 0, 1, fill = "black", width = 1, dash = (1, 10))

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




  def update(self) :
    apHeight = self.canvasArray[4].winfo_height()
    apWidth = self.canvasArray[4].winfo_width()
    self.canvasArray[4].coords(self.rulerUp,     (0, 50, apWidth, 50))
    self.canvasArray[4].coords(self.rulerDown,   (0, apHeight-50, apWidth, apHeight-50))
    self.canvasArray[4].coords(self.rulerLeft,   (50, 0, 50, apHeight))
    self.canvasArray[4].coords(self.rulerRight,  (apWidth-50, 0, apWidth-50, apHeight))

    self.canvasArray[1].coords(self.handleUp,    (50-5, 80, 50+5, 99))
    self.canvasArray[7].coords(self.handleDown,  (apWidth-50-5, 0, apWidth-50+5, 19))
    self.canvasArray[3].coords(self.handleLeft,  (80, 45, 99, 55))
    self.canvasArray[5].coords(self.handleRight, (0, apHeight-50-5, 19, apHeight-50+5))
    
  def bindHandle(self, handle, canvasId) :
    self.canvasArray[canvasId].tag_bind(handle, "<Button-1>", lambda event, id = canvasId : self.on_click(event, id))
    self.canvasArray[canvasId].tag_bind(handle, "<B1-Motion>", lambda event, id = canvasId : self.on_drag(event, id))

  def on_click(self, event, canvasId):
    self.dragData["x"] = event.x
    self.dragData["y"] = event.y
    self.dragData["id"] = canvasId

  def on_drag(self, event, canvasId):
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
    
    self._visible = val



