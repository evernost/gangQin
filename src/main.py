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
# External libs 
# =============================================================================
# Project specific constants
from commons import *

# For graphics
import pygame

# Widgets
from widgets import fingerSelector
from widgets import keyboard
from widgets import notify
from widgets import pianoRoll
from widgets import trackSelectGUI

# Various utilities
import arbiter
import conf
import metronome
import note
import score
import text
import utils

# For MIDI
import mido
import rtmidi

# For file/path utilities
import os



# =============================================================================
# Main code
# =============================================================================

# Open the MIDI interface file selection GUI
(selectedDevice, selectedFile) = conf.showSetupGUI()

if ((selectedFile == "") or (selectedFile == "None")) :
  raise SystemExit(0)


trackSelectGUI.show()



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

# Create the arbiter
pianoArbiter = arbiter.Arbiter("permissive")

# Create window
pygame.display.set_caption(f"gangQin - v{REV_MAJOR}.{REV_MINOR} [{REV_TYPE}] ({REV_MONTH} {REV_YEAR}) - <{os.path.basename(selectedFile)}>")

# Enable key repeats (250 ms delay before repeat, repeat every 50 ms)
pygame.key.set_repeat(250, 50)

# Audio notifications widget
soundNotify = notify.Notify()
soundNotify.enabled = False

# Metronome
metronomeObj = metronome.Metronome(120, 4, 4)
METRONOME_TASK = pygame.USEREVENT + 1
pygame.time.set_timer(METRONOME_TASK, metronomeObj.getInterval_ms())
pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 512)

# Autosave (todo)
AUTOSAVE_TASK = pygame.USEREVENT + 2




# =============================================================================
# MIDI messages callback
# =============================================================================
def midiCallback(midiMessage) :
  pianoArbiter.updateMidiState(midiMessage)



