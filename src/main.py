# -*- coding: utf-8 -*-
# =============================================================================
# Module name   : gangQin
# File name     : gangQin.py
# Purpose       : piano learning app
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Friday, 1 Sept 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# TODO list
# =============================================================================

# Mandatory:
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
# For graphics
import pygame
import keyboardUtils as ku
import midiUtils as mu
import fontUtils as fu
from gui import *

# For MIDI
import mido
import rtmidi

# For import/export
import os



# =============================================================================
# Constants pool
# =============================================================================
REV_MAJOR = 0
REV_MINOR = 7
REV_YEAR = 2023
REV_MONTH = "Oct"



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

# Open the MIDI interface selection GUI
(selectedDevice, inputFile) = mu.midiInterfaceGUI()

if (inputFile == "" or inputFile == "None") :
  raise SystemExit(0)

pygame.init()

# Define screen dimensions
screenWidth = 1320
screenHeight = 500
FPS = 60

# Create window
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption(f"gangQin App - v{REV_MAJOR}.{REV_MINOR} ({REV_MONTH}. {REV_YEAR})")

# Time management
clock = pygame.time.Clock()

# Create objects
keyboard = ku.Keyboard((10, 300))
pianoRoll = ku.PianoRoll(x = 10, yTop = 50, yBottom = 300-2)

# Set the background color
backgroundRGB = (180, 177, 226)

if (os.path.splitext(inputFile)[-1] == ".mid") :
  pianoRoll.importFromMIDIFile(inputFile)
else :
  pianoRoll.importFromPrFile(inputFile)

pygame.display.set_caption(f"gangQin App - v{REV_MAJOR}.{REV_MINOR} ({REV_MONTH}. {REV_YEAR}) - {inputFile}")

# =============================================================================
# Open MIDI keyboard interface
# =============================================================================
midiCurr = [0 for _ in range(128)]
midiSustained = [0 for _ in range(128)]

def midiCallback(message) :
  if (message.type == 'note_on') :
    #print(f"Note On: Note = {message.note}, Velocity = {message.velocity}")
    midiCurr[message.note] = 1
  elif (message.type == 'note_off') :
    #print(f"Note Off: Note = {message.note}, Velocity = {message.velocity}")
    midiCurr[message.note] = 0
    midiSustained[message.note] = 0 # this not cannot be considered as sustained anymore

if (mu.selectedDevice != "None") :
  midiPort = mido.open_input(mu.selectedDevice, callback = midiCallback)
else :
  print("[NOTE] No MIDI interface selected: running in navigation mode.")
  midiPort = None


# =============================================================================
# Main loop
# =============================================================================
running = True
currTime = 0

activeHands = "LR"

loopEnable = False
loopStartTimecode = -1
loopEndTimecode = -1

clickMsg = False

fingerSelGui = FingerSelector((500, 470))

