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

    # Define the current key the song is in
    self.activeKey = []



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
    
    if (len(self.activeKey) > 0) :
      for i in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        if ((i % 12) in BLACK_NOTES_CODE_MOD12) :
          if ((i % 12) in self.activeKey) :
            pygame.draw.polygon(screenInst, self.blackNoteRGB, self.keyboardPolygons[i])
          else :
            pygame.draw.polygon(screenInst, (100, 100, 100), self.keyboardPolygons[i])
        else :
          if ((i % 12) in self.activeKey) :
            pygame.draw.polygon(screenInst, self.whiteNoteRGB, self.keyboardPolygons[i])
          else :
            pygame.draw.polygon(screenInst, (220, 220, 220), self.keyboardPolygons[i])
    
    
    else :
      for i in range(LOW_KEY_MIDI_CODE, HIGH_KEY_MIDI_CODE+1) :
        if ((i % 12) in [1, 3, 6, 8, 10]) :
          pygame.draw.polygon(screenInst, self.blackNoteRGB, self.keyboardPolygons[i])
        else :
          pygame.draw.polygon(screenInst, self.whiteNoteRGB, self.keyboardPolygons[i])



  def setKey(self, scaleObj) :
    if (scaleObj != None) :
      self.activeKey = scaleObj.activeNotes
    else :
      self.activeKey = []



  # ---------------------------------------------------------------------------
  # METHOD <keyPress>
  #
  # Highlight the given list of notes on the the keyboard.
  # Indicate the hand to be used and the required finger if the information is 
  # available.
  # ---------------------------------------------------------------------------
  def keyPress(self, screenInst, noteList) :
    
    # Preprocess the list so that the earliest notes are drawn first
    # This avoids the sustained notes to be drawn on top.
    noteList.sort(key = lambda x: x.startTime)

    # -------------------------------
    # Filter notes with null duration
    # -------------------------------
    # A bit of an oddity. I am still unsure as of why that might happen.
    newNoteList = []
    for noteObj in noteList :
      if not(noteObj.fromKeyboardInput) :
        if (noteObj.startTime != noteObj.stopTime):
          newNoteList.append(noteObj)
        # else :
        #   print("[WARNING] Null duration note detected")
      else :
        newNoteList.append(noteObj)
    noteList = newNoteList

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
      if not(noteObj.sustained) :
        noteListByPitch[noteObj.pitch].append([index, noteObj])
      
    for subList in noteListByPitch :
      
      # A given key is hit exactly twice at the same time
      if (len(subList) == 2) :
        
        # One note is hit by one hand
        noteObj1 = subList[0][1]; noteObj2 = subList[1][1]
        if ((noteObj1.hand != UNDEFINED_HAND) and (noteObj2.hand != UNDEFINED_HAND)) :
          if (noteObj1.hand != noteObj2.hand) :
          
            # White note highlighting
            if ((noteObj1.pitch % 12) in WHITE_NOTES_CODE_MOD12) :
              self._doubleHandWhiteKeyPress(screenInst, noteObj1)

            # Black note highlighting
            if ((noteObj1.pitch % 12) in BLACK_NOTES_CODE_MOD12) :
              self._doubleHandBlackKeyPress(screenInst, noteObj1)

            # These notes are now displayed, we can remove them from the list
            # and go on with the "normal" notes
            if subList[0][0] > subList[1][0] :
              del noteList[subList[0][0]]
              del noteList[subList[1][0]]
            else :
              del noteList[subList[1][0]]
              del noteList[subList[0][0]]

          # The key is hit twice with the same hand
          else :
            del noteList[subList[0][0]]

      if (len(subList) >= 3) :
        print("[WARNING] Odd score: that's a lot of fingers to press one single note *questionning emoji*")


    for noteObj in noteList :

      # White note highlighting
      if (noteObj.keyColor == WHITE_KEY) :
        self._singleHandWhiteKeyPress(screenInst, noteObj)

      # Black note highlighting
      if (noteObj.keyColor == BLACK_KEY) :
        self._singleHandBlackKeyPress(screenInst, noteObj)
      
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
  # Show a given white note on the keyboard as pressed.
  # ---------------------------------------------------------------------------
  def _singleHandWhiteKeyPress(self, screenInst, noteObj) :

    # Build the little rectangle drawn on top of the note, to show that it is pressed
    eps = 3
    u = [x[0] for x in self.keyboardPolygons[noteObj.pitch]]
    x0 = min(u); y0 = self.y + self.c + self.e
    h = self.a - (self.c + self.e) - (2*eps)
    w = self.b - (2*self.e) - (2*eps)
    rect = [(x0 + eps, y0 + eps)]
    rect += utils.Vector2D(0, h)
    rect += utils.Vector2D(w, 0)
    rect += utils.Vector2D(0, -h)
    
    # Notes played from the MIDI keyboard have a different shape
    if (noteObj.fromKeyboardInput) :
      #pygame.draw.polygon(screenInst, self.sqWhiteNoteNeutralRGB, sq)
      pygame.draw.circle(screenInst, (10, 10, 10), (x0 + 4 + w/2, y0 + 5 + h/2), 5)

    else :
      (rectColor, rectOutlineColor, _) = noteObj.getNoteColor()
      pygame.draw.polygon(screenInst, rectColor, rect)

      # Draw the rectangle outline
      for i in range(4) :
        pygame.draw.line(screenInst, rectOutlineColor, (rect[i][0], rect[i][1]), (rect[(i+1) % 4][0], rect[(i+1) % 4][1]), 1)

      # Show finger number
      if (noteObj.finger in [1,2,3,4,5]) :
        # Font size 1
        #fu.renderText(screenInst, str(finger), (x0+10,y0+23), 1, self.fingerFontWhiteNoteRGB)
        
        # Font size 2
        fu.renderText(screenInst, str(noteObj.finger), (x0+7, y0+19), 2, self.fingerFontWhiteNoteRGB)



  # ---------------------------------------------------------------------------
  # METHOD <_singleHandBlackKeyPress> (private)
  #
  # Show a given black note on the keyboard as pressed.
  # ---------------------------------------------------------------------------
  def _singleHandBlackKeyPress(self, screenInst, noteObj) :

    # Build the rectangle that will be drawn on top of the note
    eps = 2
    u = [x[0] for x in self.keyboardPolygons[noteObj.pitch]]
    x0 = min(u); y0 = self.y + 50
    h = self.c - self.e - (2*eps) - 50
    w = self.d - (2*self.e) - (2*eps)
    rect = [(x0 + eps, y0 + eps)]
    rect += utils.Vector2D(0, h)
    rect += utils.Vector2D(w,0)
    rect += utils.Vector2D(0,-h)

    # Notes played from the MIDI keyboard have a different shape
    if (noteObj.fromKeyboardInput) :
      #pygame.draw.polygon(screenInst, self.sqWhiteNoteNeutralRGB, sq)
      pygame.draw.circle(screenInst, (200, 200, 200), (x0 + 2 + w/2, y0 + 1 + h/2), 5)

    else :
      (rectColor, rectOutlineColor, _) = noteObj.getNoteColor()
      pygame.draw.polygon(screenInst, rectColor, rect)

      # Draw the rectangle outline
      for i in range(4) :
        pygame.draw.line(screenInst, rectOutlineColor, (rect[i][0], rect[i][1]), (rect[(i+1) % 4][0], rect[(i+1) % 4][1]), 1)

      # Show finger number
      if (noteObj.finger in [1,2,3,4,5]) :
        # Font size 1
        #fu.renderText(screenInst, str(noteObj.finger), (x0+3, y0+23), 1, self.fingerFontBlackNoteRGB)
        
        # Font size 2
        fu.renderText(screenInst, str(noteObj.finger), (x0+1, y0+19), 2, self.fingerFontBlackNoteRGB)



  # ---------------------------------------------------------------------------
  # METHOD <_doubleHandWhiteKeyPress> (private)
  #
  # Show a given black note on the keyboard as pressed.
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
  def isActiveNoteClicked(self, clickCoord) :
    
    candidates = []
    (clickX, clickY) = clickCoord

    for (currLitNotePolygon, currNote) in self.litKeysPolygons :  
      if Point(clickX, clickY).within(Polygon(currLitNotePolygon)) :        
        candidates.append(currNote)

    # Multiple candidates: quite possibly one is pressed, the others are sustained
    # Return the note that was pressed the most recently
    if (len(candidates) > 1) :
      candidates.sort(key = lambda x : -x.startTime)
      return candidates[0]

    # Only one candidate: return it
    elif (len(candidates) == 1) :
      return candidates[0]
    
    # This click hit none of the polygons shown
    else :
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


