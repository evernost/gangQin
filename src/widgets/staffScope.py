# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : staffScope
# File name     : staffScope.py
# File type     : Python script (Python 3)
# Purpose       : viewer widget containing the music score
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 20 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project specific constants
from src.commons import *

import src.scoreShot.database as database
import src.widgets.playGlow as playGlow
import src.widgets.widget as widget

import os         # For file name manipulation
import pygame     # For image scaling



# =============================================================================
# CONSTANTS
# =============================================================================
TARGET_WIDTH = 1300
TARGET_HEIGHT = 230



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class StaffScope(widget.Widget) :

  """
  STAFF_SCOPE object

  Class definition for the staffscope widget.
  
  The staffscope viewer displays the actual music score one snapshot at a time.
  The snapshot updates as the user plays and progresses in the song.
  Some visual cues highlight the current notes expected as well as some 
  stats about the estimated difficulty of a section.
  
  The StaffScope class derives from the Widget class.
  """

  def __init__(self, top) :
    
    # Call the Widget init method
    super().__init__(top, loc = WIDGET_LOC_UNDEFINED)

    self.songName     = ""      # Name of the song
    self.jsonName     = ""      # Name of the database file
    self.jsonFile     = ""      # Full name of the databse file (path + filename)
    self.depotFolder  = ""      # Directory where all the snapshots of the song are stored
    
    self.db = None              # Reference to the Database object
    self._dbIndex = -1          # Current index loaded from the database (-1 when none is loaded)
    self._dbCursor = -1
        
    #self.cursor = -1           # Not used anymore
    
    self.img = None             # Description is TODO
    self.imgScaled = None
    self.imgFile = ""
    self.imgSpan = [-1,-1]
    self.imgHeight = -1
    self.imgWidth = -1
    self.imgCoordX = -1
    self.imgCoordY = -1
    self.imgBox = (-1, -1, -1, -1)
    self.imgScaling = 0

    self.playGlows = []
    self.playGlowDragged = -1     # Index of the playGlow currently mouse dragged
    self.playGlowResized = -1     # Index of the playGlow currently resized

    self.activeHand = "L"

    self.ghostMode = False
    self._cacheClearReq = False

    self.rulersVisible = False

    self.cursorWrongNoteCount = []



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.load()
  # ---------------------------------------------------------------------------
  def load(self, songFile: str) -> None :
    """
    Loads and initialises the Staffscope object from a song file (usually '.pr' 
    or '.gq3' file)
    Displays the first staff available from the database.

    'songFile' must be the full path to the file.
    """

    self._initFileNames(songFile)

    self.db = database.Database(self.jsonFile)
    if not(self.db.isEmpty()) :
      self.loadImageByIndex(0)



  # ---------------------------------------------------------------------------
  # METHOD StaffScope._initFileNames()                                [PRIVATE]
  # ---------------------------------------------------------------------------
  def _initFileNames(self, songFile) :
    """
    Generates the various names of files and directories associated with the 
    database.
    """
    
    # TODO: forbid any whitespace in the name, or dots, commas, etc.
    
    (_, rootNameExt) = os.path.split(songFile)
    (rootName, _) = os.path.splitext(rootNameExt)
    self.songName     = rootName
    self.jsonName     = rootName + ".json"          # Example: "my_song.json"
    self.jsonFile     = f"./snaps/{self.jsonName}"  # Example: "./snaps/my_song.json"



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.isViewEmpty()
  # ---------------------------------------------------------------------------
  def isViewEmpty(self) -> bool :
    """
    Returns True if the current cursor has no score snapshot attached to it.

    In other words, if 'StaffScope.isViewEmpty()' returns True, there is no 
    staff view to display.
    """

    return (self._dbCursor == -1)



  # ---------------------------------------------------------------------------
  # METHOD Database.isDbEmpty()
  # ---------------------------------------------------------------------------
  def isDbEmpty(self, exitOnEmpty = True) :
    """
    Returns True if the database is empty. 
    Exits the app if the option 'exitOnEmpty' is set.
    """

    if self.db.isEmpty() :
      if exitOnEmpty :
        print("[ERROR] Staffscope database is empty! Capture the score first before calling this tool.")
        exit()
      
      else :
        print("[NOTE] Staffscope database is empty!")
        return True

    return False



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.nextStaff()
  # ---------------------------------------------------------------------------
  def nextStaff(self) :
    """
    Loads and shows the next staff.
    Clamps to the last staff when reaching the end of the score.
    """
    
    if ((self._dbIndex + 1) <= (self.db.nSnapshots-1)) :
      self.loadImageByIndex(self._dbIndex+1)
    
    else :
      print("[DEBUG] StaffScope.nextStaff(): end of database reached. No more staff to show.")

  
    
  # ---------------------------------------------------------------------------
  # METHOD StaffScope.previousStaff()
  # ---------------------------------------------------------------------------
  def previousStaff(self) :
    """
    Loads and shows the previous staff.
    Clamps to the first staff when reaching the beginning of the score.
    """
    
    if ((self._dbIndex - 1) >= 0) :
      self.loadImageByIndex(self._dbIndex-1)



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.loadImageByIndex()
  # ---------------------------------------------------------------------------
  def loadImageByIndex(self, index: int) -> None :
    """
    Loads and adjusts the image at position 'index' in the snapshots array.
    Once loaded, the '_dbIndex' is updated with the requested index.
    If no image exists at the requested index (either index is out of range,
    or the image cannot be found) then _dbIndex = -1.

    Use this if you know the exact index of the snapshot you want to load from
    the database.

    Usually though, this information is unknown and you might want to use 
    'StaffScope.loadImageByCursor()' instead.
    """
    
    # Load only if not cached yet
    if (index != self._dbIndex) :

      # Request the name of the file at that index
      self.imgFile = self.db.getSnapshotFileByIndex(index)
      
      # If there is such file (index is valid)
      if (self.imgFile != "") :
        
        # Load the image
        self.img = pygame.image.load(self.imgFile)
        (self.imgWidth, self.imgHeight) = self.img.get_size()

        # Resize the image to the target dimension of the widget
        sWidth = TARGET_WIDTH/self.imgWidth
        sHeight = TARGET_HEIGHT/self.imgHeight
        self.imgScaling = min(sWidth, sHeight)      
        self.imgScaled = pygame.transform.smoothscale(self.img, (int(self.imgWidth*self.imgScaling), int(self.imgHeight*self.imgScaling)))

        self.imgCoordX = (self.top.screenWidth-(int(self.imgWidth*self.imgScaling))) // 2
        self.imgCoordY = 50

        self.imgBox = (
          self.imgCoordX, 
          self.imgCoordY,
          self.imgCoordX + int(self.imgWidth*self.imgScaling), 
          self.imgCoordY + int(self.imgHeight*self.imgScaling)
        )

        # Loading success: update the current index pointer
        self._dbIndex = index

      else : 
        print(f"[WARNING] StaffScope.loadImageByIndex(): index {index} is out of range or image could not be found")
        self.imgScaled  = None
        self.imgWidth   = -1
        self.imgHeight  = -1
        self._dbIndex   = -1

        

  # ---------------------------------------------------------------------------
  # METHOD StaffScope.loadImageByCursor()
  # ---------------------------------------------------------------------------
  def loadImageByCursor(self, cursor: int) -> None :
    """
    Loads and adjusts the image corresponding to the Score 'cursor' value.
    """
    
    # Load the staff if:
    # - either the cursor changed
    # - a "clear cache" request occured
    if ((cursor != self._dbCursor) or self._cacheClearReq) :
      dbIndex = self.db.getIndexByCursor(cursor)
    
      if (dbIndex != -1) :
        self.loadImageByIndex(dbIndex)
        
        # TODO: move to a function
        # if self.ghostMode :
        #   self.playGlows = self.db.snapshots[dbIndex].getPlayGlowsInSnapshot(activeCursor = cursor)
        # else :
        #   self.playGlows = self.db.snapshots[dbIndex].getPlayGlowsAtCursor(cursor)
        
      self._dbCursor = cursor
      self._cacheClearReq = False



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.loadPlayGlowsByCursor()
  # ---------------------------------------------------------------------------
  def loadPlayGlowsByCursor(self, cursor: int) -> None :
    """
    Loads the playglows corresponding to the Score 'cursor' value.
    """
    
    dbIndex = self.db.getIndexByCursor(cursor)
  
    if (dbIndex != -1) :
      if self.ghostMode :
        self.playGlows = self.db.snapshots[dbIndex].getPlayGlowsInSnapshot(activeCursor = cursor)
      else :
        self.playGlows = self.db.snapshots[dbIndex].getPlayGlowsAtCursor(cursor)
        
    # The cursor is not linked to any staff (dbIndex = -1)
    # Clear the list of playglows to be rendered
    else :
      self.playGlows = []



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.isStaffAvailable()
  # ---------------------------------------------------------------------------
  def isStaffAvailable(self, cursor: int) :
    """
    Returns True if the current Score cursor has a score capture associated to it.
    """
    
    return (self.db.getIndexByCursor(cursor) != -1)
    


  # ---------------------------------------------------------------------------
  # METHOD StaffScope.render()
  # ---------------------------------------------------------------------------
  def render(self) :
    """
    Renders the staff and the playglows on screen.
    This function is called at every frame of the top level application.
    
    A staff must have been loaded prior to calling this function 
    ('StaffScope.loadImageByIndex()' or 'StaffScope.loadImageByCursor()')

    When the 'ghost mode' is ON, all the playglows of the snapshot are rendered.
    A color scheme helps distinguish the active/inactive playglows.
    """
    
    # In the v2.0 main:
    # if staffScopeWidget.isStaffAvailable(userScore.getCursor()) :
    #   staffScopeWidget.loadCursor(userScore.getCursor())
    #   staffScopeWidget.declareStats(statsObj.cursorWrongNoteCount)
    #   staffScopeWidget.render()
    
    # Ask the current cursor from the Score object
    scoreCursor = self.top.widgets[WIDGET_ID_SCORE].getCursor()

    self.loadImageByCursor(scoreCursor)
    self.loadPlayGlowsByCursor(scoreCursor)


    # Test if a staff has been loaded
    # if (self.imgScaled == None) :
    #   return

    # ----------------------
    # Render the staff image
    # ----------------------
    self.top.screen.blit(self.imgScaled, (self.imgCoordX, self.imgCoordY))
    


    # -----------------
    # Render the rulers
    # -----------------
    # TODO: add the handles.
    # The handles must be outside the score image
    if self.rulersVisible :
      #self.db.snapshots[index].rulerLeftHand
      pass



    # --------------------
    # Render the playGlows
    # --------------------
    transparent_surface = pygame.Surface((self.top.screenWidth, self.top.screenHeight), pygame.SRCALPHA)
    transparent_surface.fill((0, 0, 0, 0))  # Completely transparent
    
    for p in self.playGlows :
      if p.active :
        alpha = 128
      else :
        alpha = 20
      
      if (p.hand == "L") :
        coords = p.toTuple()
        r = pygame.draw.rect(transparent_surface, (255, 0, 0, alpha), coords)

        if not(p.active) :
          pygame.draw.rect(self.top.screen, (128, 128, 128), r, 1)

      elif (p.hand == "R") :
        coords = p.toTuple()
        pygame.draw.rect(transparent_surface, (0, 255, 0, alpha), coords)



    # -----------------------------------
    # Render the visual cues (stats info)
    # -----------------------------------
    if ((len(self.playGlows) > 0) and (len(self.cursorWrongNoteCount) > 0)) :
      
      # List all playglows on the staff with a non-zero wrong note count
      minCursor = self.db.snapshots[self._dbIndex].cursorMin
      maxCursor = self.db.snapshots[self._dbIndex].cursorMax
      leftHand_y = [-1]
      rightHand_y = [10000]
      wrongNotesHist = []
      
      # Left hand: determine the y-coordinate of the lowest playglow
      # Right hand: determine the y-coordinate of the highes playglow
      for n in range(minCursor, maxCursor + 1) :
        if str(n) in self.cursorWrongNoteCount :
          wrongNotesHist.append(self.cursorWrongNoteCount[str(n)])
        playglows = self.db.snapshots[self._dbIndex].getPlayGlowsAtCursor(n)
        for p in playglows :
          if p.active :
            if (p.hand == 'L') :
              leftHand_y += [p.coord_yMin, p.coord_yMax]
            else :
              rightHand_y += [p.coord_yMin, p.coord_yMax]      
      leftHand_yMax = max(leftHand_y)
      rightHand_yMin = min(rightHand_y)

      for n in range(minCursor, maxCursor + 1) :
        
        # Calculate the transparency based on the wrong note count
        playglows = self.db.snapshots[self._dbIndex].getPlayGlowsAtCursor(n)
        if str(n) in self.cursorWrongNoteCount :
          if (min(wrongNotesHist) != max(wrongNotesHist)) :
            alphaMin = 10
            alphaMax = 100
            w = self.cursorWrongNoteCount[str(n)]
            alpha = alphaMin + int((w - min(wrongNotesHist))*(alphaMax-alphaMin)/(max(wrongNotesHist) - min(wrongNotesHist)))
        else :
          alpha = 0

        # Draw the visual cue
        for p in playglows :
          if p.active :
            coords = p.toTuple()
            if (p.hand == 'L') :
              coords = (coords[0], leftHand_yMax, coords[2], 10)
              r = pygame.draw.rect(transparent_surface, (255, 127, 0, alpha), coords)

            elif (p.hand == 'R') :
              coords = (coords[0], rightHand_yMin - 10, coords[2], 10)
              r = pygame.draw.rect(transparent_surface, (0, 255, 127, alpha), coords)
              
            else :
              pass

    self.top.screen.blit(transparent_surface, (0, 0))



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.clickDown(mouse coordinates)
  # ---------------------------------------------------------------------------
  def clickDown(self, coord) :
    """
    Handles the pressing event of a click (left button).
    Clicks when no staff is loaded are ignored.
    Clicks outside the widget are ignored.
    """
    
    x = coord[0]; y = coord[1]
    self.playGlowDragged = -1
    
    # Is a staff loaded?
    if (self._dbIndex != -1) :
      
      # Is the click on the staff?
      (img_xMin, img_yMin, img_xMax, img_yMax) = self.imgBox
      if (((x >= img_xMin) and (x <= img_xMax)) and ((y >= img_yMin) and (y <= img_yMax))) :
        
        # Is the click on an existing playGlow?
        noHit = True
        for (i, p) in enumerate(self.playGlows) :
          if p.isClickOnBorder(coord) :
            self.playGlowResized = i
            p.resizeFrom(x,y)
            noHit = False
            print("[DEBUG] StaffScope.clickDown(): resize request")
          
          elif p.isClickInBox(coord) :
            self.playGlowDragged = i
            p.dragFrom(x,y)
            noHit = False
            print("[DEBUG] StaffScope.clickDown(): move request")

          

        # Click in empty space
        if noHit :
          for (i, p) in enumerate(self.playGlows) :
            if (p.hand == self.activeHand) :
              del self.playGlows[i]
              break
          
          print(f"[DEBUG] StaffScope.clickDown(): new playGlow (hand = {self.activeHand})")
          p = playGlow.PlayGlow()
          p.load((x-5, y-5, 10, 30))
          p.hand = self.activeHand
          self.db.snapshots[self._dbIndex].setPlayGlowAtCursor(self._dbCursor, p)
          self.playGlows.append(p)



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
      
      # CTRL + click = precision move
      if ctrlKey : 
        dx = (x-x0) // 10 
        dy = (y-y0) // 10
      
      # Click = basic move
      else :
        dx = x-x0 
        dy = y-y0
      
      self.playGlows[self.playGlowDragged].shift(dx,dy)

    elif (self.playGlowResized != -1) :
      pass

      # TODO
      





  # ---------------------------------------------------------------------------
  # METHOD StaffScope.clickUp(mouse coordinates)
  # ---------------------------------------------------------------------------
  def clickUp(self, coord) :
    """
    Handles the releasing event of a click (left button).
    In this GUI, it is used to handle the drag&drop feature.
    """
    
    # If something is being dragged
    if (self.playGlowDragged != -1) :
    
      # Commit the changes to the database
      p = self.playGlows[self.playGlowDragged]
      self.db.snapshots[self._dbIndex].setPlayGlowAtCursor(self._dbCursor, p)

      # Force a reload from the database
      self._cacheClearReq = True

      # Close the drag&drop event
      self.playGlowDragged = -1



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.setMouseCursor(None)
  # ---------------------------------------------------------------------------
  def setMouseCursor(self) :
    """
    Sets the mouse cursor based on its location over the app:
    - a reticle when over the staffScope
    - a move arrow when over the hitbox of a playglow
    - a resize arrow when in the resize hitbox of a playglow
    """

    pass



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.deletePlayGlow(None)
  # ---------------------------------------------------------------------------
  def deletePlayGlow(self) :
    """
    Deletes the active playglow shown on the GUI.
    """
    
    for (i, p) in enumerate(self.playGlows) :
      if (p.hand == self.activeHand) :
        print(f"[INFO] Deleting playglow at cursor {self._dbCursor} (hand = '{self.activeHand}')")
        del self.playGlows[i]
        
        self.db.snapshots[self._dbIndex].delPlayGlowAtCursor(self._dbCursor, p.hand)
        
        break



  # ---------------------------------------------------------------------------
  # METHOD StaffScope._getPlayGlowFromCursor(None)
  # ---------------------------------------------------------------------------
  def _getPlayGlowFromCursor(self) :
    """
    Description is TODO.
    """
    
    # Read the content of the database at that cursor
    if (self._dbIndex != -1) :
      s = self.db.snapshots[self._dbIndex].leftHandRectCoords

    # Convert to a playGlow object
    # ...

    print("[DEBUG] StaffScope._getPlayGlowFromCursor() is TODO")



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.populate(None)
  # ---------------------------------------------------------------------------
  def populate(self) :
    """
    Infers the location of playglows at the cursor location in-between 2 bounding
    cursor values (beginning and end) by a simple interpolation method.

    Use this function to preset the playglows. There is not garantee that the 
    proposed locations are correct, but it is a first placing.
    """
    
    print("[DEBUG] StaffScope.populate() is TODO")


    
  # ---------------------------------------------------------------------------
  # METHOD StaffScope.toggleGhostMode(None)
  # ---------------------------------------------------------------------------
  def toggleGhostMode(self) :
    """
    Toggles the 'ghost' mode i.e. switches between:
    - showing all the playglows of the snapshot, highlighting the active one 
    - showing the active playglow only.
    """
    
    if self.ghostMode :
      print("[INFO] staffScope: 'ghost' mode is OFF.")
    else :
      print("[INFO] staffScope: 'ghost' mode is ON.")
    
    self.ghostMode = not(self.ghostMode)

    # Clean the cache to force loading the staff and playglows
    self._cacheClearReq = True



  # ---------------------------------------------------------------------------
  # METHOD StaffScope.toggleRulers(None)
  # ---------------------------------------------------------------------------
  def toggleRulers(self) :
    """
    Description is TODO.
    """
    
    if self.rulersVisible :
      print("[INFO] staffScope: 'ghost mode' is OFF.")
    else :
      print("[INFO] staffScope: 'ghost mode' is ON.")
    
    self.rulersVisible = not(self.rulersVisible)

  

  # ---------------------------------------------------------------------------
  # METHOD StaffScope.declareStats(cursorWrongNoteCount)
  # ---------------------------------------------------------------------------
  def declareStats(self, cursorWrongNoteCount) :
    """
    Description is TODO.
    """

    self.cursorWrongNoteCount = cursorWrongNoteCount


# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  
  print("[INFO] Library 'StaffScope' called as main: running unit tests...")

  songFile = SONG_PATH + "/" + "Rachmaninoff_Piano_Concerto_No2_Op18.gq3"
  scope = StaffScope(top = None)
  scope.load(songFile)
