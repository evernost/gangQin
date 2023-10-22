# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : keyboard
# File name     : keyboard.py
# Purpose       : provides a grand piano widget for main app GUI
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from commons import *

import pygame
import fontUtils as fu

# For point in polygon test
from shapely.geometry import Point, Polygon

import utils



# =============================================================================
# Constants pool
# =============================================================================




# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This library is not intended to be called as a main.")



# =============================================================================
# Main code
# =============================================================================

class Keyboard :

  # ---------------------------------------------------------------------------
  # Constructor
  # ---------------------------------------------------------------------------
  def __init__(self, loc) :
    (self.x, self.y) = loc
    
    # -------------
    # Color palette
    # -------------
    
    # Black and white notes of the keyboard
    self.whiteNoteRGB = (255, 255, 255)
    self.blackNoteRGB = (0, 0, 0)
    
    # Rectangle indicating a note to play by left hand
    self.sqWhiteNoteLeftRGB = (200, 10, 0)
    self.sqBlackNoteLeftRGB = (200, 10, 0)

    # Rectangle indicating a note to play by right hand
    self.sqWhiteNoteRightRGB = (0, 200, 10)
    self.sqBlackNoteRightRGB = (0, 200, 10)

    # Rectangle indicating a note currently played by the MIDI input
    self.sqWhiteNoteNeutralRGB = (195, 195, 195)
    self.sqBlackNoteNeutralRGB = (155, 155, 155)

    # Rectangle of a note being played by both 
    # - a note to play by left hand
    # - the current MIDI input
    self.sqWhiteNoteOverlapLeftRGB = (255, 138, 132)
    self.sqBlackNoteOverlapLeftRGB = (255, 138, 132)

    # Rectangle of a note being played by both 
    # - a note to play by right hand
    # - the current MIDI input
    self.sqWhiteNoteOverlapRightRGB = (140, 255, 146)
    self.sqBlackNoteOverlapRightRGB = (140, 255, 146)

    # Color of the font indicating the finger
    self.fingerFontBlackNoteRGB = (240, 240, 240)
    self.fingerFontWhiteNoteRGB = (240, 240, 240)

    self.litKeysPolygons = []

    # Define the size of the keys
    self.a = WHITE_NOTE_HEIGHT; self.b = WHITE_NOTE_WIDTH
    self.c = BLACK_NOTE_HEIGHT; self.d = BLACK_NOTE_WIDTH
    self.s = NOTE_CHANFER
    self.e = NOTE_SPACING
    
    # Generate polygons for all notes and store them in <keyboardPolygons>
    self.makeKeyboardPolygons()

    # List of notes currently pressed
    self.activeNotes = []


  # ---------------------------------------------------------------------------
  # Method <makeKeyboardPolygons>
  # Generates the polygons depicting all the notes of a MIDI keyboard (128 notes)
  # For a grand piano, you'd use only polygons indexed from 21 (A0) to 108 (C8)
  # ---------------------------------------------------------------------------
  def makeKeyboardPolygons(self, grandPianoMode = True) :

    self.keyboardPolygons = []

    # Some shortcuts
    a = self.a; b = self.b
    c = self.c; d = self.d
    s = self.s
    e = self.e
    x0 = self.x - (12*b); y0 = self.y

    # Initialise output
    self.keyboardPolygons = [[] for _ in range(128)]

    # Generate polygons for each note
    for i in range(0, 128, 12) :
      
      # Note C
      if (grandPianoMode and (i == 108)) :
        self.keyboardPolygons[i] = [(x0+e, y0)]
        self.keyboardPolygons[i] += utils.Vector2D(0,a-s)
        self.keyboardPolygons[i] += utils.Vector2D(s,s)
        self.keyboardPolygons[i] += utils.Vector2D(b-(2*s)-(2*e),0)
        self.keyboardPolygons[i] += utils.Vector2D(s,-s)
        self.keyboardPolygons[i] += utils.Vector2D(0,-(a-s))
      else :
        self.keyboardPolygons[i] = [(x0+e, y0)]
        self.keyboardPolygons[i] += utils.Vector2D(0,a-s)
        self.keyboardPolygons[i] += utils.Vector2D(s,s)
        self.keyboardPolygons[i] += utils.Vector2D(b-(2*s)-(2*e),0)
        self.keyboardPolygons[i] += utils.Vector2D(s,-s)
        self.keyboardPolygons[i] += utils.Vector2D(0,-(a-c-e-s))
        self.keyboardPolygons[i] += utils.Vector2D(-2*d//3,0)
        self.keyboardPolygons[i] += utils.Vector2D(0,-(c+e))

      # Note Db
      self.keyboardPolygons[i+1] = [(x0+b-(2*d//3)+e, y0)]
      self.keyboardPolygons[i+1] += utils.Vector2D(0,c-e)
      self.keyboardPolygons[i+1] += utils.Vector2D(d-(2*e),0)
      self.keyboardPolygons[i+1] += utils.Vector2D(0,-(c-e))

      # Note D
      self.keyboardPolygons[i+2] = [(x0+b+(d//3)+e, y0)]
      self.keyboardPolygons[i+2] += utils.Vector2D(0,c+e)
      self.keyboardPolygons[i+2] += utils.Vector2D(-d//3,0)
      self.keyboardPolygons[i+2] += utils.Vector2D(0,a-c-e-s)
      self.keyboardPolygons[i+2] += utils.Vector2D(s,s)
      self.keyboardPolygons[i+2] += utils.Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+2] += utils.Vector2D(s,-s)
      self.keyboardPolygons[i+2] += utils.Vector2D(0,-(a-c-e-s))
      self.keyboardPolygons[i+2] += utils.Vector2D(-d//3,0)
      self.keyboardPolygons[i+2] += utils.Vector2D(0,-(c+e))

      # Note Eb
      self.keyboardPolygons[i+3] = [(x0+(2*b)-(d//3)+e, y0)]
      self.keyboardPolygons[i+3] += utils.Vector2D(0,c-e)
      self.keyboardPolygons[i+3] += utils.Vector2D(d-(2*e),0)
      self.keyboardPolygons[i+3] += utils.Vector2D(0,-(c-e))

      # Note Eb
      self.keyboardPolygons[i+4] = [(x0+(2*b)+(2*d//3)+e, y0)]
      self.keyboardPolygons[i+4] += utils.Vector2D(0,c+e)
      self.keyboardPolygons[i+4] += utils.Vector2D(-2*d//3,0)
      self.keyboardPolygons[i+4] += utils.Vector2D(0,a-c-e-s)
      self.keyboardPolygons[i+4] += utils.Vector2D(s,s)
      self.keyboardPolygons[i+4] += utils.Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+4] += utils.Vector2D(s,-s)
      self.keyboardPolygons[i+4] += utils.Vector2D(0,-(a-s))

      # Note F
      self.keyboardPolygons[i+5] = [(x0+(3*b)+e, y0)]
      self.keyboardPolygons[i+5] += utils.Vector2D(0,a-s)
      self.keyboardPolygons[i+5] += utils.Vector2D(s,s)
      self.keyboardPolygons[i+5] += utils.Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+5] += utils.Vector2D(s,-s)
      self.keyboardPolygons[i+5] += utils.Vector2D(0,-(a-c-e-s))
      self.keyboardPolygons[i+5] += utils.Vector2D(-2*d//3,0)
      self.keyboardPolygons[i+5] += utils.Vector2D(0,-(c+e))

      # Note Gb
      self.keyboardPolygons[i+6] = [(x0+(4*b)-(2*d//3)+e, y0)]
      self.keyboardPolygons[i+6] += utils.Vector2D(0,c-e)
      self.keyboardPolygons[i+6] += utils.Vector2D(d-(2*e),0)
      self.keyboardPolygons[i+6] += utils.Vector2D(0,-(c-e))

      # Note G
      self.keyboardPolygons[i+7] = [(x0+(4*b)+(d//3)+e, y0)]
      self.keyboardPolygons[i+7] += utils.Vector2D(0,c+e)
      self.keyboardPolygons[i+7] += utils.Vector2D(-d//3,0)
      self.keyboardPolygons[i+7] += utils.Vector2D(0,a-c-e-s)
      self.keyboardPolygons[i+7] += utils.Vector2D(s,s)
      self.keyboardPolygons[i+7] += utils.Vector2D(b-(2*s)-(2*e),0)
      self.keyboardPolygons[i+7] += utils.Vector2D(s,-s)
      self.keyboardPolygons[i+7] += utils.Vector2D(0,-(a-c-e-s))
      self.keyboardPolygons[i+7] += utils.Vector2D(-d//2,0)
      self.keyboardPolygons[i+7] += utils.Vector2D(0,-(c+e))

      if ((i+8) < 127) :

        # Note Ab
        self.keyboardPolygons[i+8] = [(x0+(5*b)-(d//2)+e, y0)]
        self.keyboardPolygons[i+8] += utils.Vector2D(0,c-e)
        self.keyboardPolygons[i+8] += utils.Vector2D(d-(2*e),0)
        self.keyboardPolygons[i+8] += utils.Vector2D(0,-(c-e))

        # Note A
        if (grandPianoMode and ((i+9) == 21)) :
          self.keyboardPolygons[i+9] = [(x0+(5*b)+e, y0)]
          self.keyboardPolygons[i+9] += utils.Vector2D(0,a-s)
          self.keyboardPolygons[i+9] += utils.Vector2D(s,s)
          self.keyboardPolygons[i+9] += utils.Vector2D(b-(2*s)-(2*e),0)
          self.keyboardPolygons[i+9] += utils.Vector2D(s,-s)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,-(a-c-e-s))
          self.keyboardPolygons[i+9] += utils.Vector2D(-d//3,0)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,-(c+e))
        else :
          self.keyboardPolygons[i+9] = [(x0+(5*b)+(d//2)+e, y0)]
          self.keyboardPolygons[i+9] += utils.Vector2D(0,c+e)
          self.keyboardPolygons[i+9] += utils.Vector2D(-d//2,0)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,a-c-e-s)
          self.keyboardPolygons[i+9] += utils.Vector2D(s,s)
          self.keyboardPolygons[i+9] += utils.Vector2D(b-(2*s)-(2*e),0)
          self.keyboardPolygons[i+9] += utils.Vector2D(s,-s)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,-(a-c-e-s))
          self.keyboardPolygons[i+9] += utils.Vector2D(-d//3,0)
          self.keyboardPolygons[i+9] += utils.Vector2D(0,-(c+e))

        # Note Bb
        self.keyboardPolygons[i+10] = [(x0+(6*b)-(d//3)+e, y0)]
        self.keyboardPolygons[i+10] += utils.Vector2D(0,c-e)
        self.keyboardPolygons[i+10] += utils.Vector2D(d-(2*e),0)
        self.keyboardPolygons[i+10] += utils.Vector2D(0,-(c-e))

        # Note B
        self.keyboardPolygons[i+11] = [(x0+(6*b)+(2*d//3)+e, y0)]
        self.keyboardPolygons[i+11] += utils.Vector2D(0,c+e)
        self.keyboardPolygons[i+11] += utils.Vector2D(-2*d//3,0)
        self.keyboardPolygons[i+11] += utils.Vector2D(0,a-c-e-s)
        self.keyboardPolygons[i+11] += utils.Vector2D(s,s)
        self.keyboardPolygons[i+11] += utils.Vector2D(b-(2*s)-(2*e),0)
        self.keyboardPolygons[i+11] += utils.Vector2D(s,-s)
        self.keyboardPolygons[i+11] += utils.Vector2D(0,-(a-s))

      x0 += 7*b



  # ---------------------------------------------------------------------------
  # METHOD <drawKeys>
  # Draw the keyboard using the polygons generated for each note.
  # ---------------------------------------------------------------------------
  def drawKeys(self, screenInst) :

    # Draw keys from MIDI code 21 (A0) to MIDI code 108 (C8) ie notes of a grand piano.
    for i in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
      if ((i % 12) in [1,3,6,8,10]) :
        pygame.draw.polygon(screenInst, self.blackNoteRGB, self.keyboardPolygons[i])
      else :
        pygame.draw.polygon(screenInst, self.whiteNoteRGB, self.keyboardPolygons[i])



  # ---------------------------------------------------------------------------
  # METHOD <keyPress>
  #
  # Highlight the given list of notes on the the keyboard
  # Indicate the hand to be used and the required finger if the information is 
  # available.
  # ---------------------------------------------------------------------------
  def keyPress(self, screenInst, noteList) :
    
    # -----------------------------
    # Detect "doubly" pressed notes
    # -----------------------------
    # Occurs when the score requests to press a key by one finger of each hand.
    # How many fingers are pressing this key is not very important per se
    # (you can't hit the key "more") yet it gives info regarding how the 
    # key should be played.
    # If the key is pressed by several fingers of the same hand, there is no
    # special processing to be done. 
    noteListByPitch = [[] for x in range(128)]
    for (index, noteObj) in enumerate(noteList) :
      noteListByPitch[noteObj.pitch].append([index, noteObj])
      
    for subList in noteListByPitch :
      
      # A given key is hit exactly twice at the same time
      if (len(subList) == 2) :
        
        # One note is hit by one hand
        if ((subList[0][1].hand != UNDEFINED_HAND) and (subList[1][1].hand != UNDEFINED_HAND)) :
          if (subList[0][1].hand != subList[1][1].hand) :
          
            # White note highlighting
            if ((noteObj.pitch % 12) in WHITE_NOTES_CODE_MOD12) :
              self._doubleHandWhiteKeyPress(screenInst, noteObj)

            # Black note highlighting
            if ((noteObj.pitch % 12) in BLACK_NOTES_CODE_MOD12) :
              self._doubleHandBlackKeyPress(screenInst, noteObj)

            # These notes are now displayed, we can remove them from the list
            # and go on with the "normal" notes
            if subList[0][0] > subList[1][0] :
              del noteList[subList[0][0]]
              del noteList[subList[1][0]]
            else :
              del noteList[subList[1][0]]
              del noteList[subList[0][0]]

      if (len(subList) >= 3) :
        print("[WARNING] Odd score: that's a lot of fingers to press one single note *questionning emoji*")


    for noteObj in noteList :

      # White note highlighting
      if ((noteObj.pitch % 12) in WHITE_NOTES_CODE_MOD12) :
        self._singleHandWhiteKeyPress(screenInst, noteObj)

      # Black note highlighting
      if ((noteObj.pitch % 12) in BLACK_NOTES_CODE_MOD12) :
        self._singleHandBlackKeyPress(screenInst, noteObj)

      # Register this keypress for note overlap management
      self.activeNotes.append(noteObj)
      
      # ------------------------------
      # Note click detection materials
      # ------------------------------
      # Store the polygons associated to the "teacher notes"
      if ((noteObj.hand == LEFT_HAND) or (noteObj.hand == RIGHT_HAND)) :
        # This makes the hitbox for click on the lit part of the key only:
        #self.litKeysPolygons.append((sq, pitch))

        # This makes the hitbox for click on the entire key:
        self.litKeysPolygons.append((self.keyboardPolygons[noteObj.pitch], noteObj))



  # ---------------------------------------------------------------------------
  # METHOD <_singleHandWhiteKeyPress> (private)
  #
  # TODO
  # ---------------------------------------------------------------------------
  def _singleHandWhiteKeyPress(self, screenInst, noteObj) :

    eps = 3
    u = [x[0] for x in self.keyboardPolygons[noteObj.pitch]]
    x0 = min(u); y0 = self.y + self.c + self.e
    h = self.a - (self.c + self.e) - (2*eps)
    w = self.b - (2*self.e) - (2*eps)
    sq = [(x0 + eps, y0 + eps)]
    sq += utils.Vector2D(0, h)
    sq += utils.Vector2D(w,0)
    sq += utils.Vector2D(0,-h)
    
    if (noteObj.hand == LEFT_HAND) :
      if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
        pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapLeftRGB, sq)
      elif (noteObj.voice != VOICE_DEFAULT) :
        pygame.draw.polygon(screenInst, VOICE_COLOR[noteObj.voice], sq)
      else :
        pygame.draw.polygon(screenInst, self.sqWhiteNoteLeftRGB, sq)
    
    if (noteObj.hand == RIGHT_HAND) :
      if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
        pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapRightRGB, sq)
      elif (noteObj.voice != VOICE_DEFAULT) :
        pygame.draw.polygon(screenInst, VOICE_COLOR[noteObj.voice], sq)
      else :
        pygame.draw.polygon(screenInst, self.sqWhiteNoteRightRGB, sq)

    if (noteObj.hand == UNDEFINED_HAND) :
      pygame.draw.polygon(screenInst, self.sqWhiteNoteNeutralRGB, sq)

    # Show finger number
    if (noteObj.finger in [1,2,3,4,5]) :
      # Font size 1
      #fu.renderText(screenInst, str(finger), (x0+10,y0+23), 1, self.fingerFontWhiteNoteRGB)
      
      # Font size 2
      fu.renderText(screenInst, str(noteObj.finger), (x0+7, y0+19), 2, self.fingerFontWhiteNoteRGB)



  # ---------------------------------------------------------------------------
  # METHOD <_singleHandBlackKeyPress> (private)
  #
  # TODO
  # ---------------------------------------------------------------------------
  def _singleHandBlackKeyPress(self, screenInst, noteObj) :

    # Build the rectangle that will be drawn on top of the note
    eps = 3
    u = [x[0] for x in self.keyboardPolygons[noteObj.pitch]]
    x0 = min(u); y0 = self.y + 50
    h = self.c - self.e - (2*eps) - 50
    w = self.d - (2*self.e) - (2*eps)
    sq = [(x0 + eps, y0 + eps)]
    sq += utils.Vector2D(0, h)
    sq += utils.Vector2D(w,0)
    sq += utils.Vector2D(0,-h)

    # Note: function is called to show the MIDI input first, then the MIDI file notes.
    # This has an impact on overlap handling
    if (noteObj.hand == LEFT_HAND) :
      if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
        pygame.draw.polygon(screenInst, self.sqBlackNoteOverlapLeftRGB, sq)
      else :
        pygame.draw.polygon(screenInst, self.sqBlackNoteLeftRGB, sq)

    if (noteObj.hand == RIGHT_HAND) :
      if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
        pygame.draw.polygon(screenInst, self.sqBlackNoteOverlapRightRGB, sq)
      else :
        pygame.draw.polygon(screenInst, self.sqBlackNoteRightRGB, sq)

    if (noteObj.hand == UNDEFINED_HAND) :
      pygame.draw.polygon(screenInst, self.sqBlackNoteNeutralRGB, sq)

    # Show finger number
    if (noteObj.finger in [1,2,3,4,5]) :
      # Font size 1
      #fu.renderText(screenInst, str(noteObj.finger), (x0+3, y0+23), 1, self.fingerFontBlackNoteRGB)
      
      # Font size 2
      fu.renderText(screenInst, str(noteObj.finger), (x0+1, y0+19), 2, self.fingerFontBlackNoteRGB)
    


  # ---------------------------------------------------------------------------
  # METHOD <_doubleHandWhiteKeyPress> (private)
  #
  # TODO
  # ---------------------------------------------------------------------------
  def _doubleHandWhiteKeyPress(self, screenInst, noteObj) :

    # Build the rectangle that will be drawn on top of the note
    eps = 3
    u = [x[0] for x in self.keyboardPolygons[noteObj.pitch]]
    x0 = min(u); y0 = self.y + self.c + self.e
    h = self.a - (self.c + self.e) - (2*eps)
    w = self.b - (2*self.e) - (2*eps)
    
    rectLeft = [(x0 + eps, y0 + eps)]
    rectLeft += utils.Vector2D(0, h)
    rectLeft += utils.Vector2D(w-eps, -h)

    rectRight = [(x0 + eps + w, y0 + eps)]
    rectRight += utils.Vector2D(0, h)
    rectRight += utils.Vector2D(-w+eps,0)
    
    if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
      pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapLeftRGB, rectLeft)
    else :
      pygame.draw.polygon(screenInst, self.sqWhiteNoteLeftRGB, rectLeft)
    
    if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
      pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapRightRGB, rectRight)
    else :
      pygame.draw.polygon(screenInst, self.sqWhiteNoteRightRGB, rectRight)

    # Show finger number
    # TODO



  # ---------------------------------------------------------------------------
  # METHOD <_doubleHandBlackKeyPress> (private)
  #
  # TODO
  # ---------------------------------------------------------------------------
  def _doubleHandBlackKeyPress(self, screenInst, noteObj) :

    # Build the rectangle that will be drawn on top of the note
    eps = 3
    u = [x[0] for x in self.keyboardPolygons[noteObj.pitch]]
    x0 = min(u); y0 = self.y + 50
    h = self.c - self.e - (2*eps) - 50
    w = self.d - (2*self.e) - (2*eps)
    
    rectLeft = [(x0 + eps, y0 + eps)]
    rectLeft += utils.Vector2D(0, h)
    rectLeft += utils.Vector2D(w-1, -h)

    rectRight = [(x0 + eps + w, y0 + eps)]
    rectRight += utils.Vector2D(0, h)
    rectRight += utils.Vector2D(-w+1,0)
    
    if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
      pygame.draw.polygon(screenInst, self.sqBlackNoteOverlapLeftRGB, rectLeft)
    else :
      pygame.draw.polygon(screenInst, self.sqBlackNoteLeftRGB, rectLeft)
    
    if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
      pygame.draw.polygon(screenInst, self.sqBlackNoteOverlapRightRGB, rectRight)
    else :
      pygame.draw.polygon(screenInst, self.sqBlackNoteRightRGB, rectRight)

    # Show finger number
    # TODO


  # ---------------------------------------------------------------------------
  # METHOD <isActiveNoteClicked>
  #
  # Given a click coordinates, indicate whether it is an active key (a "lit" key)
  # that has been clicked.
  # ---------------------------------------------------------------------------
  def isActiveNoteClicked(self, clickX, clickY) :
    for (currLitNotePolygon, currNote) in self.litKeysPolygons :

      # Intersection!
      if Point(clickX, clickY).within(Polygon(currLitNotePolygon)) :
        return currNote

    return None



  # ---------------------------------------------------------------------------
  # Method <showScale>
  # 
  # Toggles the display of the scale
  # ---------------------------------------------------------------------------
  def showScale(self) :
    print("[NOTE] Showing the scale will be available in a future release.")








  # ---------------------------------------------------------------------------
  # Method <reset>
  #
  # The object keeps track of all calls to <keyPress>.
  # This function resets all notes stored.
  # Useful for the note overlapping detection.
  # ---------------------------------------------------------------------------
  def reset(self) :
    self.activeNotes = []
    self.litKeysPolygons = []