while running:
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
        if (currTime > 0) :
          currTime -= 1
          print(f"Cursor: {currTime}")

      # ---------------------------------------
      # CTRL + Left arrow: fast rewind (1 step)
      # ---------------------------------------
      if (keys[pygame.K_LEFT] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL])) :
        if (currTime > 10) :
          currTime -= 10
          print(f"Cursor: {currTime}")

      # ----------------------------------
      # Right arrow: jump forward (1 step)
      # ----------------------------------
      if (keys[pygame.K_RIGHT] and not(keys[pygame.K_LCTRL])) :
        if ((currTime+1) < (len(pianoRoll.noteOnTimecodesMerged)-1)) :
          currTime += 1
          print(f"Cursor: {currTime}")

      # -----------------------------------------
      # CTRL + right arrow: fast forward (1 step)
      # -----------------------------------------
      if (keys[pygame.K_RIGHT] and (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL])) :
        if ((currTime+10) < (len(pianoRoll.noteOnTimecodesMerged)-1)) :
          currTime += 10
          print(f"Cursor: {currTime}")

      # ---------------------------------------------------
      # CTRL + HOME: jump to the beginning of the MIDI file
      # ---------------------------------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_HOME]) :
        currTime = 0
        print(f"Cursor: {currTime}")

      # -----------------------------------
      # Down: jump to the previous bookmark
      # -----------------------------------
      if (keys[pygame.K_DOWN]) :
        if (len(pianoRoll.bookmarks) > 0) :
          tmp = [x for x in pianoRoll.bookmarks if (x < currTime)]
          if (len(tmp) > 0) :
            currTime = tmp[-1]
          else :
            print(f"[NOTE] First bookmark reached")
        else :
          print(f"[NOTE] No bookmark!")

      # -----------------------------
      # Up: jump to the next bookmark
      # -----------------------------
      if (keys[pygame.K_UP]) :
        if (len(pianoRoll.bookmarks) > 0) :
          tmp = [x for x in pianoRoll.bookmarks if (x > currTime)]
          if (len(tmp) > 0) :
            currTime = tmp[0]
          else :
            print(f"[NOTE] Last bookmark reached")
        else :
          print(f"[NOTE] No bookmark!")

      # ----------------------------------------
      # "b": toggle a bookmark on this timestamp
      # ----------------------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_b]) :
        if currTime in pianoRoll.bookmarks :
          pianoRoll.bookmarks = [x for x in pianoRoll.bookmarks if (x != currTime)]
          print(f"[NOTE] Bookmark removed at time {currTime}")
        else :
          print(f"[NOTE] Bookmark added at time {currTime}")
          pianoRoll.bookmarks.append(currTime)
          pianoRoll.bookmarks.sort()

      # ------------------
      # "c": add a comment
      # ------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_c]) :
        print("[NOTE] Adding comments will be available in a future release.")

      # ---------------------------------
      # "l": enable/disable the left hand
      # ---------------------------------
      if (keys[pygame.K_l]) :
        if (activeHands[0] == "L") :
          activeHands = " " + activeHands[1]
        else :
          activeHands = "L" + activeHands[1]

      # -----------------------
      # "p": loop practice mode
      # -----------------------
      if (keys[pygame.K_p]) :
        loopEnable = not(loopEnable)
        print("[NOTE] Loop practice will be available in a future release.")

      fingerSelGui.visible = False

      # ----------------------------------
      # "r": enable/disable the right hand
      # ----------------------------------
      if (keys[pygame.K_r]) :
        if (activeHands[1] == "R") :
          activeHands = activeHands[0] + " "
        else :
          activeHands = activeHands[0] + "R"

      # ----------------
      # "s": export/save
      # ----------------
      if (keys[pygame.K_s]) :
        print("[NOTE] Exporting piano roll...")
        (rootDir, oldName) = os.path.split(inputFile)
        (midiFileName, _) = os.path.splitext(oldName)
        newName = rootDir + '/' + midiFileName + ".pr"
        pianoRoll.exportToPrFile(newName)
        pygame.display.set_caption(f"gangQin App - v{REV_MAJOR}.{REV_MINOR} ({REV_MONTH}. {REV_YEAR}) - {midiFileName}.pr")

      # -------------------------
      # Space key: rehearsal mode
      # -------------------------
      if (keys[pygame.K_SPACE]) :
        print("[NOTE] Rehearsal mode will be available in a future release.")

    # -------------------------------------------------------------------------
    # Mouse click event handling
    # -------------------------------------------------------------------------
    if (event.type == pygame.MOUSEBUTTONDOWN) :
      if (event.button == 1) :
        clickMsg = True
        clickX, clickY = pygame.mouse.get_pos()
        print(f"Click here: x = {clickX}, y = {clickY}")
      
      # Scroll up
      if (event.button == 4) :
        if ((currTime+1) < (len(pianoRoll.noteOnTimecodesMerged)-1)) :
          currTime += 1

      # Scroll down
      if (event.button == 5) :
        if (currTime > 0) :
          currTime -= 1



  # Clear the screen
  screen.fill(backgroundRGB)

  # Draw the keyboard on screen
  keyboard.reset()
  keyboard.drawKeys(screen)
  
  # Draw the piano roll on screen
  pianoRoll.drawPianoRoll(screen, pianoRoll.noteOnTimecodesMerged[currTime])

  # -------------------------------------------------
  # Show the current key pressed on the MIDI keyboard
  # -------------------------------------------------
  for pitch in range(ku.LOW_KEY_MIDI_CODE, ku.HIGH_KEY_MIDI_CODE+1) :
    if (midiCurr[pitch] == 1) :
      keyboard.keyPress(screen, pitch, hand = ku.UNDEFINED_HAND) 

      # Idealy:
      # noteObj = ku.Note(pitch, ku.UNDEF_HAND)
      # keyboard.keyPress(screen, [noteObj])


  # ------------------------------------------------------------------
  # Build the list of current expected notes to be played at that time
  # ------------------------------------------------------------------
  pianoRoll.getTeacherNotes(currTime, activeHands)
  pianoRoll.showTeacherNotes(screen, keyboard)


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
      fingerSelGui.setNote(clickedNote)
      fingerSelGui.visible = True
    
    # Click on the finger selector
    if fingerSelGui.visible :
      ret = fingerSelGui.updateWithClick(clickX, clickY)

      if (ret == FINGERSEL_CHANGED) :
        pianoRoll.updateNoteProperties(fingerSelGui.getNote())


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
  fingerSelGui.show(screen)
  


  clock.tick(FPS)

  # Update the display
  pygame.display.flip()



# Quit Pygame
pygame.quit()


