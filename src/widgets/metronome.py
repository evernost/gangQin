# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : metronome
# File name     : metronome.py
# Purpose       : metronome object
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Saturday, 31 August 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
# Project specific constants
from commons import *
import src.text as text
import src.widgets.widget as widget

# Standard libraries
import numpy as np
import pygame



# =============================================================================
# CONSTANTS
# =============================================================================
MSG_TEMPO_UPDATE = 1
MSG_TIMER_ON = 2
MSG_TIMER_OFF = 3



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Metronome(widget.Widget)  :
  """
  METRONOME object

  Class definition for the Metronome widget.
  Provides a simple metronome feature to the main application.
  
  The Metronome class derives from the Widget class.
  """

  def __init__(self, top, bpm = 120, num = 4, denom = 4) :
    
    # Call the Widget init method
    super().__init__(top, loc = WIDGET_LOC_UNDEFINED)

    self.name = "metronome"

    self.enable = False
        
    self.bpm = bpm
    self.num = num      # Number of beats per measure
    self.denom = denom  # 1 = whole note, 2 = half note, 4 = quarter note, 8 = eighth note etc.

    self.counter = 1

    self._optionMode = False
    self._switched = False

    self.tickDuration = 0.2
    self.tickVolume = 0.3
    
    self.tickInterval_ms = 1000

    self.METRONOME_TASK = pygame.USEREVENT + 1

    self.msgQueue = []

    self._prepareWaves()
    self._init()



  # ---------------------------------------------------------------------------
  # METHOD Metronome._prepareWaves()
  # ---------------------------------------------------------------------------
  def _prepareWaves(self) :
    """
    Creates the sound waveforms for the 'tick' and 'tock'.
    """
    
    t = np.linspace(0, self.tickDuration, int(44100 * self.tickDuration), endpoint = False)
    tickHigh  = np.int16(32767 * self.tickVolume * np.sin(2 * np.pi * 880.0 * t) * np.exp(-t/(self.tickDuration/3)))
    tickLow   = np.int16(32767 * self.tickVolume * np.sin(2 * np.pi * 440.0 * t) * np.exp(-t/(self.tickDuration/3)))
    tickHigh  = tickHigh.tobytes()
    tickLow   = tickLow.tobytes()
    self.tickHighSound = pygame.mixer.Sound(buffer = tickHigh)
    self.tickLowSound = pygame.mixer.Sound(buffer = tickLow)



  # ---------------------------------------------------------------------------
  # METHOD Metronome._init()
  # ---------------------------------------------------------------------------
  def _init(self) -> None :
    """
    Description is TODO.
    """
    
    pygame.time.set_timer(self.METRONOME_TASK, self.getInterval_ms())
    pygame.mixer.init(frequency = 44100, size = -16, channels = 1, buffer = 512)




  # ---------------------------------------------------------------------------
  # METHOD Metronome.getInterval_ms()
  # ---------------------------------------------------------------------------
  def getInterval_ms(self) -> float :
    """
    Returns the value the interval (in ms) between 2 clicks of the metronome.
    """
    
    return (1000*60//self.bpm)
  

      
  # # ---------------------------------------------------------------------------
  # # METHOD Metronome.keyRelease(pygameKeys)
  # # ---------------------------------------------------------------------------
  # def keyRelease(self, key) :
  #   """
  #   Updates the metronome object status (ON, OFF, increase tempo, etc.) 
  #   based on the keys that have been released.
  #   """

  #   if (key == pygame.K_m) :

  #     if self._switched :
  #       self._switched = False

  #     else : 
  #       if self._optionMode :
  #         self._optionMode = False
  #       else :
  #         self.enable = False
  #         self.counter = 1
  #         self.msgQueue.append(MSG_TIMER_OFF)
        


  # ---------------------------------------------------------------------------
  # METHOD Sequencer._onKeyEvent()                                  [INHERITED]
  # ---------------------------------------------------------------------------
  def _onKeyEvent(self, key, type, modifier = "") :
    """
    Function is triggered by a keypress.
    """
    
    if (type == pygame.KEYDOWN) :
      
      # Simple keypresses (no modifiers)
      if (modifier == "") :
        
        if (key == pygame.K_m) :
          if not(self.enable) :
            self.enable = True
            self._switched = True
            # self.msgQueue.append(MSG_TIMER_ON)
            pygame.time.set_timer(self.METRONOME_TASK, self.getInterval_ms())
            self.counter = self.num
            self._playTick()

        if (key == pygame.K_KP_PLUS) :
          self._optionMode = True
          self.bpm += 1
          pygame.time.set_timer(self.METRONOME_TASK, self.getInterval_ms())
          # if not(MSG_TEMPO_UPDATE in self.msgQueue) :
          #   self.msgQueue.append(MSG_TEMPO_UPDATE)
        
        if (key == pygame.K_KP_MINUS) :
          self._optionMode = True
          self.bpm -= 1
          pygame.time.set_timer(self.METRONOME_TASK, self.getInterval_ms())
          # if not(MSG_TEMPO_UPDATE in self.msgQueue) :
          #   self.msgQueue.append(MSG_TEMPO_UPDATE)

        else :
          self.switched = False
          self._optionMode = False

    elif (type == pygame.KEYUP) :

      # Simple keypresses (no modifiers)
      if (modifier == "") :

        if (key == pygame.K_m) :

          if self._switched :
            self._switched = False

          else : 
            if self._optionMode :
              self._optionMode = False
            else :
              self.enable = False
              self.counter = 1
              pygame.time.set_timer(self.METRONOME_TASK, 0)



  # ---------------------------------------------------------------------------
  # METHOD Sequencer._onOtherEvent()                                [INHERITED]
  # ---------------------------------------------------------------------------
  def _onOtherEvent(self, event) :
    """
    Function is triggered by a keypress.
    """
    
    if (event.type == self.METRONOME_TASK) :
      self._playTick()



  # ---------------------------------------------------------------------------
  # METHOD Metronome._playTick()                                      [PRIVATE]
  # ---------------------------------------------------------------------------
  def _playTick(self) :
    """
    Plays the metronome 'tic' sound.
    """

    if self.enable :

      if (self.counter == self.num) :
        self.tickHighSound.play()
        self.counter = 1

      else :
        self.tickLowSound.play()
        self.counter += 1



  # ---------------------------------------------------------------------------
  # METHOD Metronome.getMsg()
  # ---------------------------------------------------------------------------
  def clearQueue(self) :
    self.msgQueue = []






  # # ----------------
  # # Metronome widget
  # # ----------------
  # # Read metronome messages
  # if (len(metronomeObj.msgQueue) > 0) :
  #   for msg in metronomeObj.msgQueue :
  #     if (msg == metronome.MSG_TEMPO_UPDATE) :
  #       pygame.time.set_timer(METRONOME_TASK, metronomeObj.getInterval_ms())
      
  #     elif (msg == metronome.MSG_TIMER_OFF) :
  #       pygame.time.set_timer(METRONOME_TASK, 0)

  #     elif (msg == metronome.MSG_TIMER_ON) :
  #       pygame.time.set_timer(METRONOME_TASK, metronomeObj.getInterval_ms())
  #       metronomeObj.counter = metronomeObj.num
  #       metronomeObj.playTick()
    
  #   metronomeObj.clearQueue()




  # ---------------------------------------------------------------------------
  # METHOD: Keyboard.render()
  # ---------------------------------------------------------------------------
  def render(self) -> None :
    """
    Renders the widget on screen.
    """

    if self.enable :
      text.render(self.top.screen, f"BPM:{self.bpm} - {self.num}/{self.denom} - {self.counter}", (950, 470), 2, GUI_TEXT_COLOR)
  
    

# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'metronome.py'")