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
import src.widgets.playGlow as playGlow
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
    
    self.cursor = -1

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

    self.activeHand = "L"

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
    Displays the first staff available from the database.
    """

    self.db = database.Database(songFile)
    self.loadStaffByIndex(0)



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.nextStaff()
  # ---------------------------------------------------------------------------
  def nextStaff(self) :
    """
    Loads and shows the next staff.
    Clamps to the last staff when reaching the end of the score.
    """
    
    if ((self._indexLoaded + 1) <= (self.db.nSnapshots-1)) :
      self.loadStaffByIndex(self._indexLoaded+1)


    
  # ---------------------------------------------------------------------------
  # METHOD StaffScope.previousStaff()
  # ---------------------------------------------------------------------------
  def previousStaff(self) :
    """
    Loads and shows the previous staff.
    Clamps to the first staff when reaching the beginning of the score.
    """
    
    if ((self._indexLoaded - 1) >= 0) :
      self.loadStaffByIndex(self._indexLoaded-1)



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.loadStaffByIndex()
  # ---------------------------------------------------------------------------
  def loadStaffByIndex(self, index) :
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
  # METHOD StaffScope.loadStaffByCursor()
  # ---------------------------------------------------------------------------
  def loadStaffByCursor(self, cursor) :
    """
    Loads the staff that covers the cursor value passed as argument.
    Loading comes with a cache to avoid useless workload.
    """
    
    if (cursor != self.cursor) :
      index = self.db.getIndexByCursor(cursor)
    
      # The cursor is not linked to a staff:
      # - load a default index (the one pointed by the user)
      # - no playGlow is shown, waiting for user input.
      if (index == -1) :
        self.loadStaffByIndex(self._indexLoaded)
        self.playGlowLeft = []
        self.playGlowRight = []
        print(f"[DEBUG] Cursor {cursor} is not linked to any staff. Proceed with playglow input")
        
      # The cursor is linked:
      # - load the staff 
      # - load the playglows (if any)
      else :
        self.loadStaffByIndex(index)

        # Load the playGlows (left and right)
        p = self.db.snapshots[index].getPlayGlowByCursor(cursor)
        self.playGlowLeft = playGlow.PlayGlow()
        self.playGlowRight = playGlow.PlayGlow()

      self.cursor = cursor

    # Cursor hasn't changed: read from cache.
    else : 
      pass



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.render(None)
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Renders the current configuration (staff + "playglows")
    The function shall be called at each frame.
    
    A staff must have been loaded prior to calling this function 
    ('loadStaffByIndex' or 'loadStaffByCursor')
    """
    
    # Test if a staff has been loaded
    # ...

    # Show the staff
    self.screen.blit(self.imgScaled, (self.imgCoordX, self.imgCoordY))
    
    # Show the playGlows
    if (len(self.playGlowLeft) != 0) :
      transparent_surface = pygame.Surface((self.screenWidth, self.screenHeight), pygame.SRCALPHA)
      transparent_surface.fill((0, 0, 0, 0))  # Completely transparent
      
      transparent_color = (255, 0, 0, 128)
      #rect_position = (446, 181, 30, 50)
      rect_position = (self.playGlowLeft[0], self.playGlowLeft[1], self.playGlowLeft[2], self.playGlowLeft[3])
      
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
      
      # Is the click coordinates on the staff?
      (img_xMin, img_yMin, img_xMax, img_yMax) = self.imgBox
      if (((x >= img_xMin) and (x <= img_xMax)) and ((y >= img_yMin) and (y <= img_yMax))) :
        
        # Is the click on a playGlow?
        # ...
        
        
        self.playGlowLeft = [x-5, y-5, 10, 30]






  # ---------------------------------------------------------------------------
  # METHOD StaffScope._getPlayGlowFromCursor(None)
  # ---------------------------------------------------------------------------
  def _getPlayGlowFromCursor(self) :
    """
    Description is TODO.
    """
    

    # Read the content of the database at that cursor
    if (self._indexLoaded != -1) :
      s = self.db.snapshots[self._indexLoaded].leftHandRectCoords

    # Convert to a playGlow object
    # ...

    print("[DEBUG] StaffScope._getPlayGlowFromCursor() is TODO")





  # ---------------------------------------------------------------------------
  # METHOD StaffScope.populate(None)
  # ---------------------------------------------------------------------------
  def populate(self) :
    """
    Description is TODO.
    """
    
    print("[DEBUG] StaffScope.populate() is TODO")


    