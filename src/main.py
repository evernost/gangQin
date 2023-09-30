# -*- coding: utf-8 -*-
# =============================================================================
# Module name     : gangQin
# File name       : gangQin.py
# Purpose         : projet gangQin
# Author          : Quentin Biache (nitrogenium@hotmail.com)
# Creation date   : September 1st, 2023
# =============================================================================

# =============================================================================
# TODO
# =============================================================================

# Mandatory:
# - import/export the piano roll and all the metadata
# - allow the user to play the requested notes while sustaining the previous ones
# - allow the user to edit note properties (fingering, hand)
# - repeat feature between 2 bookmarks
# - allow the user to practice hands separately
# - patch the bad exit behavior upon pressing "q"
# - add "if __main__" in all libs
# - <drawPianoRoll>: compute polygons once for all. Don't recompute them if time code hasn't changed
# - during MIDI import: ask the user which tracks to use (there might be more than 2)
# - allow the user to add some comments that spans one to several timecodes
# - a dropdown list with all .mid/.pr files found instead of changing manually the variable

# Nice to have:
# - if a note is played on the keyboard, the note is correct but isn't enough to progress in 
#   the song (eg another note is missing) the colors overlap.
#   It would be great to handle this overlapping properly
# - patch the obscure variable names in keyboardUtils

# Later:
# - change the framework, use pyqt instead
# - complete the font library (fontUtils.py)

# Done:
# - add a fast forward option
# - draw the piano roll
# - handle properly the case of no MIDI interface selected (navigation mode)
# - add shortcut to jump to the first / last note



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
import json
import os



# =============================================================================
# Settings
# =============================================================================
# Defines the criteria to decide when to move onto the next notes
# - "exact": won't go further until the expected notes only are pressed, nothing else
# - "allowSustain": accepts that the last valid notes are sustained
playComparisonMode = "exact"



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
pygame.display.set_caption("gangQin App - v0.2 (Sept. 2023)")

# Time management
clock = pygame.time.Clock()

# Create objects
keyboard = ku.Keyboard((10, 300))
pianoRoll = ku.PianoRoll(x = 10, yTop = 50, yBottom = 300-2)

# Set the background color
backgroundRGB = (180, 177, 226)

# Read the MIDI file
midiFile = "./midi/Rachmaninoff_Piano_Concerto_No2_Op18.mid"
#midiFile = "./midi/Sergei_Rachmaninoff_-_Moments_Musicaux_Op._16_No._4_in_E_Minor.mid"
#midiFile = "./midi/12_Etudes_Op.8__Alexander_Scriabin__tude_in_A_Major_-_Op._8_No._6.mid"

pianoRoll.loadPianoRollArray(midiFile)



# =============================================================================
# Open MIDI keyboard interface
# =============================================================================
midiCurr = [0 for _ in range(128)]

def midiCallback(message) :
  if (message.type == 'note_on') :
    print(f"Note On: Note={message.note}, Velocity={message.velocity}")
    midiCurr[message.note] = 1
  elif (message.type == 'note_off') :
    print(f"Note Off: Note={message.note}, Velocity={message.velocity}")
    midiCurr[message.note] = 0

if mu.selectedDevice :
  midiPort = mido.open_input(mu.selectedDevice, callback = midiCallback)
else :
  print("[NOTE] No MIDI interface selected: running in navigation mode.")


# =============================================================================
# Main loop
# =============================================================================
running = True
currTime = 0

bookmarks = []
activeHands = "LR"

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
        midiPort.close()
        pygame.quit()

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
        if currTime in bookmarks :
          bookmarks = [x for x in bookmarks if (x != currTime)]
          print(f"[NOTE] Bookmark removed at time {currTime}")
        else :
          print(f"[NOTE] Bookmark added at time {currTime}")
          bookmarks.append(currTime)
          bookmarks.sort()

      # -----------------------------------
      # Down: jump to the previous bookmark
      # -----------------------------------
      if (keys[pygame.K_DOWN]) :
        if (len(bookmarks) > 0) :
          tmp = [x for x in bookmarks if (x < currTime)]
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
        if (len(bookmarks) > 0) :
          tmp = [x for x in bookmarks if (x > currTime)]
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
        print("[NOTE] Exporting piano roll")
        (midiDir, oldName) = os.path.split(midiFile)
        (midiFileName, _) = os.path.splitext(oldName)
        newName = midiDir + '/' + midiFileName + ".pr"
        print(newName)
        pianoRoll.exportPianoRoll(newName)



  # Clear the screen
  screen.fill(backgroundRGB)

  # Draw the keyboard on screen
  keyboard.reset()
  keyboard.drawKeys(screen)
  
  # Draw the piano roll on screen
  pianoRoll.drawKeyLines(screen)
  pianoRoll.drawPianoRoll(screen, pianoRoll.noteOnTimecodesMerged[currTime])

  # Show the current key pressed on the MIDI keyboard
  for pitch in range(21, 108+1) :
    if (midiCurr[pitch] == 1) :
      keyboard.keyPress(screen, pitch, hand = "neutral") 

  # Build the list of current expected notes to be played at that time
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

  # Decide whether to move forward in the score depending on the user input
  if (playComparisonMode.lower() == "exact") :
    if (midiTeacher == midiCurr) :
      currTime += 1
      print(f"currTime = {currTime}")

  if (playComparisonMode.lower() == "allowsustain") :
    if (midiTeacher == midiCurr) :
      currTime += 1
      print(f"currTime = {currTime}")

  if (currTime in bookmarks) :
    fu.render(screen, f"BOOKMARK #{bookmarks.index(currTime)+1}", (10, 470), 2, (41, 67, 241))


  # Show the current active hands
  fu.render(screen, activeHands, (1288, 470), 2, (10, 10, 10))


  clock.tick(FPS)

  # Update the display
  pygame.display.flip()

# Quit Pygame
pygame.quit()


