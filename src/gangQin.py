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
import mido.backends.rtmidi   # Not used but necessary for the .exe generation

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
    self.screen = pygame.display.set_mode((GUI_SCREEN_WIDTH, GUI_SCREEN_HEIGHT))
    self.screenWidth = self.screen.get_size()[0]
    self.screenHeight = self.screen.get_size()[1]
    self.clock = pygame.time.Clock()
    pygame.key.set_repeat(250, 50)    # Enable key repeats (250 ms delay before repeat, repeat every 50 ms)
    self._backgroundInit()
    self.running = False
    self.midiPort = None

    # Limit the key events to avoid unnecessary processing
    pygame.event.set_allowed([
      pygame.KEYDOWN,
      pygame.KEYUP,
      pygame.MOUSEBUTTONDOWN,
      pygame.QUIT
    ])

    # Initialise the widgets
    self.widgets = {
      WIDGET_ID_SCORE       : score.Score(self),
      WIDGET_ID_KEYBOARD    : keyboard.Keyboard(self, loc = (10, 300)),
      WIDGET_ID_PIANOROLL   : pianoRoll.PianoRoll(self, loc = (10, 50)),
      WIDGET_ID_STAFFSCOPE  : staffScope.StaffScope(self),
      #fingerSelector.FingerSelector(self),
      #metronome.Metronome(self),
      #arbiter.Arbiter(self),
      #stats.Stats(self),
      #notify.Notify(self)
      WIDGET_ID_SEQUENCER   : sequencer.Sequencer(self)
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
      self.widgets[WIDGET_ID_SCORE].loadGQ3File(songFile)
      self.widgets[WIDGET_ID_STAFFSCOPE].load(songFile)

    # Update the app properties
    pygame.display.set_caption(f"gangQin player - v{REV_MAJOR}.{REV_MINOR} [{REV_TYPE}] ({REV_MONTH} {REV_YEAR}) - Song: {self.songName}")

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
    self._onExit()



  # ---------------------------------------------------------------------------
  # METHOD: GangQin._midiCallback()
  # ---------------------------------------------------------------------------
  def _midiCallback(self, midiMessage) :
    """
    This function is called on every MIDI event coming from the external MIDI
    keyboard.
    """

    self.widgets[WIDGET_ID_KEYBOARD].updateFromMidi(midiMessage)
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

    if (self.midiPort != None) :
      self.midiPort.close()

    #statsObj.userActivity()
    #statsObj.save()
    self.widgets[WIDGET_ID_SCORE].exportToPrFile(backup = True)

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



  # ---------------------------------------------------------------------------
  # METHOD: GangQin._midiInterfaceInit()                              [PRIVATE]
  # ---------------------------------------------------------------------------
  def _midiInterfaceInit(self, selectedDevice: str) :
    """
    Opens the MIDI keyboard interface pointed by the string descriptor in 
    'selectedDevice'.

    When not using any MIDI keyboard, use selectedDevice = "None".
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



# =============================================================================
# MAIN
# =============================================================================
if (__name__ == "__main__") :
  gqApp = GangQin()
  
  # Call the file selection GUI
  gqApp.loadSong()

  # Main app
  gqApp.run()


