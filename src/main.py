# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : main
# File name     : main.py
# Purpose       : application entry point
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Friday, 1 Sept 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# TODO list
# =============================================================================

# Mandatory:
# - allow user to set the finger using numbers on the keypad
# - when editing the finger of an unedited note, FingerSelector shall be set 
#   on a default selector that matches with the hand of the note
# - highlight the activeNote ie the note whose finger is currently being associated
# - fingerSelGui should be visible and have focus 
# - allow the user to transfer a hand from one hand to the other
#   That involves inserting a note in <noteOnTimecodes>
# - allow the user to practice hands separately
# - loop feature between 2 bookmarks
# - allow the user to add some comments that can span on one to several timecodes
#   Comments can be guidelines on the way to play, any notes really.
# - during MIDI import: ask the user which tracks to use (there might be more than 2)
# - patch the keypress management in the code (combinations of CTRL+... are buggy)
# - issue: some notes from the teacher are shown in grey.
# - investigate the origin of the empty lists in the .pr file
#   Is it normal?
# - auto-increase the step size if CTRL+left/right is hit multiple times in a row 

# Nice to have:
# - inform the user somehow that he is not playing the expected note
# - patch the obscure variable names in keyboardUtils
# - add a play button to hear some sections
# - <drawPianoRoll>: compute polygons once for all. Don't recompute them if time code hasn't changed
# - add "if __main__" in all libs
# - add autosave feature (save snapshot every 2 minutes)
# - show a "*" in the title bar as soon as there are unsaved changes in the pianoRoll object

# Later:
# - change the framework, use pyqt instead
# - complete the font library (fontUtils.py)
# - a dropdown list with all .mid/.pr files found instead of changing manually the variable
# - <midiCallback>: handle MIDI keyboards that send <noteON> messages with 0 velocity as a <noteOFF>

# Done:
# - add a fast forward option
# - draw the piano roll
# - handle properly the case of no MIDI interface selected (navigation mode)
# - add shortcut to jump to the first / last note
# - if a note is played on the keyboard, the note is correct but isn't enough to progress in 
#   the song (eg another note is missing) the colors overlap.
# - allow the user to play the requested notes while sustaining the previous ones
# - patch the bad exit behavior upon pressing "q"
# - import/export the piano roll and all the metadata
# - note select for an edit shall have a hitbox that spans the entire key. Not only the lit part.
# - allow the user to edit note properties (finger)



# =============================================================================
# External libs 
# =============================================================================
# Project specific constants
from commons import *

# For graphics
import pygame

# Widgets
from widgets import keyboard
from widgets import pianoRoll
from widgets import fingerSelector



import fontUtils as fu
import conf
import utils
import score


# For MIDI
import mido
import rtmidi

# For?
import os





# =============================================================================
# Constants pool
# =============================================================================




# =============================================================================
# General settings
# =============================================================================
# Defines the criteria to decide when to move onto the next notes
# - "exact": won't go further until the expected notes only are pressed, nothing else
# - "allowSustain": accepts that the last valid notes are sustained
playComparisonMode = "allowSustain"



# =============================================================================
# Main code
# =============================================================================

# Open the MIDI interface file selection GUI
(selectedDevice, selectedFile) = conf.showSetupGUI()

if (selectedFile == "" or selectedFile == "None") :
  raise SystemExit(0)

pygame.init()

# Define screen dimensions
screenWidth = 1320
screenHeight = 500
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Time management
FPS = 60
clock = pygame.time.Clock()

# Create widgets
keyboardWidget = keyboard.Keyboard((10, 300))
pianoRollWidget = pianoRoll.PianoRoll(x = 10, yTop = 50, yBottom = 300-2)
fingerSelWidget = fingerSelector.FingerSelector((500, 470))

# Create score and import file
userScore = score.Score()
userScore.importFromFile(selectedFile)

# Ajust the piano roll view
pianoRollWidget.importPianoRoll(userScore.pianoRoll)
pianoRollWidget.viewSpan = userScore.avgNoteDuration*PIANOROLL_VIEW_SPAN

# Set the background color
backgroundRGB = (180, 177, 226)

# Create window
pygame.display.set_caption(f"gangQin App - v{REV_MAJOR}.{REV_MINOR} ({REV_MONTH}. {REV_YEAR}) - <{os.path.basename(selectedFile)}>")



# =============================================================================
# Open MIDI keyboard interface
# =============================================================================
midiCurr = [0 for _ in range(128)]
midiSustained = [0 for _ in range(128)]

