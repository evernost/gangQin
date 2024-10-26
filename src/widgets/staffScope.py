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



# =============================================================================
# Constants pool
# =============================================================================
TARGET_WIDTH = 1300
TARGET_HEIGHT = 230



# =============================================================================
# Main code
# =============================================================================
class StaffScope :

  """
  The StaffScope widget is ...
  """
  def __init__(self) :
    
    self.db = None
    
    self.screen = None
    self.screenWidth = -1       # GUI width
    self.screenHeight = -1      # GUI height
    
    self.img = None
    self.imgFile = ""
    self.imgSpan = [-1,-1]
    self.imgHeight = -1
    self.imgWidth = -1
    self.imgCoordX = -1
    self.imgCoordY = -1
    self.imgBox = (-1, -1, -1, -1)
    self.imgScaling = 0

    self._indexLoaded = -1      # Index of the snapshot loaded (-1 when nothing is loaded)

    self.playGlowLeft = []
    self.playGlowRight = []


    # User interaction queues
    self.msgQueueIn = []
    self.msgQueueOut = []



  # ---------------------------------------------------------------------------
  # METHOD Database.setScreen()
  # ---------------------------------------------------------------------------
  def setScreen(self, screenObj, width, height) :
    """
    Creates an internal copy of the Pygame screen parameters.
    Required to draw and interact with the widget.
    """

    self.screen = screenObj
    self.screenWidth = width
    self.screenHeight = height



  # ---------------------------------------------------------------------------
  # METHOD Database.load(<.pr filename string>)
  # ---------------------------------------------------------------------------
  def load(self, songFile) :
    """
    Loads the snapshot database associated with the filename given as argument.
    """

    self.db = database.Database(songFile)
    self.loadByIndex(0)



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.nextStaff()
  # ---------------------------------------------------------------------------
  def nextStaff(self) :
    """
    Loads and shows the next staff.
    Clamps to the last staff when reaching the end of the score.
    """
    
    if ((self._indexLoaded + 1) <= (self.db.nSnapshots-1)) :
      self.loadByIndex(self._indexLoaded+1)


    
# ---------------------------------------------------------------------------
  # METHOD StaffScope.previousStaff()
  # ---------------------------------------------------------------------------
  def previousStaff(self) :
    """
    Loads and shows the previous staff.
    Clamps to the first staff when reaching the beginning of the score.
    """
    
    if ((self._indexLoaded - 1) >= 0) :
      self.loadByIndex(self._indexLoaded-1)



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.loadByIndex()
  # ---------------------------------------------------------------------------
  def loadByIndex(self, index) :
    """
    Loads the content located at position "index" in the snapshot database.
    Once loaded, the "_indexLoaded" is updated with the requested index.
    """
    
    # Load only if not cached yet
    if (self._indexLoaded != index) :

      self.imgFile = self.db.getSnapshotFileByIndex(index)
      if (self.imgFile != "") :
        
        # Load the file
        self.img = pygame.image.load(self.imgFile)
        (self.imgWidth, self.imgHeight) = self.img.get_size()

        # Adjust the image to the widget target dimension
        sWidth = TARGET_WIDTH/self.imgWidth
        sHeight = TARGET_HEIGHT/self.imgHeight
        self.imgScaling = min(sWidth, sHeight)      
        self.imgScaled = pygame.transform.smoothscale(self.img, (int(self.imgWidth*self.imgScaling), int(self.imgHeight*self.imgScaling)))

        self.imgCoordX = (self.screenWidth-(int(self.imgWidth*self.imgScaling))) // 2
        self.imgCoordY = 50

        self.imgBox = (
          self.imgCoordX, 
          self.imgCoordY,
          self.imgCoordX + int(self.imgWidth*self.imgScaling), 
          self.imgCoordY + int(self.imgHeight*self.imgScaling)
        )

        self._indexLoaded = index

      else : 
        print(f"[DEBUG] Index = {index} has no image associated to it.")
        self.imgWidth = -1
        self.imgHeight = -1
        self._indexLoaded = index

        

  # ---------------------------------------------------------------------------
  # METHOD StaffScope.loadByCursor()
  # ---------------------------------------------------------------------------
  def loadByCursor(self, cursor) :
    """
    Loads the staff that covers the cursor value passed as argument.
    """
    
    # if ((index >= self.imgSpan[0]) and (index <= self.imgSpan[1])) :
    #   pass
    
    # else :
    #   index = self.db.getIndexByCursor(cursor)
    #   self.loadByIndex(index)



    # Temporary:
    self.loadByIndex(self._indexLoaded)


    
  # ---------------------------------------------------------------------------
  # METHOD StaffScope.render(cursor)
  # ---------------------------------------------------------------------------
  def render(self, cursor) :
    """
    Renders the current configuration (staff + "playglows")
    The function shall be called at each frame.
    """
    
    # Fetch the staff from the database
    self.loadByCursor(cursor)

    # Show the staff
    self.screen.blit(self.imgScaled, (self.imgCoordX, self.imgCoordY))
    
    # Show the playGlows
    transparent_surface = pygame.Surface((self.screenWidth, self.screenHeight), pygame.SRCALPHA)
    transparent_surface.fill((0, 0, 0, 0))  # Completely transparent
    
    transparent_color = (255, 255, 0, 128)
    rect_position = (446, 181, 30, 50)
    
    pygame.draw.rect(transparent_surface, transparent_color, rect_position)
    self.screen.blit(transparent_surface, (0, 0))



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.click(mouse coordinates)
  # ---------------------------------------------------------------------------
  def click(self, coord) :
    """
    Handles the mouse click based on its coordinates.
    Clicks when no staff is loaded are ignored.
    Clicks outside the StaffScope widget are ignored.
    """
    
    x = coord[0]; y = coord[1]
    
    # Is a staff loaded?
    if (self._indexLoaded != -1) :
      
      (img_xMin, img_yMin, img_xMax, img_yMax) = self.imgBox

      # Is the click on the staff?
      if (((x >= img_xMin) and (x <= img_xMax)) and ((y >= img_yMin) and (y <= img_yMax))) :
        print(f"[DEBUG] Click here: x = {coord[0]}, y = {coord[1]}")



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.populate(None)
  # ---------------------------------------------------------------------------
  def populate(self) :
    """
    Description is TODO.
    """
    
    print("[DEBUG] StaffScope.populate() is TODO")


    