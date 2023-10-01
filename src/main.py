# -*- coding: utf-8 -*-
# =============================================================================
# Module name     : gangQin
# File name       : gangQin.py
# Purpose         : piano learning app
# Author          : Quentin Biache (nitrogenium@hotmail.com)
# Creation date   : September 1st, 2023
# =============================================================================

# =============================================================================
# TODO
# =============================================================================

# Mandatory:
# - import/export the piano roll and all the metadata
# - allow the user to edit note properties (fingering, hand)
# - allow the user to add some comments that spans one to several timecodes
# - loop feature between 2 bookmarks
# - allow the user to practice hands separately
# - add "if __main__" in all libs
# - <drawPianoRoll>: compute polygons once for all. Don't recompute them if time code hasn't changed
# - during MIDI import: ask the user which tracks to use (there might be more than 2)
# - a dropdown list with all .mid/.pr files found instead of changing manually the variable
# - patch the keypress management in the code (combinations of CTRL+... are buggy)
# - issue: some notes from the teacher are show in grey.

# Nice to have:
# - patch the obscure variable names in keyboardUtils
# - add a play button to hear some sections

# Later:
# - change the framework, use pyqt instead
# - complete the font library (fontUtils.py)

# Done:
# - add a fast forward option
# - draw the piano roll
# - handle properly the case of no MIDI interface selected (navigation mode)
# - add shortcut to jump to the first / last note
# - if a note is played on the keyboard, the note is correct but isn't enough to progress in 
#   the song (eg another note is missing) the colors overlap.
# - allow the user to play the requested notes while sustaining the previous ones
# - patch the bad exit behavior upon pressing "q"



# =============================================================================
# Imports 
# =============================================================================
# For graphics
import pygame
import keyboardUtils as ku
import midiUtils as mu
import fontUtils as fu

# For MIDI
import mido
import rtmidi

# For import/export
import os

# For point in polygon test
from shapely.geometry import Point, Polygon


# =============================================================================
# Constants pool
# =============================================================================
REV_MAJOR = 0
REV_MINOR = 3
REV_YEAR = 2023
REV_MONTH = "Oct"

FSM_NORMAL = 0
FSM_LOOP_INPUT = 1


# =============================================================================
# Settings
# =============================================================================
# Defines the criteria to decide when to move onto the next notes
# - "exact": won't go further until the expected notes only are pressed, nothing else
# - "allowSustain": accepts that the last valid notes are sustained
playComparisonMode = "allowSustain"



# =============================================================================
# Main code
# =============================================================================

# Open the MIDI interface selection GUI
selectedDevice = mu.midiInterfaceGUI()
print(selectedDevice)

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

pianoRoll.importPianoRoll("./midi/Prelude_in_D_Minor_Opus_23_No._3__Sergei_Rachmaninoff.pr")

# Read the MIDI file
#midiFile = "./midi/Rachmaninoff_Piano_Concerto_No2_Op18.mid"
#midiFile = "./midi/Sergei_Rachmaninoff_-_Moments_Musicaux_Op._16_No._4_in_E_Minor.mid"
#midiFile = "./midi/12_Etudes_Op.8__Alexander_Scriabin__tude_in_A_Major_-_Op._8_No._6.mid"
midiFile = "./midi/Prelude_in_D_Minor_Opus_23_No._3__Sergei_Rachmaninoff.mid"

#pianoRoll.loadPianoRollArray(midiFile)




# =============================================================================
# Open MIDI keyboard interface
# =============================================================================
midiCurr = [0 for _ in range(128)]
midiSustained = [0 for _ in range(128)]

def midiCallback(message) :
  if (message.type == 'note_on') :
    print(f"Note On: Note = {message.note}, Velocity = {message.velocity}")
    midiCurr[message.note] = 1
  elif (message.type == 'note_off') :
    print(f"Note Off: Note = {message.note}, Velocity = {message.velocity}")
    midiCurr[message.note] = 0
    midiSustained[message.note] = 0 # this not cannot be considered as sustained anymore

if mu.selectedDevice :
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

fsmState = FSM_NORMAL