# =============================================================================
# Navigation mode
# =============================================================================
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
      shiftKey  = event.mod & pygame.KMOD_SHIFT
    
      # Send message to the metronome
      metronomeObj.keyRelease(event.key)


    elif (event.type == pygame.KEYDOWN) :
      keys    = pygame.key.get_pressed()
      ctrlKey = event.mod & pygame.KMOD_CTRL
      altKey  = event.mod & pygame.KMOD_ALT
      shiftKey  = event.mod & pygame.KMOD_SHIFT

      # Send message to the metronome
      metronomeObj.keyPress(keys)

      # -----------------
      # "q": exit the app
      # -----------------
      if keys[pygame.K_q] :
        if (midiPort != None) :
          midiPort.close()
        
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

      # ---------------------------------------------
      # Tab key: highlight the note above for editing
      # ---------------------------------------------
      if (keys[pygame.K_TAB] and not(shiftKey)) :
        fingerSelWidget.keyPress(keys)

      # -----------------------------------------------
      # Maj + tab: highlight the note before for editing
      # -----------------------------------------------
      if (keys[pygame.K_TAB] and shiftKey) :
        print("[TODO] Highlight previous note for fingersatz edition using Tab key")

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

      # -------------------------------
      # F2: increase lookAhead distance
      # -------------------------------
      if (keys[pygame.K_F2]) :
        if (userScore.lookAheadDistance == 5) :
          userScore.lookAheadDistance = 0
        else :
          userScore.lookAheadDistance += 1

        print(f"[DEBUG] Lookahead distance set to {userScore.lookAheadDistance}")

      # --------------------------------
      # F3: toggle "strict mode" in loop
      # --------------------------------
      if (keys[pygame.K_F3]) :
        if userScore.loopStrictMode :
          print(f"[DEBUG] Strict mode in loop is OFF.")
        else :
          print(f"[DEBUG] Strict mode in loop is ON.")
          
        userScore.loopStrictMode = not(userScore.loopStrictMode)

      # -----------------------------------------------------------
      # F4: metronome's tempo follows the instructions in the score
      # -----------------------------------------------------------
      if (keys[pygame.K_F4]) :
        if userScore.tempoReadFromScore :
          print("[INFO] Metronome: AUTO MODE. Tempo value is read from the score, modifications will be stored in the score.")
        else :
          print("[INFO] Metronome: FREE RUNNING MODE. Tempo value is free, modifications will not affect the tempo information in the score.")
        userScore.tempoReadFromScore = not(userScore.tempoReadFromScore)

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
        print("[INFO] Adding comments will be available in a future release.")

      # --------------------------------
      # "d" + "-": shorten note duration
      # --------------------------------
      if (keys[pygame.K_d] and keys[pygame.K_KP_MINUS]) :
        print("[INFO] Note duration shortening will be added in a future release.")

      # ----------------------------
      # "h": (Hear) toggle play mode
      # ----------------------------
      if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_h]) :
        print("[INFO] Playing the song feature will be added in a future release.")

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
        print("[INFO] Setting the key of the song will be added in a future release.")

      # ------------------------------
      # "l": toggle left hand practice
      # ------------------------------
      if (keys[pygame.K_l]) :  
        userScore.toggleLeftHandPractice()
      
      # -------------------------------
      # "r": toggle right hand practice
      # -------------------------------
      if (keys[pygame.K_r]) :
        userScore.toggleRightHandPractice()

      # ----------------
      # "s": export/save
      # ----------------
      if (keys[pygame.K_s]) :
        print("[INFO] Exporting piano roll...")
        (rootDir, rootNameExt) = os.path.split(selectedFile)
        (rootName, _) = os.path.splitext(rootNameExt)
        newName = rootDir + '/' + rootName + ".pr"
        userScore.exportToPrFile(newName)
        pygame.display.set_caption(f"gangQin - v{REV_MAJOR}.{REV_MINOR} [{REV_TYPE}] ({REV_MONTH} {REV_YEAR}) - <{rootName}.pr>")

      # -------------------------
      # Space key: rehearsal mode
      # -------------------------
      if (keys[pygame.K_SPACE]) :
        userScore.toggleRehearsalMode()

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
        
        # Find feature: go to the next cursor whose active notes match 
        # the current notes being pressed.
        # Note : use a copy of the MIDI notes list to prevent the 
        #        MIDI callback to mess with the function.
        if (max(pianoArbiter.midiCurr) == 1) :
          print("[INFO] Backward search requested...")
          (suspendReq, pitchListHold) = userScore.search(pianoArbiter.midiCurr.copy())
          if suspendReq :
            pianoArbiter.suspendReq(pitchListHold)

        elif ctrlKey :
          userScore.cursorStep(10)
        else :
          userScore.cursorStep(1)

      # Scroll down
      if (event.button == MOUSE_SCROLL_DOWN) :
        
        # Find feature
        if (max(pianoArbiter.midiCurr) == 1) :
          print("[INFO] Forward search requested...")
          (suspendReq, pitchListHold) = userScore.search(pianoArbiter.midiCurr.copy(), direction = -1)
          if suspendReq :
            pianoArbiter.suspendReq(pitchListHold)
        
        elif ctrlKey :
          userScore.cursorStep(-10)
        else :
          userScore.cursorStep(-1)


    # -------------------------------------------------------------------------
    # Metronome
    # -------------------------------------------------------------------------
    elif (event.type == METRONOME_TASK) :
      metronomeObj.playTick()



  # Clear the screen
  screen.fill(BACKGROUND_COLOR)

  # Draw the keyboard on screen
  keyboardWidget.reset()
  keyboardWidget.drawKeys(screen)
  
  currKey = userScore.getCurrentKey()
  keyboardWidget.setKey(currKey)
  if (currKey != None) :
    text.render(screen, f"KEY: {currKey.root.upper()} {currKey.mode.upper()}", (200, 470), 2, UI_TEXT_COLOR)
  
  # Draw the piano roll on screen
  pianoRollWidget.drawPianoRoll(screen, userScore.getCurrentTimecode())

  # -------------------------------------------------
  # Show the notes expected to be played at that time
  # -------------------------------------------------
  teacherNotes = userScore.getTeacherNotes()
  keyboardWidget.keyPress(screen, teacherNotes)

  # -------------------------------------------------
  # Show the current key pressed on the MIDI keyboard
  # -------------------------------------------------
  # TODO: list in comprehension might do a better job here
  midiNoteList = []
  for pitch in GRAND_PIANO_MIDI_RANGE :
    if (pianoArbiter.midiCurr[pitch] == 1) :
      newMidiNote = note.Note(pitch)
      newMidiNote.fromKeyboardInput = True
      newMidiNote.hand = UNDEFINED_HAND
      newMidiNote.finger = 0
      midiNoteList.append(newMidiNote)
  
  keyboardWidget.keyPress(screen, midiNoteList)

  # -----------------------
  # Show the upcoming notes
  # -----------------------
  upcomingNotes = userScore.getUpcomingNotes()
  keyboardWidget.keyPress(screen, upcomingNotes)

  # -----------------------------------------------------------------------
  # Decide whether to move forward in the score depending on the user input
  # -----------------------------------------------------------------------
  
  # Evaluate the status based on the score and the user input
  arbiterMsgQueue = pianoArbiter.eval(teacherNotes)

  # Read the arbiter messages
  for msg in arbiterMsgQueue :
    if (msg == arbiter.MSG_CURSOR_NEXT) :
      userScore.cursorNext()
      
      if (userScore.cursor == userScore.loopStart) :
        soundNotify.loopPassed()
      else :
        soundNotify.loopPassedReset()
      
      soundNotify.wrongNoteReset()

    if (msg == arbiter.MSG_RESET_COMBO) :  
      comboFall = (userScore.comboCount != 0)
    
      userScore.comboCount = 0
      soundNotify.wrongNote()
      
      # Strict mode practice: a wrong note resets the cursor to the beginning of the loop 
      # when <loopStrictMode> is active.
      # Reset occurs even if only the start point of the loop has been defined (unbounded looped practice)
      if (userScore.loopStrictMode) :
        c = userScore.getCursor()
        
        # Bound looped practice
        # The beginning and the end of the loop are defined.
        if userScore.loopEnable :
            
          # Cursor resets only if it was in the looping range.
          # Otherwise it is not affected: the user is practicing something outside the loop.
          # It wouldn't make sense to reset the cursor in this case.
          if ((c >= userScore.loopStart) and (c <= userScore.loopEnd)) :
            userScore.setCursor(userScore.loopStart)
            
            if comboFall :
              print(f"[INFO] Wrong note! loop reset :(   (combo: {c - userScore.loopStart})")

          else: 
            if comboFall :
              print("[INFO] Wrong note outside the looping range.")

        # Unbound looped practice
        # The end of the loop is not defined.
        # It is commonly used to practice a section and try to go as far as possible.
        elif (userScore.loopStart != -1) :
          if (c >= userScore.loopStart) :
            userScore.setCursor(userScore.loopStart)
            
            if comboFall :
              print(f"[INFO] Wrong note! loop reset :(   (combo: {c - userScore.loopStart})")
          
          else : 
            if comboFall :
              print("[INFO] Wrong note outside the looping range.")

  

  # ------------------------------------------------------
  # Show pointing hand when hovering over an editable note
  # ------------------------------------------------------
  (mouse_x, mouse_y) = pygame.mouse.get_pos()
  
  # Is the cursor somewhere above the keyboard?
  if ((10 <= mouse_x <= 1310) and (300 <= mouse_y <= 450)) :  
    detectedNote = keyboardWidget.isActiveNoteClicked(pygame.mouse.get_pos())
    if detectedNote :
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    else :
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
  else:
    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



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
        userScore.toggleNoteHand(fingerSelWidget.getEditedNote())

    clickMsg = False



  # ---------------------------------------------
  # Show some info relative to the current cursor
  # ---------------------------------------------
  # CURSOR
  text.render(screen, f"CURSOR: {userScore.cursor+1} / {userScore.scoreLength}", (12, 20), 2, UI_TEXT_COLOR)
  
  # BOOKMARK
  if userScore.isBookmarked() :
    text.render(screen, f"BOOKMARK #{userScore.bookmarks.index(userScore.getCursor()) + 1}", (10, 470), 2, UI_TEXT_COLOR)

  # ACTIVE HAND
  text.render(screen, userScore.activeHands, (1288, 470), 2, UI_TEXT_COLOR)

  # LOOP SETTINGS
  if userScore.loopEnable :
    text.render(screen, f"LOOP: [{userScore.loopStart+1} ... {userScore.cursor+1} ... {userScore.loopEnd+1}]", (400, 20), 2, UI_TEXT_COLOR)
  else :
    if (userScore.loopStart >= 0) :
      text.render(screen, f"LOOP: [{userScore.loopStart+1} ... {userScore.cursor+1} ... _]", (400, 20), 2, UI_TEXT_COLOR)

    if (userScore.loopEnd >= 0) :
      text.render(screen, f"LOOP: [_  ... {userScore.cursor+1} ... {userScore.loopEnd+1}]", (400, 20), 2, UI_TEXT_COLOR)
      
  # COMBO COUNT
  text.render(screen, f"COMBO: {userScore.comboCount} (MAX: {userScore.comboHighestSession} / ALLTIME: {userScore.comboHighestAllTime})", (1312, 20), 2, UI_TEXT_COLOR, justify = text.RIGHT_JUSTIFY)

  # FINGER SELECTION
  fingerSelWidget.show(screen)
  if (fingerSelWidget.getEditedNote() != None) :
    if (userScore.getCursor() != fingerSelWidget.editedCursor) :
      fingerSelWidget.resetEditedNote()
  
  # METRONOME
  if metronomeObj.enable :
    text.render(screen, f"BPM:{metronomeObj.bpm} - {metronomeObj.num}/{metronomeObj.denom} - {metronomeObj.counter}", (900, 470), 2, UI_TEXT_COLOR)



  # Request to edit the fingersatz with automatic note highlighting
  if (setFingersatzMsg > 0) :
    fingerSelWidget.setFingerAutoHighlight(setFingersatzMsg, userScore.teacherNotes, userScore.activeHands)
    setFingersatzMsg = -1



  # Some statistics
  userScore.updateStats()

  # Read metronome messages
  if (len(metronomeObj.msgQueue) > 0) :
    for msg in metronomeObj.msgQueue :
      if (msg == metronome.MSG_TEMPO_UPDATE) :
        pygame.time.set_timer(METRONOME_TASK, metronomeObj.getInterval_ms())
      
      elif (msg == metronome.MSG_TIMER_OFF) :
        pygame.time.set_timer(METRONOME_TASK, 0)

      elif (msg == metronome.MSG_TIMER_ON) :
        pygame.time.set_timer(METRONOME_TASK, metronomeObj.getInterval_ms())
        metronomeObj.counter = metronomeObj.num
        metronomeObj.playTick()
    
    metronomeObj.clearQueue()


  clock.tick(FPS)

  # Update the display
  pygame.display.flip()



# Quit Pygame
pygame.quit()


