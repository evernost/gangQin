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
# - allow the user to transfer a note from one hand to the other
#   That involves inserting a note in <noteOnTimecodes>
# - loop timer: as soon as the first note of the loop is played, start a timer
#   and show a "fluidity" score
# - allow the user to add some comments. Comments should span one to several timecodes.
#   Comments can be guidelines, info on the way to play, ... any notes, really.
# - patch the keypress management in the code (combinations of CTRL+... are buggy)

# Nice to have:
# - funky animation everytime the right notes are played
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
from widgets import notify

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
fingerSelWidget = fingerSelector.FingerSelector((490, 470))

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

# Audio notifications widget
soundNotify = notify.Notify()



# =============================================================================
# Open MIDI keyboard interface
# =============================================================================
# - midiCurr     : state of all the notes on the MIDI keyboard
# - midiSustained: '1' for all notes that were correct in the score, but have been 
#                  sustained since then.
# - midiSuperfluous: 
# - midiAssociatedID: 
midiCurr         = [0 for _ in range(128)]
midiSustained    = [0 for _ in range(128)]
midiSuperfluous  = [0 for _ in range(128)]
midiAssociatedID = [-1 for _ in range(128)]

# Define the MIDI callback
def midiCallback(message) :
  if (message.type == 'note_on') :
    midiCurr[message.note] = 1

  elif (message.type == 'note_off') :
    midiCurr[message.note] = 0
    midiSustained[message.note] = 0 # this note cannot be considered as sustained anymore
    midiSuperfluous[message.note] = 0
    midiAssociatedID[message.note] = -1

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
ctrlKey  = False
altKey   = False

comboCount = 0
comboDrop  = False

