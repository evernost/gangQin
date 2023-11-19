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
# - during MIDI import: ask the user which tracks to use (there might be more than 2)
# - fingerSelGui should be visible and have focus 
# - allow the user to transfer a note from one hand to the other
#   That involves inserting a note in <noteOnTimecodes>
# - loop timer: as soon as the first note of the loop is played, start a timer
#   and show a "fluidity" score
# - allow the user to add some comments. Comments should span one to several timecodes.
#   Comments can be guidelines, info on the way to play, ... any notes, really.
# - patch the keypress management in the code (combinations of CTRL+... are buggy)

# Nice to have:
# - funky animation everytime the right notes are played
# - inform the user somehow that he is not playing the expected note
# - patch the obscure variable names in keyboardUtils
# - add a play button to hear some sections
# - <drawPianoRoll>: compute polygons once for all. Don't recompute them if time code hasn't changed
# - add autosave feature (save snapshot every 2 minutes)
# - show a "*" in the title bar as soon as there are unsaved changes in the pianoRoll object
# - pretty print the JSON (.pr file)
# - show arrows on the keyboard to give some guidance about where the "center of gravity"
#   of the hand is heading to
# - loop feature: "color memory game". Increase the size of the loop as the user
#   plays it without any mistakes and more quickly
# - auto-increase the step size if CTRL+left/right is hit multiple times in a row

# Later:
# - change the framework, use pyqt instead
# - complete the font library (fontUtils.py)
# - a dropdown list with all .mid/.pr files found instead of changing manually the variable
# - <midiCallback>: handle MIDI keyboards that send <noteON> messages with 0 velocity as a <noteOFF>

# Done:
# - bug fix: allow to play again the last note
# - highlight the activeNote ie the note whose finger is currently being associated
# - allow the user to practice hands separately
# - allow user to set the finger using numbers on the keypad
# - CTRL + mouse scroll has step 10 instead of 1
# - loop feature between 2 bookmarks
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
# - when editing the finger of an unedited note, FingerSelector shall be set 
#   on a default selector that matches with the hand of the note
# - issue: some notes from the teacher are shown in grey.
# - add "if __main__" in all libs



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

# Various utilities
import fontUtils as fu
import conf
import utils
import score

# For MIDI
import mido
import rtmidi

# For file/path utilities
import os



# =============================================================================
# Constants pool
# =============================================================================
# None.



# =============================================================================
# General settings
# =============================================================================
# Defines the criteria to allow moving forward in the score.
# - "exact": won't go further until the expected notes only are pressed, nothing else
# - "exactWithSustain": same as "exact", but tolerates the last valid notes to be sustained
# - "permissive": anything else played alongside the expected notes is ignored
playComparisonMode = "permissive"



# =============================================================================
# Main code
# =============================================================================

# Open the MIDI interface file selection GUI
(selectedDevice, selectedFile) = conf.showSetupGUI()

if ((selectedFile == "") or (selectedFile == "None")) :
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

# Load score and adjust the piano roll view
pianoRollWidget.loadPianoRoll(userScore.pianoRoll)
pianoRollWidget.viewSpan = userScore.avgNoteDuration*PIANOROLL_VIEW_SPAN

# Create window
pygame.display.set_caption(f"gangQin App - v{REV_MAJOR}.{REV_MINOR} ({REV_MONTH}. {REV_YEAR}) - <{os.path.basename(selectedFile)}>")

# Enable key repeats (250 ms delay before repeat, repeat every 50 ms)
pygame.key.set_repeat(250, 50)



# =============================================================================
# Open MIDI keyboard interface
# =============================================================================
midiCurr = [0 for _ in range(128)]
midiSustained = [0 for _ in range(128)]
midiSuperfluous = [0 for _ in range(128)]

# Define the MIDI callback
def midiCallback(message) :
  if (message.type == 'note_on') :
    midiCurr[message.note] = 1

  elif (message.type == 'note_off') :
    midiCurr[message.note] = 0
    midiSustained[message.note] = 0 # this note cannot be considered as sustained anymore
    midiSuperfluous[message.note] = 0


