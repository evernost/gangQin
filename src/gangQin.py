# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : GangQin Player
# File name     : gangQin.py
# File type     : Python script (Python 3)
# Purpose       : GangQin Player - class definition
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Saturday, 5 April 2025
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs 
# =============================================================================
# Project specific constants
from commons import *

# Graphic interface
import pygame

# Widgets
import src.widgets.fileSelectionGUI as fileSelectionGUI
import src.widgets.fingerSelector as fingerSelector
import src.widgets.keyboard as keyboard
import src.widgets.notify as notify
import src.widgets.pianoRoll as pianoRoll
import src.widgets.trackSelectionGUI as trackSelectionGUI
import src.widgets.staffScope as staffScope
import src.widgets.sequencer as sequencer

# Utilities
import arbiter
import metronome
import note
import score
import stats
import text

# MIDI
import mido

# Standard libs
import os



# =============================================================================
# CONSTANTS
# =============================================================================




# =============================================================================
# CLASS DEFINITION
# =============================================================================
class GangQin :

  """
  TODO
  """
  
  # ---------------------------------------------------------------------------
  # METHOD: GangQin.__init__
  # ---------------------------------------------------------------------------
  def __init__(self) :
    
    # Initialise attributes
    self.songFile = ""    # Example: "./songs/my_song.mid"
    self.songDir  = ""    # Example: './songs'
    self.songName = ""    # Example: 'my_song'
    self.songType = ""    # Example: "mid"

    # Initialise pygame
    pygame.init()
    self.screen = pygame.display.set_mode((GUI_SCREEN_WIDTH, GUI_SCREEN_HEIGHT))
    self.screenWidth = self.screen.get_size()[0]
    self.screenHeight = self.screen.get_size()[1]
    self.clock = pygame.time.Clock()
    pygame.key.set_repeat(250, 50)    # Enable key repeats (250 ms delay before repeat, repeat every 50 ms)
    self._backgroundInit()
    self.running = False

    # Limit the keyevents to avoid unncessary processing
    pygame.event.set_allowed([
      pygame.KEYDOWN,
      pygame.KEYUP,
      pygame.MOUSEBUTTONDOWN,
      pygame.QUIT
    ])

    # Initialise the widgets
    self.widgets = {
      WIDGET_ID_SCORE : score.Score(self),
      WIDGET_ID_KEYBOARD: keyboard.Keyboard(self, loc = (10, 300)),
      #WIDGET_ID_PIANOROLL: pianoRoll.PianoRoll(self, loc = (10, 50)),
      WIDGET_ID_STAFFSCOPE: staffScope.StaffScope(self),
      #fingerSelector.FingerSelector(self),
      #metronome.Metronome(self),
      #arbiter.Arbiter(self),
      #stats.Stats(self),
      #notify.Notify(self)
      WIDGET_ID_SEQUENCER: sequencer.Sequencer(self)
    }
    


  # ---------------------------------------------------------------------------
  # METHOD: GangQin.loadSong()
  # ---------------------------------------------------------------------------
  def loadSong(self) :
    """
    Initialises the gangQin application with the song to work on (.mid or .gq file)
    """

    # Call the file selection GUI
    fsGUI = fileSelectionGUI.new()
    (selectedDevice, songFile) = fsGUI.run()

    if ((songFile == "") or (songFile == "None")) :
      print("[INFO] No file selected, exiting...")
      exit()
    else :
      (rootDir, rootNameExt) = os.path.split(songFile)
      (rootName, _) = os.path.splitext(rootNameExt)
      self.songFile = songFile
      self.songDir  = rootDir
      self.songName = rootName

    # If a MIDI file is selected, show the track selection GUI
    if songFile.endswith(".mid") :
      self.songType = "mid"
      trackSel = trackSelectionGUI.new()
      trackSel.load(songFile)
      midiTracks = trackSel.show()
      self.widgets[WIDGET_ID_SCORE].loadMIDIFile(songFile, midiTracks)
    else :
      self.songType = "gq"
      self.widgets[WIDGET_ID_SCORE].loadGQFile(songFile)
      self.widgets[WIDGET_ID_STAFFSCOPE].load(songFile)

    # Initialise the MIDI keyboard interface
    if (selectedDevice != "None") :
      try :
        midiPort = mido.open_input(selectedDevice, callback = self._midiCallback)
      except Exception as err :
        print("[WARNING] Failed to open the MIDI device (it is used by another software?): running in navigation mode.")
        midiPort = None  
    else :
      print("[NOTE] No MIDI interface selected: running in navigation mode.")
      midiPort = None

    # Update the app properties
    pygame.display.set_caption(f"gangQin player - v{REV_MAJOR}.{REV_MINOR} [{REV_TYPE}] ({REV_MONTH} {REV_YEAR}) - Song: {self.songName}")



  # ---------------------------------------------------------------------------
  # METHOD: GangQin.run()
  # ---------------------------------------------------------------------------
  def run(self) :
    
    # Start app
    self.appRunning = True

    # Main execution loop.
    # Loop exits when the application is done
    while self.appRunning :
      
      # Fill background screen
      self.screen.blit(self.background, (0, 0))
    
      for event in pygame.event.get() :
        if (event.type == pygame.QUIT) :
          self.appRunning = False

        # Pass keyboard/click messages to the widgets
        for widget in self.widgets.values() :
          widget.uiEvent(event)

      # Render widgets
      for widget in self.widgets.values() :
        widget.render()

      


      self.clock.tick(GUI_FPS)

      # Update the display
      pygame.display.flip()

  # Quit Pygame
  pygame.quit()






  # ---------------------------------------------------------------------------
  # METHOD: GangQin._midiCallback()
  # ---------------------------------------------------------------------------
  def _midiCallback(self, midiMessage) :
    """
    This function is called on every MIDI event coming from the external MIDI
    keyboard.
    """

    self.widgets[WIDGET_ID_ARBITER].updateMidiState(midiMessage)
    self.widgets[WIDGET_ID_STATS].userActivity()






  # ---------------------------------------------------------------------------
  # METHOD: GangQin._backgroundInit()                                 [PRIVATE]
  # ---------------------------------------------------------------------------
  def _backgroundInit(self) :
    """
    Initialises the 'background' attribute from a pattern description.
    Builds the tiling.
    """

    # TODO: move to 'commons.py'
    C0 = GUI_BACKGROUND_COLOR
    C1 = (58, 97, 90)
    patternData = [
      [C0, C0, C1, C0, C0, C0, C0, C0],
      [C0, C0, C1, C0, C0, C0, C0, C0],
      [C1, C1, C1, C0, C0, C0, C0, C0],
      [C0, C0, C0, C0, C0, C0, C0, C0],
      [C0, C0, C0, C0, C0, C0, C0, C0],
      [C0, C0, C0, C0, C0, C1, C1, C1],
      [C0, C0, C0, C0, C0, C1, C0, C0],
      [C0, C0, C0, C0, C0, C1, C0, C0]
    ]

    #patternData = self._backgroundInitFromImage()

    w, h = len(patternData[0]), len(patternData)
    patternSurface = pygame.Surface((w, h))
    for y in range(h):
      for x in range(w):
        patternSurface.set_at((x, y), patternData[y][x])
    
    self.background = pygame.Surface((GUI_SCREEN_WIDTH, GUI_SCREEN_HEIGHT))
    for x in range(0, GUI_SCREEN_WIDTH, patternSurface.get_width()):
      for y in range(0, GUI_SCREEN_HEIGHT, patternSurface.get_height()):
        self.background.blit(patternSurface, (x, y))



  # ---------------------------------------------------------------------------
  # METHOD: GangQin._backgroundInitFromImage()                        [PRIVATE]
  # ---------------------------------------------------------------------------
  def _backgroundInitFromImage(self) :
    """
    Init from a pattern image.
    """
    
    C0 = GUI_BACKGROUND_COLOR
    C1 = (58, 97, 90)

    # Define color LUT
    LUT = {
      (0, 0, 0)       : C0,
      (195, 195, 195) : C1,
      (232, 232, 232) : (24, 89, 80),
      (255, 255, 255) : (36, 135, 121)
    }

    image = pygame.image.load("./resources/background/cubes.bmp")
    image = image.convert()
    (width, height) = image.get_size()

    # Convert to a 2D-list
    patternData = [
      [image.get_at((x, y))[:3] for x in range(width)]  # [:3] to get RGB only, no alpha
      for y in range(height)
    ]

    # Apply palette
    patternData = [
      [LUT.get(color, color) for color in row]
      for row in patternData
    ]

    return patternData
  


  # ---------------------------------------------------------------------------
  # METHOD: GangQin._onExit()                                         [PRIVATE]
  # ---------------------------------------------------------------------------
  def _onExit(self) :
    """
    Function is called upon exiting.
    Do all the things here that you need to do before leaving 
    (save, look for unsaved changes, etc.)

    This function is called automatically. It is not meant to be called 
    externally.
    """

    pass



  # ---------------------------------------------------------------------------
  # METHOD: GangQin._onSave()                                         [PRIVATE]
  # ---------------------------------------------------------------------------
  def _onSave(self) :
    """
    Function is called when a 'save' event occured (either from user or 
    automatically)

    This function is called automatically. It is not meant to be called 
    externally.
    """

    pass






