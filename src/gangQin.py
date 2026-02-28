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
# EXTERNALS
# =============================================================================
# Project specific constants
from commons import *

# Graphical interface
import pygame

# Widgets
import src.widgets.fileSelectionGUI as fileSelectionGUI
import src.widgets.fingerSelector as fingerSelector
import src.widgets.keyboard as keyboard
import src.widgets.pianoRoll as pianoRoll
import src.widgets.trackSelectionGUI as trackSelectionGUI
import src.widgets.staffScope as staffScope
import src.widgets.sequencer as sequencer
import src.widgets.stats as stats

# Utilities
import arbiter
import score


# MIDI
import mido
import mido.backends.rtmidi   # Not used, but necessary for the .exe generation

# Standard libs
import os



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class GangQin :

  """
  GANG_QIN object

  Description is TODO.
  """
  
  # ---------------------------------------------------------------------------
  # METHOD: GangQin.__init__
  # ---------------------------------------------------------------------------
  def __init__(self) :
    
    # TODO: check the minimal requirements to run properly
    # - '/song' directory must exist
    # ...?
    # self._envCheck()

    # Initialise attributes
    self.songFile = ""    # Example: "./songs/my_song.mid"
    self.songDir  = ""    # Example: './songs'
    self.songName = ""    # Example: 'my_song'
    self.songType = ""    # Example: "mid"

    # Initialise pygame
    pygame.init()
    self.screen       = pygame.display.set_mode((GUI_SCREEN_WIDTH, GUI_SCREEN_HEIGHT))
    self.screenWidth  = self.screen.get_size()[0]
    self.screenHeight = self.screen.get_size()[1]
    self.clock        = pygame.time.Clock()
    
    # Enable key repeats (250 ms delay before repeat, repeat every 50 ms)
    pygame.key.set_repeat(250, 50)
    
    self._backgroundInit()
    self.running = False
    self.midiPort = None
    self.midiTranspose = 0    # Indicate here the transpose state of the input keyboard, so that the app adapts to it.

    # Limit the supported key events to avoid unnecessary processing
    pygame.event.set_allowed([
      pygame.KEYDOWN,
      pygame.KEYUP,
      pygame.MOUSEBUTTONDOWN,
      pygame.QUIT
    ])

    # Create the widgets
    self.widgets = {
      WIDGET_ID_SCORE           : score.Score(self),
      WIDGET_ID_KEYBOARD        : keyboard.Keyboard(self, loc = (10, 300)),
      WIDGET_ID_PIANOROLL       : pianoRoll.PianoRoll(self, loc = (10, 50)),
      WIDGET_ID_STAFFSCOPE      : staffScope.StaffScope(self, loc = WIDGET_LOC_UNDEFINED),
      WIDGET_ID_FINGERSELECTOR  : fingerSelector.FingerSelector(self, loc = (490, 470)),
      WIDGET_ID_ARBITER         : arbiter.Arbiter(self),
      WIDGET_ID_SEQUENCER       : sequencer.Sequencer(self),
      WIDGET_ID_STATS           : stats.Stats(self)
      #metronome.Metronome(self),
      #stats.Stats(self),
      #notify.Notify(self)
    }
    


  # ---------------------------------------------------------------------------
  # METHOD: GangQin.loadSong()
  # ---------------------------------------------------------------------------
  def loadSong(self) :
    """
    Calls the song/MIDI interface selector.
    Initialises the application accordingly.
    """

    # Call the file selection GUI
    fsGUI = fileSelectionGUI.new()
    (selectedDevice, selectedFile) = fsGUI.run()

    if ((selectedFile == "") or (selectedFile == "None")) :
      print("[INFO] No file selected, exiting...")
      exit()
    else :
      (rootDir, rootNameExt) = os.path.split(selectedFile)
      (rootName, _) = os.path.splitext(rootNameExt)
      self.selectedFile = selectedFile
      self.songDir  = rootDir
      self.songName = rootName

    # If a MIDI file is selected, show the track selection GUI
    if selectedFile.endswith(".mid") :
      self.songType = "mid"
      trackSel = trackSelectionGUI.new()
      trackSel.load(selectedFile)
      midiTracks = trackSel.show()
      self.widgets[WIDGET_ID_SCORE].loadMidiFile(selectedFile, midiTracks)
      self.widgets[WIDGET_ID_STATS].load(selectedFile)
    elif selectedFile.endswith(".pr") :
      self.songType = "pr"
      self.widgets[WIDGET_ID_SCORE].loadPrFile(selectedFile)
      self.widgets[WIDGET_ID_STAFFSCOPE].load(selectedFile)
      self.widgets[WIDGET_ID_STATS].load(selectedFile)
    elif selectedFile.endswith(".gq3") :
      self.songType = "gq3"
      self.widgets[WIDGET_ID_SCORE].loadGq3File(selectedFile)
      self.widgets[WIDGET_ID_STAFFSCOPE].load(selectedFile)
      self.widgets[WIDGET_ID_STATS].load(selectedFile)
    else :
      print("[ERROR] Internal error (unsupported file extension)")    

    # Update the app properties
    pygame.display.set_caption(f"gangQin player - v{REV_MAJOR}.{REV_MINOR} [{REV_TYPE}] ({REV_MONTH} {REV_YEAR}) - Song: {rootNameExt}")

    # Initialise the selected MIDI interface (if any)
    self._midiInterfaceInit(selectedDevice)



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
        if (event.type == pygame.KEYDOWN) :
          if (event.key == pygame.K_q) :
            self._onExit()
          elif (event.key == pygame.K_s) :
            self.widgets[WIDGET_ID_SCORE].save()
        elif (event.type == pygame.QUIT) :
          self._onExit()

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
    self._onExit()



  # ---------------------------------------------------------------------------
  # METHOD: GangQin._midiInterfaceInit()                              [PRIVATE]
  # ---------------------------------------------------------------------------
  def _midiInterfaceInit(self, selectedDevice: str) :
    """
    Opens the MIDI keyboard interface pointed by the string descriptor in 
    'selectedDevice'.

    Assigns the callback function that catches the MIDI events.

    NOTE: when no MIDI keyboard is needed, use selectedDevice = "None".
    """

    if (selectedDevice != "None") :
      try :
        self.midiPort = mido.open_input(selectedDevice, callback = self._midiCallback)
      except Exception as err :
        print("[WARNING] Failed to open the MIDI device (it is used by another software?): running in navigation mode.")
        self.midiPort = None  
    else :
      print("[NOTE] No MIDI interface selected: running in navigation mode.")
      self.midiPort = None



  # ---------------------------------------------------------------------------
  # METHOD: GangQin._midiCallback()
  # ---------------------------------------------------------------------------
  def _midiCallback(self, midiMessage) :
    """
    This function is triggered for each incoming MIDI event from the external 
    keyboard and routes the message to all interested widgets.
    """

    # Run some preprocessing on the message
    # - Filter out unused messages
    # - apply transpose when activated
    midiMessage = self._midiPreProcessor(midiMessage)

    if (WIDGET_ID_KEYBOARD in self.widgets) :
      self.widgets[WIDGET_ID_KEYBOARD].onExternalMidiEvent(midiMessage)
    
    if (WIDGET_ID_ARBITER in self.widgets) :
      self.widgets[WIDGET_ID_ARBITER].onExternalMidiEvent(midiMessage)
    
    if (WIDGET_ID_SEQUENCER in self.widgets) :
      self.widgets[WIDGET_ID_SEQUENCER].onExternalMidiEvent(midiMessage)

    if (WIDGET_ID_PIANOROLL in self.widgets) :
      self.widgets[WIDGET_ID_PIANOROLL].onExternalMidiEvent(midiMessage)

    if (WIDGET_ID_STATS in self.widgets) :
      self.widgets[WIDGET_ID_STATS].userActivity()



  # ---------------------------------------------------------------------------
  # METHOD: GangQin._midiPreProcessor()
  # ---------------------------------------------------------------------------
  def _midiPreProcessor(self, midiMessage) :
    """
    Description is TODO.
    """

    # TRANSPOSED INPUT MODE
    # The app gives the possibility to play the song while the input keyboard
    # is actually in a transposed mode:
    # - either because the user plays a transposed version of the song
    # - or because the keyboard settings transpose the MIDI messages.
    # This preprocessing reverts the transposition and makes the notes appear
    # at their correct location.
    if (midiMessage.type == "note_on") :
      midiMessage.note = midiMessage.note - self.midiTranspose

    elif (midiMessage.type == "note_off") :
      midiMessage.note = midiMessage.note - self.midiTranspose

    else :
      pass
    
    return midiMessage



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

    (w, h) = len(patternData[0]), len(patternData)
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

    self.appRunning = False

    if (self.midiPort != None) :
      self.midiPort.close()

    if (WIDGET_ID_STATS in self.widgets) :
      self.widgets[WIDGET_ID_STATS].logUserActivity()
      self.widgets[WIDGET_ID_STATS].save()
    
    if (WIDGET_ID_SCORE in self.widgets) :
      self.widgets[WIDGET_ID_SCORE].save(backup = True)

    print("")
    print("See you!")
    pygame.quit()
    exit()



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



# =============================================================================
# MAIN
# =============================================================================
if (__name__ == "__main__") :
  gqApp = GangQin()
  
  # Call the file selection GUI
  gqApp.loadSong()

  # Main app
  gqApp.run()