if (conf.selectedDevice != "None") :
  midiPort = mido.open_input(conf.selectedDevice, callback = midiCallback)
else :
  print("[WARNING] No MIDI interface selected: running in navigation mode.")
  midiPort = None



# =============================================================================
# Main loop
# =============================================================================
running = True

clickMsg = False
ctrlKey = False

comboCount = 0
comboDrop = False

while running :
  for event in pygame.event.get() :
    if (event.type == pygame.QUIT) :
      running = False

    # -------------------------------------------------------------------------
    # Keyboard event handling
    # -------------------------------------------------------------------------
    if (event.type == pygame.KEYUP) :
      keys = pygame.key.get_pressed()
      ctrlKey = event.mod & pygame.KMOD_CTRL
    
    if (event.type == pygame.KEYDOWN) :
      keys = pygame.key.get_pressed()
      ctrlKey = event.mod & pygame.KMOD_CTRL

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
      if (keys[pygame.K_LEFT] and not(ctrlKey)) :
        userScore.cursorStep(-1)

      # -----------------------------------------
      # CTRL + Left arrow: fast rewind (10 steps)
      # -----------------------------------------
      if (keys[pygame.K_LEFT] and ctrlKey) :
        userScore.cursorStep(-10)

      # ----------------------------------
      # Right arrow: jump forward (1 step)
      # ----------------------------------
      if (keys[pygame.K_RIGHT] and not(ctrlKey)) :
        userScore.cursorStep(1)

      # -------------------------------------------
      # CTRL + right arrow: fast forward (10 steps)
      # -------------------------------------------
      if (keys[pygame.K_RIGHT] and ctrlKey) :
        userScore.cursorStep(10)

      # ----------------------------------------------
      # HOME: jump to the beginning of the file
      # ----------------------------------------------
      if (keys[pygame.K_HOME]) :
        userScore.cursorBegin()

      # ---------------------------------------
      # END: jump to the end of the file
      # ---------------------------------------
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

      # ---------------------------
      # F9: set the start of a loop
      # ---------------------------
      if (keys[pygame.K_F9]) :
        userScore.setLoopStart()

      # --------------------------
      # F10: set the end of a loop
      # --------------------------
      if (keys[pygame.K_F10]) :
        userScore.setLoopEnd()

      # -------------------
      # F11: clear the loop
      # -------------------
      if (keys[pygame.K_F11]) :
        userScore.clearLoop()

      # -----------------------------------------------
      # Keypad 1 to 5: assign finger to a selected note
      # -----------------------------------------------
      if (keys[pygame.K_KP1] or keys[pygame.K_KP2] or keys[pygame.K_KP3] or keys[pygame.K_KP4] or keys[pygame.K_KP5]) :
        if fingerSelWidget.visible :
          t = [
            (keys[pygame.K_KP1], 1), 
            (keys[pygame.K_KP2], 2), 
            (keys[pygame.K_KP3], 3),
            (keys[pygame.K_KP4], 4),
            (keys[pygame.K_KP5], 5)
          ]
          for (boolCurr, index) in t :
            if boolCurr :
              fingerSelWidget.setFinger(index)
      
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

      # ------------------------------
      # "l": toggle left hand practice
      # ------------------------------
      if (keys[pygame.K_l]) :  
        userScore.toggleLeftHand()

      # -----------------------
      # "p": loop practice mode
      # -----------------------
      if (keys[pygame.K_p]) :
        userScore.toggleLoopMode()

      # -------------------------------
      # "r": toggle right hand practice
      # -------------------------------
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
        pygame.display.set_caption(f"gangQin App - v{REV_MAJOR}.{REV_MINOR} ({REV_MONTH}. {REV_YEAR}) - <{rootName}.pr>")

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
        clickCoord = pygame.mouse.get_pos()
        print(f"[DEBUG] Click here: x = {clickCoord[0]}, y = {clickCoord[1]}")
      
      # Scroll up
      if (event.button == MOUSE_SCROLL_UP) :
        
        # Find feature: go to the next cursor whose active notes match 
        # the current notes being pressed.
        # Note : use a copy of the MIDI notes list to prevent the 
        #        MIDI callback to mess with the function.
        if (max(midiCurr) == 1) :
          userScore.cursorJumpToNextMatch(midiCurr.copy())
        elif ctrlKey :
          userScore.cursorStep(10)
        else :
          userScore.cursorStep(1)

      # Scroll down
      if (event.button == MOUSE_SCROLL_DOWN) :
        
        # Find feature
        if (max(midiCurr) == 1) :
          userScore.cursorJumpToNextMatch(midiCurr.copy(), direction = -1)
        elif ctrlKey :
          userScore.cursorStep(-10)
        else :
          userScore.cursorStep(-1)



  # Clear the screen
  screen.fill(BACKGROUND_COLOR)

  # Draw the keyboard on screen
  keyboardWidget.reset()
  keyboardWidget.drawKeys(screen)
  
  # Draw the piano roll on screen
  pianoRollWidget.drawPianoRoll(screen, userScore.getCurrentTimecode())

  # -------------------------------------------------
  # Show the notes expected to be played at that time
  # -------------------------------------------------
  keyboardWidget.keyPress(screen, userScore.getTeacherNotes())

  # -------------------------------------------------
  # Show the current key pressed on the MIDI keyboard
  # -------------------------------------------------
  # TODO: list in comprehension might do a better job here
  midiNoteList = []
  for pitch in GRAND_PIANO_MIDI_RANGE :
    if (midiCurr[pitch] == 1) :
      newMidiNote = utils.Note(pitch)
      newMidiNote.fromKeyboardInput = True
      newMidiNote.hand = UNDEFINED_HAND
      newMidiNote.finger = 0
      midiNoteList.append(newMidiNote)
  
  keyboardWidget.keyPress(screen, midiNoteList)

  # -----------------------------------------------------------------------
  # Decide whether to move forward in the score depending on the user input
  # -----------------------------------------------------------------------
  
  # *** Exact mode ***
  if (playComparisonMode == "exact") :
    if (userScore.teacherNotesMidi == midiCurr) :
      userScore.cursorNext()



  # *** Sustain mode ***
  # Sustained note are tolerated to proceed forward.
  # But they are not be treated as a pressed note: user needs to release and press it again.
  if (playComparisonMode == "exactWithSustain") :
    allowProgress = True
    for pitch in GRAND_PIANO_MIDI_RANGE :

      # Key is pressed, but is actually an "old" key press (sustained note)
      if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 1)) :
        allowProgress = False

      if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 0) and (midiSustained[pitch] == 0)) :
        allowProgress = False

      if ((userScore.teacherNotesMidi[pitch] == 0) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 0)) :
        allowProgress = False

    # Disable progression 
    if (userScore.arbiterSuspendReq) :
      allDown = True
      for x in userScore.arbiterPitchListHold :
        if (midiCurr[x] == 1) :
          allDown = False

      if allDown :
        userScore.arbiterSuspendReq = False
      else :
        allowProgress = False

    if allowProgress :
      userScore.cursorNext()
      
      # Take snapshot
      for pitch in range(128) :
        if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 0)) :
          midiSustained[pitch] = 1



  # *** Permissive mode ***
  # Progress as long as the expected notes are pressed. 
  # The rest is ignored, but flagged as superfluous and will need
  # to be released and pressed again if requiered by the teacher.
  if (playComparisonMode == "permissive") :
    allowProgress = True
    for pitch in GRAND_PIANO_MIDI_RANGE :

      # A superfluous note is not considered as pressed
      if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSuperfluous[pitch] == 1)) :
        allowProgress = False

      # A requiered note is not pressed
      if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 0) and (midiSuperfluous[pitch] == 0)) :
        allowProgress = False


      if ((userScore.teacherNotesMidi[pitch] == 0) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 0)) :
        userScore.comboCount = 0

    # Disable progression if we came here by a key search
    # Progress is allowed as soon as the notes are released
    if (userScore.arbiterSuspendReq) :
      allDown = True
      for x in userScore.arbiterPitchListHold :
        if (midiCurr[x] == 1) :
          allDown = False

      if allDown :
        userScore.arbiterSuspendReq = False
      else :
        allowProgress = False

    if allowProgress :
      userScore.cursorNext()
      
      # Register all superfluous notes
      for pitch in GRAND_PIANO_MIDI_RANGE :
        
        # Is it a superfluous note?
        if ((userScore.teacherNotesMidi[pitch] == 0) and (midiCurr[pitch] == 1)) :
          midiSuperfluous[pitch] = 1

        if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 1)) :
          midiSustained[pitch] = 1


  # -----------------------
  # Note properties edition
  # -----------------------
  if clickMsg :
    
    # Click on a note on the keyboard
    clickedNote = keyboardWidget.isActiveNoteClicked(clickCoord)
    if clickedNote :
      print(f"[DEBUG] Clicked note: {clickedNote}")
      
      fingerSelWidget.setEditedNote(clickedNote, userScore.getCursor())
      fingerSelWidget.visible = True
    
    # Click on the finger selector
    if fingerSelWidget.visible :
      ret = fingerSelWidget.setFingerWithClick(clickCoord)

      if (ret == fingerSelector.FINGERSEL_HAND_CHANGE) :
        userScore.switchHand(fingerSelWidget.getEditedNote())

    clickMsg = False

  # --------------------------------------------
  # Print some info relative to the current time
  # --------------------------------------------
  # Bookmark
  if userScore.isBookmarkedTimecode() :
    # Note: "+1" because a bookmark number starting at 0 is not very user friendly
    fu.renderText(screen, f"BOOKMARK #{userScore.bookmarks.index(userScore.getCursor())+1}", (10, 470), 2, UI_TEXT_COLOR)

  # Current active hands
  fu.renderText(screen, userScore.activeHands, (1288, 470), 2, UI_TEXT_COLOR)

  # Loop
  if userScore.loopEnable :
    fu.renderText(screen, f"LOOP: {userScore.loopStart}/{userScore.getCursor()}/{userScore.loopEnd}", (250, 470), 2, UI_TEXT_COLOR)
  else :
    if (userScore.loopStart >= 0) :
      if (userScore.getCursor() >= userScore.loopStart) :
        fu.renderText(screen, f"LOOP: {userScore.loopStart}/{userScore.getCursor()}/{userScore.getCursor()}", (250, 470), 2, UI_TEXT_COLOR)
      else :
        fu.renderText(screen, f"LOOP: {userScore.loopStart}/{userScore.getCursor()}/_", (250, 470), 2, UI_TEXT_COLOR)

    if (userScore.loopEnd >= 0) :
      if (userScore.getCursor() <= userScore.loopEnd) :
        fu.renderText(screen, f"LOOP: {userScore.getCursor()}/{userScore.getCursor()}/{userScore.loopEnd}", (250, 470), 2, UI_TEXT_COLOR)
      else :
        fu.renderText(screen, f"LOOP: _/{userScore.getCursor()}/{userScore.loopEnd}", (250, 470), 2, UI_TEXT_COLOR)
      
  # Cursor display
  fu.renderText(screen, f"CURSOR: {userScore.cursor+1}", (12, 20), 2, UI_TEXT_COLOR)

  # Combo display
  fu.renderText(screen, f"COMBO: {userScore.comboCount}", (1200, 20), 2, UI_TEXT_COLOR)

  # Finger selection
  fingerSelWidget.show(screen)
  if (fingerSelWidget.getEditedNote() != None) :
    if (userScore.getCursor() != fingerSelWidget.editedCursor) :
      fingerSelWidget.resetEditedNote()
  

  clock.tick(FPS)

  # Update the display
  pygame.display.flip()



# Quit Pygame
pygame.quit()


