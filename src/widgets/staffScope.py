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

    self._snapshotIndex = -1      # Index of the snapshot loaded (-1 when nothing is loaded)

    self.playGlows = []
    self.playGlowDragged = -1     # Index of the playGlow currently mouse dragged

    self.activeHand = "L"

    self.ghostMode = False

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
    
    if ((self._snapshotIndex + 1) <= (self.db.nSnapshots-1)) :
      self.loadStaffByIndex(self._snapshotIndex+1)


    
  # ---------------------------------------------------------------------------
  # METHOD StaffScope.previousStaff()
  # ---------------------------------------------------------------------------
  def previousStaff(self) :
    """
    Loads and shows the previous staff.
    Clamps to the first staff when reaching the beginning of the score.
    """
    
    if ((self._snapshotIndex - 1) >= 0) :
      self.loadStaffByIndex(self._snapshotIndex-1)



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.loadStaffByIndex()
  # ---------------------------------------------------------------------------
  def loadStaffByIndex(self, index) :
    """
    Loads the content located at position "index" in the snapshot database.
    Once loaded, the "_snapshotIndex" is updated with the requested index.
    """
    
    # Load only if not cached yet
    if (self._snapshotIndex != index) :

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

        self._snapshotIndex = index

      else : 
        print(f"[DEBUG] Index = {index} has no image associated to it.")
        self.imgWidth = -1
        self.imgHeight = -1
        self._snapshotIndex = index

        

  # ---------------------------------------------------------------------------
  # METHOD StaffScope.loadStaffByCursor()
  # ---------------------------------------------------------------------------
  def loadStaffByCursor(self, cursor) :
    """
    Loads the staff that covers the cursor value passed as argument.
    Loads the playglows (left and right hand)
    Loading has a cache to avoid useless workload.
    """
    
    if (cursor != self.cursor) :
      index = self.db.getIndexByCursor(cursor)
    
      # The cursor is linked to a staff:
      # - load the staff 
      # - load the playglows (if any)
      if (index != -1) :
        self.loadStaffByIndex(index)
        self.playGlows = self.db.snapshots[index].getPlayGlowAtCursor(cursor)
        
      # The cursor is not linked to any staff:
      # - load a default index (the one pointed by the user)
      # - no playglow is shown, waiting for user input.
      else :
        self.loadStaffByIndex(self._snapshotIndex)
        self.playGlows = []
        print(f"[DEBUG] Cursor {cursor} is not linked to any staff. Proceed with playglow input")

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

    # Render the staff
    self.screen.blit(self.imgScaled, (self.imgCoordX, self.imgCoordY))
    
    # Render the playGlows
    transparent_surface = pygame.Surface((self.screenWidth, self.screenHeight), pygame.SRCALPHA)
    transparent_surface.fill((0, 0, 0, 0))  # Completely transparent
    
    for p in self.playGlows :
      if (p.hand == "L") :
        coords = p.toTuple()
        pygame.draw.rect(transparent_surface, (255, 0, 0, 128), coords)
        self.screen.blit(transparent_surface, (0, 0))

      elif (p.hand == "R") :
        coords = p.toTuple()
        pygame.draw.rect(transparent_surface, (0, 255, 0, 128), coords)
        self.screen.blit(transparent_surface, (0, 0))



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.clickDown(mouse coordinates)
  # ---------------------------------------------------------------------------
  def clickDown(self, coord) :
    """
    Handles the pressing event of a click (left button).
    Clicks when no staff is loaded are ignored.
    Clicks outside the StaffScope widget are ignored.
    """
    
    x = coord[0]; y = coord[1]
    self.playGlowDragged = -1
    
    # Is a staff loaded?
    if (self._snapshotIndex != -1) :
      
      # Is the click on the staff?
      (img_xMin, img_yMin, img_xMax, img_yMax) = self.imgBox
      if (((x >= img_xMin) and (x <= img_xMax)) and ((y >= img_yMin) and (y <= img_yMax))) :
        
        # Is the click on an existing playGlow?
        noHit = True
        for (i, p) in enumerate(self.playGlows) :
          if p.isClickInBox(coord) :
            self.playGlowDragged = i
            p.dragFrom(x,y)
            noHit = False
            print("[DEBUG] Move request")

          elif p.isClickOnBorder(coord) :
            noHit = False
            print("[DEBUG] Resize request")

        # Create a playglow at the location of the click
        if noHit :
          print("[DEBUG] New playGlow")
          p = playGlow.PlayGlow()
          p.load((x-5, y-5, 10, 30))
          p.hand = self.activeHand
          self.db.snapshots[self._snapshotIndex].setPlayGlowAtCursor(self.cursor, p)

          # Faux : il faut remplacer le playGlow 
          # Là ils vont tous être effacés !
          self.playGlows = []
          self.playGlows.append(p)
        


  # ---------------------------------------------------------------------------
  # METHOD StaffScope.clickUp(mouse coordinates)
  # ---------------------------------------------------------------------------
  def clickUp(self, coord) :
    """
    Handles the releasing event of a click (left button).
    In this GUI, it is used to handle the drag&drop feature.
    """
    
    # Apply the changes to the object
    # self.playGlows[self.playGlowDragged].shiftApply()

    # Commit the changes to the database
    p = self.playGlows[self.playGlowDragged]
    self.db.snapshots[self._snapshotIndex].setPlayGlowAtCursor(self.cursor, p)

    # Close the drag&drop event
    self.playGlowDragged = -1



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.mouseMove(mouse coordinates)
  # ---------------------------------------------------------------------------
  def mouseMove(self, coord, ctrlKey) :
    """
    Handles a mouse move over the GUI.
    In this GUI, it is used to handle the drag&drop feature.
    """
    
    # TODO: ensure continuity of the coordinates when switching from 
    # 'coarse' move to 'fine' move (when CTRL key is pressed)

    if (self.playGlowDragged != -1) :
      (x0, y0) = (self.playGlows[self.playGlowDragged].dragCoord_x, self.playGlows[self.playGlowDragged].dragCoord_y)
      x = coord[0]; y = coord[1]
      if ctrlKey : 
        dx = (x-x0) // 10; dy = (y-y0) // 10
      else :
        dx = x-x0; dy = y-y0
      
      self.playGlows[self.playGlowDragged].shift(dx,dy)

    

  # ---------------------------------------------------------------------------
  # METHOD StaffScope.deletePlayGlow(None)
  # ---------------------------------------------------------------------------
  def deletePlayGlow(self) :
    """
    Delete the active playglow shown on the GUI.
    """
    
    print("[DEBUG] StaffScope.deletePlayGlow() is TODO")



  # ---------------------------------------------------------------------------
  # METHOD StaffScope._getPlayGlowFromCursor(None)
  # ---------------------------------------------------------------------------
  def _getPlayGlowFromCursor(self) :
    """
    Description is TODO.
    """
    

    # Read the content of the database at that cursor
    if (self._snapshotIndex != -1) :
      s = self.db.snapshots[self._snapshotIndex].leftHandRectCoords

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


    