setFingersatzMsg = -1

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
    
    if (event.type == pygame.KEYDOWN) :
      keys    = pygame.key.get_pressed()
      ctrlKey = event.mod & pygame.KMOD_CTRL
      altKey  = event.mod & pygame.KMOD_ALT

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

      # ------------------------------------------
      # ALT + Left arrow: highlight the note below
      # ------------------------------------------
      if (keys[pygame.K_LEFT] and altKey) :
        print("[TODO]")

      # -------------------------------------------
      # ALT + Right arrow: highlight the note above
      # -------------------------------------------
      if (keys[pygame.K_LEFT] and altKey) :
        print("[TODO]")

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
        t = [
          (keys[pygame.K_KP1], 1), 
          (keys[pygame.K_KP2], 2), 
          (keys[pygame.K_KP3], 3),
          (keys[pygame.K_KP4], 4),
          (keys[pygame.K_KP5], 5)
        ]
        for (boolCurr, index) in t :
          if boolCurr :
            
            # Implicit fingersatz edition
            # No note is highlighted: highlight it automatically based on current context.
            if (fingerSelWidget.getEditedNote() == None) :
              setFingersatzMsg = index
            
            # Explicit fingersatz edition
            # The note to edit was highlighted with a click beforehand.
            else :
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

      # --------------------------------
      # "d" + "-": shorten note duration
      # --------------------------------
      if (keys[pygame.K_d] and keys[pygame.K_KP_MINUS]) :
        print("[NOTE] Note duration shortening will be added in a future release.")

      # ----------------------------
      # "h": (Hear) toggle play mode
      # ----------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_h]) :
        print("[NOTE] Playing the song feature will be added in a future release.")

      # ---------------------------------------------
      # "k": toggle display of the notes in the scale
      # ---------------------------------------------
      if keys[pygame.K_k] :
        
        # A key has been defined starting from the current cursor
        currKey = userScore.getCurrentKey()
        
        if (currKey != None) :
          if (currKey.startTime == userScore.getCursor()) :
            if keys[pygame.K_KP_PLUS] :
              currKey.nextRoot()

            elif keys[pygame.K_KP_MINUS] :
              currKey.previousRoot()

        # Otherwise: start a new key here
        else :
          
          # TODO: do some stats and print the keys that are the most likely
          # userScore.guessKey()
          print("[DEBUG] New key added")
          userScore.keyList.append(utils.Scale("C", "major", startTime = userScore.getCursor()))

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
        #print(f"[DEBUG] Click here: x = {clickCoord[0]}, y = {clickCoord[1]}")
      
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
  
  currKey = userScore.getCurrentKey()
  keyboardWidget.setKey(currKey)
  if (currKey != None) :
    fu.renderText(screen, f"KEY: {currKey.root.upper()} {currKey.mode.upper()}", (200, 470), 2, UI_TEXT_COLOR)
  
  # Draw the piano roll on screen
  pianoRollWidget.drawPianoRoll(screen, userScore.getCurrentTimecode())

  # -------------------------------------------------
  # Show the notes expected to be played at that time
  # -------------------------------------------------
  # TODO: <getTeacherNotes> must cache the teacher notes instead of building them at each call.
  teacherNotes = userScore.getTeacherNotes()
  keyboardWidget.keyPress(screen, teacherNotes)

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

      # Case 1: the right note is pressed, but is actually an "old" key press (sustained note)
      if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 1)) :
        allowProgress = False

      # Case 2: a note is missing
      if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 0) and (midiSustained[pitch] == 0)) :
        allowProgress = False
      
      # Case 3: a wrong note is pressed 
      if ((userScore.teacherNotesMidi[pitch] == 0) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 0)) :
        allowProgress = False

    # Case 4: progress disabled because the "note finding" feature is still active
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
  # The rest is ignored, but flagged as 'superfluous'.
  # 'Superfluous' notes need to be released and pressed again to be accepted later on.
  if (playComparisonMode == "permissive") :
    allowProgress = True
    for pitch in GRAND_PIANO_MIDI_RANGE :

      # Case 1: a note is missing
      if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 0) and (midiSuperfluous[pitch] == 0)) :
        allowProgress = False

      # Case 2: the right note is played, but it was hit before expected and maintained since then
      if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSuperfluous[pitch] == 1)) :
        allowProgress = False

      # Case 3: the note was played correctly, but has not been released yet
      # Meanwhile, the score requires this note to be played again.
      if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 1)) :
        
        # Read the ID of the current note
        authorisedIDs = [x.id for x in userScore.teacherNotes if (x.pitch == pitch)]        
        
        # The IDs do not match: the note being played on the keyboard right now
        # is a previous valid note being sustained.
        # It cannot be used to trigger a new note of the same pitch.
        if not(midiAssociatedID[pitch] in authorisedIDs) :
          allowProgress = False
        
      # Other: a wrong note is pressed
      # Since it is permissive, it does not block the progress.
      # But it resets the combo counter and plays a notification.
      if ((userScore.teacherNotesMidi[pitch] == 0) and (midiCurr[pitch] == 1) and (midiSustained[pitch] == 0)) :
        userScore.comboCount = 0
        soundNotify.wrongNote()

    # Case 4: progress disabled because the "note finding" feature is still active
    # Waiting for all notes to be released.
    if (userScore.arbiterSuspendReq) :
      allDown = True
      for x in userScore.arbiterPitchListHold :
        if (midiCurr[x] == 1) :
          allDown = False

      if allDown :
        userScore.arbiterSuspendReq = False
      else :
        allowProgress = False



    # **********
    # Conclusion
    # **********
    if allowProgress :
      userScore.cursorNext()
      
      if (userScore.cursor == userScore.loopStart) :
        soundNotify.loopPassed()
      else :
        soundNotify.loopPassedReset()
      
      soundNotify.wrongNoteReset()
      
      # Update note status
      for pitch in GRAND_PIANO_MIDI_RANGE :
        
        # Is it a superfluous note?
        if ((userScore.teacherNotesMidi[pitch] == 0) and (midiCurr[pitch] == 1)) :
          midiSuperfluous[pitch] = 1

        # A valid note is now flagged as 'sustained'
        # The ID of the associated teacher note is registered (this keypress cannot validate another note 
        # of the same pitch)
        if ((userScore.teacherNotesMidi[pitch] == 1) and (midiCurr[pitch] == 1)) :
          midiSustained[pitch] = 1
          
          # Get the ID of the correct note
          # TODO: is it really always the first one that needs to be taken?
          q = [x for x in userScore.teacherNotes if (x.pitch == pitch)]
          midiAssociatedID[pitch] = q[0].id



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
  # Bookmark info
  if userScore.isBookmarkedTimecode() :
    fu.renderText(screen, f"BOOKMARK #{userScore.bookmarks.index(userScore.getCursor()) + 1}", (10, 470), 2, UI_TEXT_COLOR)

  # Active hand info
  fu.renderText(screen, userScore.activeHands, (1288, 470), 2, UI_TEXT_COLOR)

  # Loop info
  if userScore.loopEnable :
    fu.renderText(screen, f"LOOP: [{userScore.loopStart+1} ... {userScore.cursor+1} ... {userScore.loopEnd+1}]", (300, 20), 2, UI_TEXT_COLOR)
  else :
    if (userScore.loopStart >= 0) :
      fu.renderText(screen, f"LOOP: [{userScore.loopStart+1} ... {userScore.cursor+1} ... _]", (300, 20), 2, UI_TEXT_COLOR)

    if (userScore.loopEnd >= 0) :
      fu.renderText(screen, f"LOOP: [_  ... {userScore.cursor+1} ... {userScore.loopEnd+1}]", (300, 20), 2, UI_TEXT_COLOR)
      
  # Cursor info
  fu.renderText(screen, f"CURSOR: {userScore.cursor+1} / {userScore.cursorMax+1}", (12, 20), 2, UI_TEXT_COLOR)

  # Combo info
  fu.renderText(screen, f"COMBO: {userScore.comboCount} (MAX: {userScore.comboHighestSession} / ALLTIME: {userScore.comboHighestAllTime})", (800, 20), 2, UI_TEXT_COLOR)

  # Finger selection
  fingerSelWidget.show(screen)
  if (fingerSelWidget.getEditedNote() != None) :
    if (userScore.getCursor() != fingerSelWidget.editedCursor) :
      fingerSelWidget.resetEditedNote()
  


  # Request to edit the fingersatz with automatic note highlighting
  if (setFingersatzMsg > 0) :
    fingerSelWidget.setFingerAutoHighlight(setFingersatzMsg, userScore.teacherNotes, userScore.activeHands)
    setFingersatzMsg = -1


  clock.tick(FPS)

  # Update the display
  pygame.display.flip()



# Quit Pygame
pygame.quit()


