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
import src.widgets.staffScope as staffScope
import src.score as score
import src.text as text

#import src.scoreShot.database as database

import pygame
import os



# =============================================================================
# Constants pool
# =============================================================================
# None.



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

# StaffScope widget
staffScopeWidget = staffScope.StaffScope()
staffScopeWidget.setScreen(screen, screenWidth, screenHeight)
staffScopeWidget.load(songFile)

# Create window
pygame.display.set_caption(f"scoreShot Fusion - v0.1 [ALPHA] (October 2024) - <{os.path.basename(songFile)}>")

# Enable key repeats (250 ms delay before repeat, repeat every 50 ms)
pygame.key.set_repeat(250, 50)



running = True

# TODO: get rid of these.
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

      # ----------------------------------
      # Right arrow: jump forward (1 step)
      # ----------------------------------
      if (keys[pygame.K_RIGHT] and not(ctrlKey) and not(altKey)) :
        userScore.cursorStep(1)

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

      # ----------------------
      # Page up: next snapshot
      # ----------------------
      if (keys[pygame.K_PAGEUP]) :
        staffScopeWidget.nextStaff()

      # ----------------------------
      # Page down: previous snapshot
      # ----------------------------
      if (keys[pygame.K_PAGEDOWN]) :
        staffScopeWidget.previousStaff()

      # ----------------
      # "s": export/save
      # ----------------
      if (keys[pygame.K_s]) :
        print("[DEBUG] Saving is not supported yet.")
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
        coord = pygame.mouse.get_pos()
        staffScopeWidget.click(coord)
      
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

  # Load the staff display
  staffScopeWidget.loadByCursor(userScore.getCursor())

  # CURSOR
  text.showCursor(screen, userScore.getCursor(), userScore.scoreLength)
  
  # BOOKMARK
  text.showBookmark(screen, userScore.getBookmarkIndex())
 


  clock.tick(FPS)

  # Update the display
  pygame.display.flip()

# Quit Pygame
pygame.quit()