if False :

  # Load the file to a Score object
  userScore = score.Score(songFile)

  # Widget: grand piano
  keyboardWidget = keyboard.Keyboard(loc = (10, 300))

  # Widget: piano roll
  pianoRollWidget = pianoRoll.PianoRoll(x = 10, yTop = 50, yBottom = 300-2)
  pianoRollWidget.loadPianoRoll(userScore.pianoRoll)
  pianoRollWidget.viewSpan = userScore.avgNoteDuration*PIANOROLL_VIEW_SPAN

  # Widget: staffscope
  staffScopeVisible = STAFFSCOPE_DEFAULT_VISIBILITY
  #staffScopeWidget = 
  staffScopeWidget.setScreen(screen, GUI_SCREEN_WIDTH, GUI_SCREEN_HEIGHT)
  staffScopeWidget.loadDatabase(songFile)

  # Widget: finger editor
  fingerSelWidget = fingerSelector.FingerSelector((490, 470))

  # Widget: audio notifications
  soundNotify = notify.Notify()
  soundNotify.enabled = False

  # Widget: metronome
  metronomeObj = metronome.Metronome(120, 4, 4)
  METRONOME_TASK = pygame.USEREVENT + 1
  pygame.time.set_timer(METRONOME_TASK, metronomeObj.getInterval_ms())
  pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 512)

  # Widget: statistics
  statsObj = stats.Stats()
  statsObj.load(songFile)
  statsObj.showIntroSummary()

  # Widget: arbiter
  pianoArbiter = arbiter.Arbiter("permissive")





  # =============================================================================
  # Main loop
  # =============================================================================
  running = True
  

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
      
        # Send message to the widgets
        metronomeObj.keyRelease(event.key)
        fingerSelWidget.keyRelease(keys)
        pianoRollWidget.keyRelease(keys)

      elif (event.type == pygame.KEYDOWN) :
        keys    = pygame.key.get_pressed()
        ctrlKey = event.mod & pygame.KMOD_CTRL
        altKey  = event.mod & pygame.KMOD_ALT
        shiftKey  = event.mod & pygame.KMOD_SHIFT

        # Send message to the widgets
        metronomeObj.keyPress(keys)
        fingerSelWidget.keyPress(keys)
        pianoRollWidget.keyPress(keys)








        # -------------------------------
        # F2: increase lookAhead distance
        # -------------------------------
        if (keys[pygame.K_F2]) :
          if (userScore.lookAheadDistance == 5) :
            userScore.lookAheadDistance = 0
          else :
            userScore.lookAheadDistance += 1

          print(f"[DEBUG] Lookahead distance set to {userScore.lookAheadDistance}/5")

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
        
        # --------------------------------------
        # "a": start special mode of the arbiter
        # --------------------------------------
        if (not(keys[pygame.K_LCTRL]) and keys[pygame.K_a]) :
          userScore.setWeakArbitration()





        
        # ------------------------------
        # "e": report error in the score
        # ------------------------------
        if keys[pygame.K_e] :
          print("[INFO] Error reporting will be added in a future release.")
          #errSel = errorReportGUI.show()
          # Pass the info to staffScope:
          # ...



        
        # -----------------
        # "q": exit the app
        # -----------------
        if keys[pygame.K_q] :
          if (midiPort != None) :
            midiPort.close()
          
          statsObj.userActivity()
          statsObj.save()
          userScore.exportToPrFile(backup = True)

          print("")
          print("See you!")
          pygame.quit()
          raise SystemExit(0)

        # -------------------------------
        # "r": toggle right hand practice [DEPRECATED]
        # -------------------------------
        if (keys[pygame.K_r]) :
          userScore.toggleRightHandPractice()

        # ----------------
        # "s": export/save
        # ----------------
        if (keys[pygame.K_s]) :        
          userScore.exportToPrFile()
          pygame.display.set_caption(f"gangQin - v{REV_MAJOR}.{REV_MINOR} [{REV_TYPE}] ({REV_MONTH} {REV_YEAR}) - <{userScore.songName}.pr>")

        # -----------------------------------------
        # "v": toggle view (pianoroll / staffScope)
        # -----------------------------------------
        if (keys[pygame.K_v]) :
          staffScopeVisible = not(staffScopeVisible)
          if (staffScopeVisible) :
            if staffScopeWidget.isStaffAvailable(userScore.getCursor()) :
              print("[INFO] Staffscope view: ON")
            else :
              print("[INFO] Staffscope view: ON (but no data available!)")
          else :
            print("[INFO] Staffscope view: OFF")



      # -------------------------------------------------------------------------
      # Mouse click event handling
      # -------------------------------------------------------------------------
      elif (event.type == pygame.MOUSEBUTTONDOWN) :
        
        pianoRollWidget.mouseEvent(event)

        # Left click
        if (event.button == MOUSE_LEFT_CLICK) :
          clickMsg = True
          clickCoord = pygame.mouse.get_pos()
        
        # Scroll up
        if (event.button == MOUSE_SCROLL_UP) :
          
          # Find feature: go to the next cursor whose active notes match 
          # the current notes being pressed.
          # Note : use a copy of the MIDI notes list to prevent the 
          #        MIDI callback to mess with the function.
          if (pianoArbiter.hasActiveMidiInput()) :
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
          if (pianoArbiter.hasActiveMidiInput()) :
            print("[INFO] Forward search requested...")
            (suspendReq, pitchListHold) = userScore.search(pianoArbiter.midiCurr.copy(), direction = -1)
            if suspendReq :
              pianoArbiter.suspendReq(pitchListHold)
          
          elif ctrlKey :
            userScore.cursorStep(-10)
          else :
            userScore.cursorStep(-1)


      # -------------------------------------------------------------------------
      # Timer events
      # -------------------------------------------------------------------------
      elif (event.type == METRONOME_TASK) :
        metronomeObj.playTick()

      # elif (event.type == STATS_TASK) :
      #   statsObj.tick()



    # Clear the screen
    screen.fill(GUI_BACKGROUND_COLOR)

    # Render the keyboard
    keyboardWidget.reset()
    keyboardWidget.render(screen)

    # Show the key
    currKey = userScore.getCurrentKey()
    keyboardWidget.setKey(currKey)
    if (currKey != None) :
      text.render(screen, f"KEY: {currKey.root.upper()} {currKey.mode.upper()}", (200, 470), 2, GUI_TEXT_COLOR)
    
    # --------------------------------
    # Staffscope / pianoroll rendering
    # --------------------------------
    if staffScopeVisible :
      if staffScopeWidget.isStaffAvailable(userScore.getCursor()) :
        staffScopeWidget.loadCursor(userScore.getCursor())
        staffScopeWidget.declareStats(statsObj.cursorWrongNoteCount)
        staffScopeWidget.render()
      else :
        pianoRollWidget.drawPianoRoll(screen, userScore.getCurrentTimecode())  
    else :
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



    # --------------------------
    # Keyboard input arbitration
    # --------------------------
    # if userScore.hasWeakArbitration() :
    #   pianoArbiter.setWeakArbitrationNotes(userScore.getUnarbitredNotes())
    
    arbiterMsgQueue = pianoArbiter.eval(teacherNotes)

    for msg in arbiterMsgQueue :
      
      # Valid input
      if (msg == arbiter.MSG_CURSOR_NEXT) :
        userScore.cursorNext()
        # statsObj.intervalTimerUpdate(userScore.getCurrentTimecode())
        statsObj.reportCorrectNote()

        if (userScore.cursor == userScore.loopStart) :
          soundNotify.loopPassed()
        else :
          soundNotify.loopPassedReset()

        soundNotify.wrongNoteReset()

      # Invalid input
      if (msg == arbiter.MSG_RESET_COMBO) :  
        statsObj.reportWrongNote(userScore.getCursor())
        soundNotify.wrongNote()
        
        # TODO: MOVE THIS SECTION TO THE 'SCORE' OBJECT ↓↓↓
        # Strict looped practice: a wrong note resets the cursor to the beginning of the loop.
        if (userScore.loopStrictMode) :
          c = userScore.getCursor()
          comboDropHeight = c - userScore.loopStart
          
          # Bound looped practice (beginning and end loop are defined)
          if userScore.loopEnable :
              
            # Reset the cursor only if it is in the looping range.
            # (it could be temporarily outside for specific practice)
            if ((c >= userScore.loopStart) and (c <= userScore.loopEnd)) :
              userScore.setCursor(userScore.loopStart)
              
              if (statsObj.isComboBroken and (comboDropHeight > 3)) :
                # NOTE: requiring a minimal "drop height" to print the message avoids 
                # flooding the console when many wrong notes are played at once.
                print(f"[INFO] Wrong note! loop reset :(   (combo: {comboDropHeight})")

            else : 
              if statsObj.isComboBroken :
                print("[INFO] Wrong note outside the looping range.")

          # Unbound looped practice (only the beginning of the loop is defined)
          elif (userScore.loopStart != -1) :
            if (c >= userScore.loopStart) :
              userScore.setCursor(userScore.loopStart)
              
              if (statsObj.isComboBroken and (comboDropHeight > 3)):
                print(f"[INFO] Wrong note! loop reset :(   (combo: {comboDropHeight})")
            
            else : 
              if statsObj.isComboBroken :
                print("[INFO] Wrong note outside the looping range.")

        # No looped practice: a wrong note has no particular consequence.
        else :
          pass
    


    # ----------------------
    # Mouse cursor modifiers
    # ----------------------
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    
    # Is the cursor somewhere above the keyboard?
    # TODO: remove absolute coordinates, infer them from geometry
    if ((10 <= mouse_x <= 1310) and (300 <= mouse_y <= 450)) :  
      detectedNote = keyboardWidget.isActiveNoteClicked(pygame.mouse.get_pos())
      if detectedNote :
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
      else :
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    else:
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



    # --------------------
    # Mouse click handling
    # --------------------
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



    # -----------------------------------
    # Render text on screen (bitmap font)
    # -----------------------------------
    # text.showCursor(screen, userScore.getCursor(), userScore.scoreLength)
    # text.showBookmark(screen, userScore.getBookmarkIndex())
    # text.showActiveHands(screen, userScore.activeHands)
    text.showLoop(screen, userScore.loopEnable, userScore.loopStart, userScore.loopEnd, userScore.getCursor())
    text.showCombo(screen, statsObj.comboCount, statsObj.comboHighestSession, statsObj.comboHighestAllTime)
    text.showMetronome(screen, metronomeObj)



    # -----------------------
    # Finger selection widget
    # -----------------------
    fingerSelWidget.show(screen)
    
    if (fingerSelWidget.getEditedNote() != None) :
      if (userScore.getCursor() != fingerSelWidget.editedCursor) :
        fingerSelWidget.resetEditedNote()
    
    # Request to edit the fingersatz with automatic note highlighting
    if (setFingersatzMsg > 0) :
      fingerSelWidget.setFingerAutoHighlight(setFingersatzMsg, userScore.teacherNotes, userScore.activeHands)
      setFingersatzMsg = -1



    # ----------------
    # Metronome widget
    # ----------------
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


    clock.tick(GUI_FPS)

    # Update the display
    pygame.display.flip()

  # Quit Pygame
  pygame.quit()



# =============================================================================
# Standalone call
# =============================================================================
if (__name__ == "__main__") :
  gqApp = GangQin()
  
  # Call the file selection GUI
  gqApp.loadSong()

  # Main app
  gqApp.run()


