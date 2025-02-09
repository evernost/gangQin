# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : scoreShot_fusion
# File name     : scoreShot_fusion.py
# File type     : Python script (Python 3)
# Purpose       : score snapshots / MIDI file merging tool
# Author        : QuBi (nitrogenium@outlook.fr)
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
import src.widgets.handSelector as handSelector
import src.widgets.scoreStatus as scoreStatus

import src.scoreShot.fileSelectionGUI as fileSelectionGUI

import src.score as score
import src.text as text

import pygame
import os



# =============================================================================
# Constants pool
# =============================================================================
# None.



# =============================================================================
# Main code
# =============================================================================

# Call the song file selection GUI
fileSel = fileSelectionGUI.new()
fileSel.setTitle("ScoreShot (Fusion) - New session")
songFile = fileSel.show()

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
staffScopeWidget.checkEmpty()

# Finger editor widget
handSelWidget = handSelector.handSelector()
handSelWidget.setScreen(screen)

# Score status widget
scoreStatusWidget = scoreStatus.scoreStatus()
scoreStatusWidget.setScreen(screen)



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

      # ------------------------
      # "g": toggle 'ghost' mode
      # ------------------------
      if keys[pygame.K_g] :
        staffScopeWidget.toggleGhostMode()

      # -------------
      # "p": populate
      # -------------
      if keys[pygame.K_p] :
        staffScopeWidget.populate()

      # ------------------
      # "r": toggle rulers
      # ------------------
      if keys[pygame.K_r] :
        staffScopeWidget.toggleRulers()

      # -----------------
      # "q": exit the app
      # -----------------
      if keys[pygame.K_q] :
        
        # Look for unsaved changes
        # ...
        
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

      # ---------------------------
      # Del: delete active playglow
      # ---------------------------
      if (keys[pygame.K_DELETE]) :
        staffScopeWidget.deletePlayGlow()

      # ----------------
      # "s": export/save
      # ----------------
      if (keys[pygame.K_s]) :
        print("[DEBUG] Requesting save from the database...")
        staffScopeWidget.db.save()
        


    # -------------------------------------------------------------------------
    # Mouse click event handling
    # -------------------------------------------------------------------------
    elif (event.type == pygame.MOUSEBUTTONDOWN) :
      
      if (event.button == MOUSE_LEFT_CLICK) :
        coord = pygame.mouse.get_pos()
        staffScopeWidget.clickDown(coord)
        handSelWidget.clickDown(coord)

      if (event.button == MOUSE_RIGHT_CLICK) :
        coord = pygame.mouse.get_pos()
        handSelWidget.rightClickDown(coord)
      
      # TODO: disable scrolling if drag&drop is ongoing
      if (event.button == MOUSE_SCROLL_UP) :
        if ctrlKey :
          userScore.cursorStep(10)
        else :
          userScore.cursorStep(1)

      if (event.button == MOUSE_SCROLL_DOWN) :
        if ctrlKey :
          userScore.cursorStep(-10)
        else :
          userScore.cursorStep(-1)

    elif (event.type == pygame.MOUSEBUTTONUP) :
      if (event.button == MOUSE_LEFT_CLICK) :
        coord = pygame.mouse.get_pos()
        staffScopeWidget.clickUp(coord)

    elif (event.type == pygame.MOUSEMOTION) :
      coord = pygame.mouse.get_pos()
      staffScopeWidget.mouseMove(coord, ctrlKey)



  # Clear the screen
  screen.fill(BACKGROUND_COLOR)

  # Draw the keyboard on screen
  keyboardWidget.reset()
  keyboardWidget.render(screen)
  
  # Show the teacher notes on the keyboard widget
  teacherNotes = userScore.getTeacherNotes()
  keyboardWidget.keyPress(screen, teacherNotes)

  # Render the staff display
  staffScopeWidget.loadCursor(userScore.getCursor())
  staffScopeWidget.render()

  # Render the left/right hand selector
  handSelWidget.render()
  for msg in handSelWidget.msgQueueOut : 
    if (msg == handSelector.Msg.SET_TO_LEFT_HAND) :
      staffScopeWidget.activeHand = "L"
    elif (msg == handSelector.Msg.SET_TO_RIGHT_HAND) :
      staffScopeWidget.activeHand = "R"

  # Render the text on screen
  text.showCursor(screen, userScore.getCursor(), userScore.scoreLength)
  text.showBookmark(screen, userScore.getBookmarkIndex())
 
  # Change the mouse cursor 
  coord = pygame.mouse.get_pos()
  # staffScopeWidget.setMouseCursor(coord)

  clock.tick(FPS)

  # Update the display
  pygame.display.flip()

# Quit Pygame
pygame.quit()