# Define the MIDI callback
def midiCallback(message) :
  if (message.type == 'note_on') :
    # print(f"[DEBUG] Note On: Note = {message.note}, Velocity = {message.velocity}")
    midiCurr[message.note] = 1
  elif (message.type == 'note_off') :
    # print(f"[DEBUG] Note Off: Note = {message.note}, Velocity = {message.velocity}")
    midiCurr[message.note] = 0
    midiSustained[message.note] = 0 # this note cannot be considered as sustained anymore

if (conf.selectedDevice != "None") :
  midiPort = mido.open_input(conf.selectedDevice, callback = midiCallback)
else :
  print("[WARNING] No MIDI interface selected: running in navigation mode.")
  midiPort = None



# =============================================================================
# Main loop
# =============================================================================
running = True
currTime = 0

clickMsg = False

while running :
  for event in pygame.event.get() :
    if (event.type == pygame.QUIT) :
      running = False

    # -------------------------------------------------------------------------
    # Keyboard event handling
    # -------------------------------------------------------------------------
    if (event.type == pygame.KEYDOWN) :
      keys = pygame.key.get_pressed()

      # -----------------
      # "q": exit the app
      # -----------------
      if keys[pygame.K_q] :
        if (midiPort != None) :
          midiPort.close()
        
        print("See you!")
        pygame.quit()
        raise SystemExit(0)

      # ----------------------------------
      # Left arrow: jump backward (1 step)
      # ----------------------------------
      if (keys[pygame.K_LEFT] and not(keys[pygame.K_LCTRL])) :
        userScore.cursorStep(-1)

      # -----------------------------------------
      # CTRL + Left arrow: fast rewind (10 steps)
      # -----------------------------------------
      if (keys[pygame.K_LEFT] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL])) :
        userScore.cursorStep(-10)

      # ----------------------------------
      # Right arrow: jump forward (1 step)
      # ----------------------------------
      if (keys[pygame.K_RIGHT] and not(keys[pygame.K_LCTRL])) :
        userScore.cursorStep(1)

      # -------------------------------------------
      # CTRL + right arrow: fast forward (10 steps)
      # -------------------------------------------
      if (keys[pygame.K_RIGHT] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL])) :
        userScore.cursorStep(10)

      # ----------------------------------------------
      # CTRL + HOME: jump to the beginning of the file
      # ----------------------------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_HOME]) :
        userScore.cursorReset()

      # ---------------------------------------
      # CTRL + END: jump to the end of the file
      # ---------------------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_END]) :
        print("[INFO] Supported in a future release")

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

      # -----------------------------------------------
      # Keypad 1 to 5: assign finger to a selected note
      # -----------------------------------------------
      if (keys[pygame.K_KP1] or keys[pygame.K_KP2] or keys[pygame.K_KP3] or keys[pygame.K_KP4] or keys[pygame.K_KP5]) :
        print("[INFO] Supported in a future release")
      
      # ----------------------------------------
      # "b": toggle a bookmark on this timestamp
      # ----------------------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_b]) :
        userScore.toggleBookmark()
      
      # ------------------
      # "c": add a comment
      # ------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_c]) :
        print("[NOTE] Adding comments will be available in a future release.")

      # ----------------------------
      # "h": (Hear) toggle play mode
      # ----------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_h]) :
        print("[NOTE] Playing the song feature will be added in a future release.")

      # ---------------------------------------------
      # "k": toggle display of the notes in the scale
      # ---------------------------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_k]) :
        print("[NOTE] Displaying the notes in the scale will be added in a future release.")

      # ------------------------------------
      # CTRL + k: set the key the song is in
      # ------------------------------------
      if (keys[pygame.K_LCTRL] and keys[pygame.K_k]) :
        print("[NOTE] Setting the key of the song will be added in a future release.")

      # ---------------------------------
      # "l": enable/disable the left hand
      # ---------------------------------
      if (keys[pygame.K_l]) :  
        userScore.toggleLeftHand()

      # -----------------------
      # "p": loop practice mode
      # -----------------------
      if (keys[pygame.K_p]) :
        userScore.toggleLoopMode()

      # ----------------------------------
      # "r": enable/disable the right hand
      # ----------------------------------
      if (keys[pygame.K_r]) :
        userScore.toggleRightHand()

      # ----------------
      # "s": export/save
      # ----------------
      if (keys[pygame.K_s]) :
        print("[NOTE] Exporting piano roll...")
        (rootDir, rootNameExt) = os.path.split(selectedFile)
        (rootName, _) = os.path.splitext(rootNameExt)
        newName = rootDir + '/' + rootName + ".pr"
        userScore.exportToPrFile(newName)
        pygame.display.set_caption(f"gangQin App - v{REV_MAJOR}.{REV_MINOR} ({REV_MONTH}. {REV_YEAR}) - {rootName}.pr")

      # -------------------------
      # Space key: rehearsal mode
      # -------------------------
      if (keys[pygame.K_SPACE]) :
        userScore.toggleRehearsalMode()

    # -------------------------------------------------------------------------
    # Mouse click event handling
    # -------------------------------------------------------------------------
    if (event.type == pygame.MOUSEBUTTONDOWN) :
      
      # Left click
      if (event.button == MOUSE_LEFT_CLICK) :
        clickMsg = True
        clickX, clickY = pygame.mouse.get_pos()
        print(f"[DEBUG] Click here: x = {clickX}, y = {clickY}")
      
      # Scroll up
      if (event.button == MOUSE_SCROLL_UP) :
        userScore.cursorStep(1)

      # Scroll down
      if (event.button == MOUSE_SCROLL_DOWN) :
        userScore.cursorStep(-1)



  # Clear the screen
  screen.fill(backgroundRGB)

  # Draw the keyboard on screen
  keyboardWidget.reset()
  keyboardWidget.drawKeys(screen)
  
  # Draw the piano roll on screen
  pianoRollWidget.drawPianoRoll(screen, pianoRollWidget.noteOnTimecodesMerged[currTime])

  # -------------------------------------------------
  # Show the current key pressed on the MIDI keyboard
  # -------------------------------------------------
  for pitch in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
    if (midiCurr[pitch] == 1) :
      #keyboardWidget.keyPress(screen, pitch, hand = UNDEFINED_HAND) 
      keyboardWidget.keyPress(screen, [utils.Note(pitch, hand = UNDEFINED_HAND)])

  # ------------------------------------------------------------------
  # Build the list of current expected notes to be played at that time
  # ------------------------------------------------------------------
  pianoRollWidget.getTeacherNotes(currTime, activeHands)
  pianoRollWidget.showTeacherNotes(screen, keyboard)

  # -----------------------------------------------------------------------
  # Decide whether to move forward in the score depending on the user input
  # -----------------------------------------------------------------------
  
  # Exact mode
  if (playComparisonMode == "exact") :
    if (pianoRoll.teacherMidi == midiCurr) :
      currTime += 1
      print(f"currTime = {currTime}")

  # Sustain mode
  # Sustained note are tolerated to proceed forward.
  # But they are not be treated as a pressed note: user needs to release and press it again.
  if (playComparisonMode == "allowSustain") :
    allowProgress = True
    for pitch in range(128) :
      
      # Key is pressed, but is actually an "old" key press (sustained note)
      if ((pianoRoll.teacherMidi[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 1)) :
        allowProgress = False

      if ((pianoRoll.teacherMidi[pitch] == 1) and (midiCurr[pitch] == 0) and (midiSustained[pitch] == 0)) :
        allowProgress = False

      if ((pianoRoll.teacherMidi[pitch] == 0) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 0)) :
        allowProgress = False
  
    if allowProgress :
      currTime += 1
      print(f"currTime = {currTime}")

      # Take snapshot
      for pitch in range(128) :
        if ((pianoRoll.teacherMidi[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 0)) :
          midiSustained[pitch] = 1

  # -----------------------
  # Note properties edition
  # -----------------------
  if clickMsg :
    
    # Click on a note on the keyboard
    if pianoRoll.isActiveNoteClicked(clickX, clickY, keyboard.litKeysPolygons) :
      clickedNote = pianoRoll.getActiveNoteClicked()
      fingerSelWidget.setNote(clickedNote)
      fingerSelWidget.visible = True
    
    # Click on the finger selector
    if fingerSelWidget.visible :
      ret = fingerSelWidget.updateWithClick(clickX, clickY)

      if (ret == fingerSelector.FINGERSEL_CHANGED) :
        pianoRoll.updateNoteProperties(fingerSelWidget.getNote())


    clickMsg = False

  # --------------------------------------------
  # Print some info relative to the current time
  # --------------------------------------------
  # Bookmark
  if (currTime in pianoRoll.bookmarks) :
    fu.renderText(screen, f"BOOKMARK #{pianoRoll.bookmarks.index(currTime)+1}", (10, 470), 2, (41, 67, 132))

  # Current active hands
  fu.renderText(screen, activeHands, (1288, 470), 2, (41, 67, 132))

  # Loop
  if loopEnable :
    fu.renderText(screen, "LOOP ACTIVE: 1/?", (300, 470), 2, (41, 67, 132))

  # Finger selection
  fingerSelWidget.show(screen)
  


  clock.tick(FPS)

  # Update the display
  pygame.display.flip()



# Quit Pygame
pygame.quit()


