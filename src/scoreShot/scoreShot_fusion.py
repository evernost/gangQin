# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : scoreShot_fusion
# File name     : scoreShot_fusion.py
# Purpose       : score snapshots / MIDI file merging tool
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Saturday, 19 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs 
# =============================================================================
from src.commons import *

import src.widgets.keyboard as keyboard
import src.score as score
import src.text as text

import src.scoreShot.database as database

import pygame
import os



# =============================================================================
# Constants pool
# =============================================================================
TARGET_WIDTH = 1300
TARGET_HEIGHT = 230



# =============================================================================
# Main code
# =============================================================================

# TODO: call a file selection GUI.
songFile = "./songs/Rachmaninoff_Moment_Musical_Op_16_No_4.pr"



pygame.init()

# Define screen dimensions
screenWidth = 1320
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Time management
clock = pygame.time.Clock()

# Import file in the internal score representation
userScore = score.Score()
userScore.importFromFile(songFile)

# Grand piano widget
keyboardWidget = keyboard.Keyboard(loc = (10, 300))


db = database.Database(songFile)


# Create window
pygame.display.set_caption(f"scoreShot Fusion - v0.1 [ALPHA] (October 2024) - <{os.path.basename(songFile)}>")

# Enable key repeats (250 ms delay before repeat, repeat every 50 ms)
pygame.key.set_repeat(250, 50)


imgIndex = 0

running = True

clickMsg = False
ctrlKey  = False
altKey   = False

# =============================================================================
# Main loop
# =============================================================================
while running :
  for event in pygame.event.get() :
    if (event.type == pygame.QUIT) :
      running = False

    # -------------------------------------------------------------------------
    # Keyboard event handling
    # -------------------------------------------------------------------------
    if (event.type == pygame.KEYUP) :
      keys    = pygame.key.get_pressed()
      ctrlKey = event.mod & pygame.KMOD_CTRL
      altKey  = event.mod & pygame.KMOD_ALT
      shiftKey  = event.mod & pygame.KMOD_SHIFT
    
    elif (event.type == pygame.KEYDOWN) :
      keys    = pygame.key.get_pressed()
      ctrlKey = event.mod & pygame.KMOD_CTRL
      altKey  = event.mod & pygame.KMOD_ALT
      shiftKey  = event.mod & pygame.KMOD_SHIFT

      # -----------------
      # "q": exit the app
      # -----------------
      if keys[pygame.K_q] :
        print("")
        print("See you!")
        pygame.quit()
        raise SystemExit(0)

      # ----------------------------------
      # Left arrow: jump backward (1 step)
      # ----------------------------------
      if (keys[pygame.K_LEFT] and not(ctrlKey) and not(altKey)) :
        userScore.cursorStep(-1)
        imgIndex -= 1

      # ----------------------------------
      # Right arrow: jump forward (1 step)
      # ----------------------------------
      if (keys[pygame.K_RIGHT] and not(ctrlKey) and not(altKey)) :
        userScore.cursorStep(1)
        imgIndex += 1

      # -----------------------------------------
      # CTRL + Left arrow: fast rewind (10 steps)
      # -----------------------------------------
      if (keys[pygame.K_LEFT] and ctrlKey) :
        userScore.cursorStep(-10)

      # -------------------------------------------
      # CTRL + right arrow: fast forward (10 steps)
      # -------------------------------------------
      if (keys[pygame.K_RIGHT] and ctrlKey) :
        userScore.cursorStep(10)

      # ---------------------------------------
      # HOME: jump to the beginning of the file
      # ---------------------------------------
      if (keys[pygame.K_HOME]) :
        userScore.cursorBegin()

      # --------------------------------
      # END: jump to the end of the file
      # --------------------------------
      if (keys[pygame.K_END]) :
        userScore.cursorEnd()

      # -----------------------------------
      # Down: jump to the previous bookmark
      # -----------------------------------
      if (keys[pygame.K_DOWN]) :
        userScore.gotoPreviousBookmark()

      # -----------------------------
      # Up: jump to the next bookmark
      # -----------------------------
      if (keys[pygame.K_UP]) :
        userScore.gotoNextBookmark()

      

      # ----------------
      # "s": export/save
      # ----------------
      # if (keys[pygame.K_s]) :
        # print("[INFO] Exporting piano roll...")
        # (rootDir, rootNameExt) = os.path.split(selectedFile)
        # (rootName, _) = os.path.splitext(rootNameExt)
        # newName = rootDir + '/' + rootName + ".pr"
        # userScore.exportToPrFile(newName)
        # pygame.display.set_caption(f"gangQin - v{REV_MAJOR}.{REV_MINOR} [{REV_TYPE}] ({REV_MONTH} {REV_YEAR}) - <{rootName}.pr>")

      

    # -------------------------------------------------------------------------
    # Mouse click event handling
    # -------------------------------------------------------------------------
    elif (event.type == pygame.MOUSEBUTTONDOWN) :
      
      # Left click
      if (event.button == MOUSE_LEFT_CLICK) :
        clickMsg = True
        clickCoord = pygame.mouse.get_pos()
        #print(f"[DEBUG] Click here: x = {clickCoord[0]}, y = {clickCoord[1]}")
      
      # Scroll up
      if (event.button == MOUSE_SCROLL_UP) :
        if ctrlKey :
          userScore.cursorStep(10)
        else :
          userScore.cursorStep(1)

      # Scroll down
      if (event.button == MOUSE_SCROLL_DOWN) :
        if ctrlKey :
          userScore.cursorStep(-10)
        else :
          userScore.cursorStep(-1)




  # Clear the screen
  screen.fill(BACKGROUND_COLOR)

  # Draw the keyboard on screen
  keyboardWidget.reset()
  keyboardWidget.drawKeys(screen)
  
  # Show the teacher notes on the keyboard widget
  teacherNotes = userScore.getTeacherNotes()
  keyboardWidget.keyPress(screen, teacherNotes)

  # Load the score image
  imgName = db.getSnapshotNameByIndex(imgIndex)
  if (imgName != "") :
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





  
  # CURSOR
  text.showCursor(screen, userScore.getCursor(), userScore.scoreLength)
  
  # BOOKMARK
  text.showBookmark(screen, userScore.getBookmarkIndex())
 


  clock.tick(FPS)

  # Update the display
  pygame.display.flip()

# Quit Pygame
pygame.quit()