while running:
  for event in pygame.event.get() :
    if (event.type == pygame.QUIT) :
      running = False

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
      if (keys[pygame.K_LEFT] and keys[pygame.K_LCTRL]) :
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
      if (keys[pygame.K_RIGHT] and keys[pygame.K_LCTRL]) :
        if ((currTime+10) < (len(pianoRoll.noteOnTimecodesMerged)-1)) :
          currTime += 10
          print(f"Cursor: {currTime}")

      # TODO: auto-increase the step size if CTRL+left/right is hit multiple times in a row 

      # ---------------------------------------------------
      # CTRL + HOME: jump to the beginning of the MIDI file
      # ---------------------------------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_HOME]) :
        currTime = 0
        print(f"Cursor: {currTime}")

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

      # -------------------------------------
      # "f": define finger on a selected note
      # -------------------------------------
      if (keys[pygame.K_f]) :
        print("[NOTE] TODO")

      # -----------------------------------
      # "h": define hand on a selected note
      # -----------------------------------
      if (keys[pygame.K_h]) :
        print("[NOTE] TODO")

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

      # ---------------------------------
      # "l": enable/disable the left hand
      # ---------------------------------
      if (keys[pygame.K_l]) :
        if (activeHands[0] == "L") :
          activeHands = " " + activeHands[1]
        else :
          activeHands = "L" + activeHands[1]

      # ----------------------------------
      # "r": enable/disable the right hand
      # ----------------------------------
      if (keys[pygame.K_r]) :
        if (activeHands[1] == "R") :
          activeHands = activeHands[0] + " "
        else :
          activeHands = activeHands[0] + "R"

      # ----------------------------------
      # "s": export/save
      # ----------------------------------
      if (keys[pygame.K_s]) :
        print("[NOTE] Exporting piano roll...")
        (midiDir, oldName) = os.path.split(midiFile)
        (midiFileName, _) = os.path.splitext(oldName)
        newName = midiDir + '/' + midiFileName + ".pr"
        print(newName)
        pianoRoll.exportPianoRoll(newName)

      # ----------------------------------
      # "p": loop
      # ----------------------------------
      if (keys[pygame.K_p]) :
        loopEnable = not(loopEnable)
        print("[NOTE] TODO")

    # --------------------
    # Mouse click handling
    # --------------------
    if (event.type == pygame.MOUSEBUTTONDOWN) :
      click_x, click_y = pygame.mouse.get_pos()


  # Clear the screen
  screen.fill(backgroundRGB)

  # Draw the keyboard on screen
  keyboard.reset()
  keyboard.drawKeys(screen)
  
  # Draw the piano roll on screen
  pianoRoll.drawKeyLines(screen)
  pianoRoll.drawPianoRoll(screen, pianoRoll.noteOnTimecodesMerged[currTime])

  # -------------------------------------------------
  # Show the current key pressed on the MIDI keyboard
  # -------------------------------------------------
  for pitch in range(21, 108+1) :
    if (midiCurr[pitch] == 1) :
      keyboard.keyPress(screen, pitch, hand = "neutral") 



  # ------------------------------------------------------------------
  # Build the list of current expected notes to be played at that time
  # ------------------------------------------------------------------
  # TODO: make it a function
  midiTeacher = [0 for _ in range(128)]
  for pitch in range(21, 108+1) :
    if (activeHands == "LR") :
      for track in range(pianoRoll.nTracks) :
        for evt in pianoRoll.noteArray[track][pitch] :
          if (evt.startTime == pianoRoll.noteOnTimecodesMerged[currTime]) :
            midiTeacher[pitch] = 1
            if (track == 0) :
              keyboard.keyPress(screen, pitch, hand = "left", finger = 1)
            
            if (track == 1) :
              keyboard.keyPress(screen, pitch, hand = "right", finger = 2) 

    if (activeHands == " R") :
      track = 1
      for evt in pianoRoll.noteArray[track][pitch] :
          if (evt.startTime == pianoRoll.noteOnTimecodes[track][currTime]) :
            midiTeacher[pitch] = 1
            keyboard.keyPress(screen, pitch, hand = "right", finger = 2) 

    if (activeHands == "L ") :
      track = 0
      for evt in pianoRoll.noteArray[track][pitch] :
          if (evt.startTime == pianoRoll.noteOnTimecodes[track][currTime]) :
            midiTeacher[pitch] = 1
            keyboard.keyPress(screen, pitch, hand = "left", finger = 1)



  # -----------------------------------------------------------------------
  # Decide whether to move forward in the score depending on the user input
  # -----------------------------------------------------------------------
  if (playComparisonMode == "exact") :
    if (midiTeacher == midiCurr) :
      currTime += 1
      print(f"currTime = {currTime}")

  # A sustained note is not taken into account to decide whether to move
  # forward or not. It will not block progress if sustained and not expected.
  # But it will not be treated as a pressed note: user needs to release and press it again.
  if (playComparisonMode == "allowSustain") :
    allowProgress = True
    for pitch in range(128) :
      
      # Key pressed, but is actually an "old" key press (note is sustained)
      if ((midiTeacher[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 1)) :
        allowProgress = False

      if ((midiTeacher[pitch] == 1) and (midiCurr[pitch] == 0) and (midiSustained[pitch] == 0)) :
        allowProgress = False

      if ((midiTeacher[pitch] == 0) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 0)) :
        allowProgress = False
  
    if allowProgress :
      currTime += 1
      print(f"currTime = {currTime}")

      # Take snapshot
      for pitch in range(128) :
        if ((midiTeacher[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 0)) :
          midiSustained[pitch] = 1


  # --------------------------------------------
  # Print some info relative to the current time
  # --------------------------------------------
  # Bookmark
  if (currTime in pianoRoll.bookmarks) :
    fu.render(screen, f"BOOKMARK #{pianoRoll.bookmarks.index(currTime)+1}", (10, 470), 2, (41, 67, 241))

  # Current active hands
  fu.render(screen, activeHands, (1288, 470), 2, (10, 10, 10))

  # Loop
  
  if loopEnable :
    fu.render(screen, "LOOP ACTIVE: 1/?", (500, 470), 2, (10, 10, 10))


  clock.tick(FPS)

  # Update the display
  pygame.display.flip()



# Quit Pygame
pygame.quit()


