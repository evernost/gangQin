# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : 
# File name     : staffScope.py
# Purpose       : viewer widget on the actual music score
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 20 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================


# Specs:
# - draws the staffScope widget
# - loads and resizes the score snapshot efficiently (loads and reshapes once)
# - draws the rectangle overlay on the score snapshot
# - handles the user interactions


# =============================================================================
# External libs 
# =============================================================================


import src.scoreShot.database as database

import pygame
import os



# =============================================================================
# Constants pool
# =============================================================================



# =============================================================================
# Main code
# =============================================================================
class StaffScope :

  """
  The StaffScope widget is ...
  """
  def __init__(self, songFile) :
    
    self.db = None
    
    self.screen = None
    
    self.img = None
    self.imgFile = ""
    self.imgSpan = [-1,-1]


    self._indexLoaded = -1   # Index of the image loaded



    # User interaction queues
    self.msgQueueIn = []
    self.msgQueueOut = []


    # Internal initialisation
    self._loadDatabase(songFile)
    self.loadByIndex(0)



  # ---------------------------------------------------------------------------
  # METHOD Database._loadDatabase()
  # ---------------------------------------------------------------------------
  def _loadDatabase(self, songFile) :
    """
    Generates the various names of files and directories associated with the 
    database.
    """
    
    self.db = database.Database(songFile)
    
    
    # (rootDir, rootNameExt) = os.path.split(prFile)
    # (rootName, _) = os.path.splitext(rootNameExt)
    # self.songName     = rootName
    # self.songFile     = rootNameExt
    # self.jsonName     = rootName + ".json"          # Example: "my_song.json"
    # self.jsonFile     = f"./snaps/{self.jsonName}"  # Example: "./snaps/my_song.json"
    # self.depotFolder  = f"./snaps/db__{rootName}"   # Example: "./snaps/db__my_song"



  # ---------------------------------------------------------------------------
  # METHOD Database.setScreen()
  # ---------------------------------------------------------------------------
  def setScreen(self, screenObj) :
    """
    Creates an internal copy of the Pygame screen object of the main application
    window.
    """
    self.screen = screenObj







  # ---------------------------------------------------------------------------
  # GETTER StaffScope.index
  # ---------------------------------------------------------------------------
  @property
  def index(self) :
    return self._indexLoaded

  # ---------------------------------------------------------------------------
  # SETTER StaffScope.index
  # ---------------------------------------------------------------------------
  @index.setter
  def index(self, val) :
    """
    Setter for the 'index' attribute.
    TODO
    """
    
    if ((val > 0) and (val < self.db.nSnapshots)) :
      self._indexLoaded = val
      self.loadByIndex(self._indexLoaded)

    
    


  # ---------------------------------------------------------------------------
  # METHOD Database.nextStaff()
  # ---------------------------------------------------------------------------
  def nextStaff(self) :
    """
    Loads and shows the next staff.
    Clamps to the last staff when reaching the end.
    """
    
    self.index += 1


    
# ---------------------------------------------------------------------------
  # METHOD Database.previousStaff()
  # ---------------------------------------------------------------------------
  def previousStaff(self) :
    """
    Loads and shows the previous staff.
    Clamps to the first staff when reaching the beginning.
    """
    
    self.index -= 1




  # ---------------------------------------------------------------------------
  # METHOD Database.loadByIndex()
  # ---------------------------------------------------------------------------
  def loadByIndex(self, index) :
    """
    Loads and shows the staff at index "index" in the database.
    
    """
    
    print("[DEBUG] StaffScope.nextStaff() is TODO.")

    self.imgName = self.db.getSnapshotNameByIndex(index)
    
    if (self.imgName != "") :
      img = pygame.image.load(imgName)
      (imgWidth, imgHeight) = img.get_size()

      sWidth = TARGET_WIDTH/imgWidth
      sHeight = TARGET_HEIGHT/imgHeight

      s = min(sWidth, sHeight)
      
      imgScaled = pygame.transform.smoothscale(img, (int(imgWidth*s), int(imgHeight*s)))

      # Create a transparent surface (same size as the main window)
      #transparent_surface = pygame.Surface(window_size, pygame.SRCALPHA)

      # Define the rectangle color (RGBA format: R, G, B, A) with transparency
      #transparent_color = (255, 0, 0, 128)  # Red with 50% transparency

      # Define the rectangle's position and size (x, y, width, height)
      #rect_position = (150, 200, 200, 100)

      
      # Display the image at the specified position
      xCenter = (screenWidth-(int(imgWidth*s)))//2
      screen.blit(imgScaled, (xCenter, 50))

      # Clear the transparent surface (important if you redraw it each frame)
      #transparent_surface.fill((0, 0, 0, 0))  # Completely transparent




  # ---------------------------------------------------------------------------
  # METHOD Database.loadByCursor()
  # ---------------------------------------------------------------------------
  def loadByCursor(self, cursor) :
    """
    Loads and shows the staff that covers the cursor value passed as argument.
    The image is cached as long as the cursor requested stays in the capture's span.
    Therefore, calls to the function have virtually no cost.
    """
    
    if ((index >= self.imgSpan[0]) and (index <= self.imgSpan[1])) :
      pass
    
    else :
      index = self.db.getIndexByCursor(cursor)
      self.loadByIndex(index)

    



