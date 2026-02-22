# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : Keyboard (inherited from Widget)
# File name     : keyboard.py
# File type     : Python script (Python 3)
# Purpose       : draws the keyboard displayed on screen
# Author        : QuBi (nitrogenium@outlook.fr)
# Creation date : Sunday, 8 Oct 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# EXTERNALS
# =============================================================================
from src.commons import *
import src.note as note
import src.text as text
import src.utils as utils
import src.widgets.widget as widget

# Standard libraries
import pygame
from shapely.geometry import Point, Polygon     # For point in polygon test



# =============================================================================
# CONSTANTS
# =============================================================================
# None.



# =============================================================================
# CLASS DEFINITION
# =============================================================================
class Keyboard(widget.Widget) :

  """
  KEYBOARD Object
  
  The Keyboard object is a Widget representing the keyboard on screen.

  It is in charge of:
  - drawing the actual keyboard (black and white notes)
  - highlighting the notes pressed by the user on his external MIDI keyboard
  - highlighting the notes that have to be played.

  The Keyboard class derives from the Widget class.
  """

  def __init__(self, top, loc) :
    
    # Call the Widget init method
    super().__init__(top, loc)

    # Name of the widget
    self.name = "keyboard"

    # Populated after calling "Keyboard._makePolygons()"
    self.polygons = []

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

    # Define shorthand notations
    self.c = KEYBOARD_BLACK_NOTE_HEIGHT
    self.d = KEYBOARD_BLACK_NOTE_WIDTH
    self.s = KEYBOARD_NOTE_CHANFER
    self.e = KEYBOARD_NOTE_SPACING
    self.x = self.loc[0]; self.y = self.loc[1]

    # TODO: add description
    self.litKeysPolygons = []

    # Generate polygons for all notes and store them in 'Keyboard.polygons'
    self._makePolygons()

    # List of notes currently pressed
    #self.activeNotes      = []
    self.activeNotesMIDI  = []
    self.activeNotesScore = []



  # ---------------------------------------------------------------------------
  # METHOD: Keyboard.render()
  # ---------------------------------------------------------------------------
  def render(self) -> None :
    """
    Draws the keyboard using the polygons generated for each note.
    This function is called every time the app renders a new frame.
    """

    # Render the keyboard
    for i in MIDI_CODE_GRAND_PIANO_RANGE :
      if ((i % 12) in MIDI_CODE_BLACK_NOTES_MOD12) :
        pygame.draw.polygon(self.top.screen, KEYBOARD_BLACK_NOTE_COLOR, self.polygons[i])
      else :
        pygame.draw.polygon(self.top.screen, KEYBOARD_WHITE_NOTE_COLOR, self.polygons[i])

    # Render the notes from the Score and from the keyboard input
    if (WIDGET_ID_SCORE in self.top.widgets) :
      self.litKeysPolygons = []
      self.activeNotesScore = self.top.widgets[WIDGET_ID_SCORE].getTeacherNotes()
      self._renderKeyPress(self.activeNotesScore)
      self._renderKeyPress(self.activeNotesMIDI)

    # Render the mouse cursor
    self._renderMouseArrow()
    


  # ---------------------------------------------------------------------------
  # METHOD Keyboard._renderMouseArrow()                               [PRIVATE]
  # ---------------------------------------------------------------------------
  def _renderMouseArrow(self) :
    """
    Changes the mouse cursor appearance when hovering over the notes.
    """

    (mouse_x, mouse_y) = pygame.mouse.get_pos()
  
    # TODO: get rid of the magic values, derive these values directly from the geometry
    if ((10 <= mouse_x <= 1310) and (300 <= mouse_y <= 450)) :  
      
      # TODO: 'detectedNotes' must contain active notes only (no sustained note)
      (isNoteHit, _) = self.clickHitTest((mouse_x, mouse_y))
      if isNoteHit :
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
      else :
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    else:
      pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



  # ---------------------------------------------------------------------------
  # METHOD Keyboard._renderKeyPress()                                 [PRIVATE]
  # ---------------------------------------------------------------------------
  def _renderKeyPress(self, notes) -> None :
    """
    Renders a keypress on the keyboard.
    
    The function takes a list of 'Note' objects as input.
    The rendering takes the note's attributes into account.
    """

    # Preprocess the list so that the earliest notes are drawn first.
    # This avoids the sustained notes to be drawn on top.
    notes.sort(key = lambda x: x.startTime)

    # # -----------------------------------
    # # Filter out notes with null duration
    # # -----------------------------------
    # # A bit of an oddity. I am still unsure as of why that might happen.
    # newNoteList = []
    # for noteObj in notes :
    #   if not(noteObj.fromKeyboardInput) :
    #     if (noteObj.startTime != noteObj.stopTime):
    #       newNoteList.append(noteObj)
    #     # else :
    #     #   print("[WARNING] Keyboard._renderKeyPress(): null duration note detected.")
    #   else :
    #     newNoteList.append(noteObj)
    # notes = newNoteList

    # -----------------------------
    # Detect "double-pressed" notes
    # -----------------------------
    # Occurs when the score requests to press a key by one finger of each hand.
    # In this case, only one note is rendered to limit the 'display noise'.
    # The other note is simply ignored.
    # TODO: optimise this function. The way it is currently done costs a lot.
    
    # noteListByPitch = [[] for _ in range(128)]
    # for (index, noteObj) in enumerate(notes) :
    #   if not(noteObj.sustained) :
    #     noteListByPitch[noteObj.pitch].append((index, noteObj))
      
    # for notesInPitch in noteListByPitch :

    #   # Note is hit exactly twice at the same time
    #   if (len(notesInPitch) == 2) :
        
    #     # noteObj1 = notesInPitch[0][1]
    #     # noteObj2 = notesInPitch[1][1]
    #     print("[WARNING] Double pressed note!")

        

    #   # Note is hit more than twice at the same time (!)
    #   if (len(notesInPitch) >= 3) :
    #     print("[WARNING] Odd score: that's a lot of fingers to press one single note *questionning emoji*")

    
    
    # --------------
    # "Normal" notes
    # --------------
    for noteObj in notes :

      self._renderSimpleKeyPress(self.top.screen, noteObj)

      # Store the polygons associated to the "teacher notes"
      # This makes the hitbox for click on the entire key
      if ((noteObj.hand == note.hand_T.LEFT) or (noteObj.hand == note.hand_T.RIGHT)) :
        self.litKeysPolygons.append((self.polygons[noteObj.pitch], noteObj))



  # ---------------------------------------------------------------------------
  # METHOD Keyboard._renderSimpleKeyPress()                           [PRIVATE]
  # ---------------------------------------------------------------------------
  def _renderSimpleKeyPress(self, screenInst, noteObj) :
    """
    Renders a keypress on a black note.

    Adapts the rendering if the note comes from the score or from the
    input keyboard ('fromKeyboardInput' attribute)
    """

    if (noteObj.keyColor == note.keyColor_T.WHITE_KEY) :
      eps = 3
      u = [x[0] for x in self.polygons[noteObj.pitch]]
      x0 = min(u); y0 = self.y + self.c + self.e
      h = KEYBOARD_WHITE_NOTE_HEIGHT - (self.c + self.e) - (2*eps)
      w = KEYBOARD_WHITE_NOTE_WIDTH - (2*self.e) - (2*eps)
      rect = [(x0 + eps, y0 + eps)]
      rect += utils.Vector2D(0, h)
      rect += utils.Vector2D(w, 0)
      rect += utils.Vector2D(0, -h)
    elif (noteObj.keyColor == note.keyColor_T.BLACK_KEY) :
      eps = 2
      u = [x[0] for x in self.polygons[noteObj.pitch]]
      x0 = min(u); y0 = self.y + 50
      h = self.c - self.e - (2*eps) - 50
      w = self.d - (2*self.e) - (2*eps)
      rect = [(x0 + eps, y0 + eps)]
      rect += utils.Vector2D(0, h)
      rect += utils.Vector2D(w,0)
      rect += utils.Vector2D(0,-h)
    else :
      pass

    # Notes played from the MIDI keyboard have a different shape
    if (noteObj.fromKeyboardInput) :
      if (noteObj.keyColor == note.keyColor_T.WHITE_KEY) :
        pygame.draw.circle(screenInst, (10, 10, 10), (x0 + 4 + w/2, y0 + 5 + h/2), 5)
      elif (noteObj.keyColor == note.keyColor_T.BLACK_KEY) :
        pygame.draw.circle(screenInst, (200, 200, 200), (x0 + 2 + w/2, y0 + 1 + h/2), 5)
      else : 
        pass

    else :
      (rectColor, rectOutlineColor, _) = noteObj.getNoteColor()
      pygame.draw.polygon(screenInst, rectColor, rect)

      # Draw the rectangle outline
      for i in range(4) :
        pygame.draw.line(screenInst, rectOutlineColor, (rect[i][0], rect[i][1]), (rect[(i+1) % 4][0], rect[(i+1) % 4][1]), 1)

      # Show finger number
      if (noteObj.finger != note.finger_T.UNDEFINED) :
        
        if (noteObj.keyColor == note.keyColor_T.WHITE_KEY) :
          text.render(screenInst, str(noteObj.finger.value), (x0+7, y0+19), 2, KEYBOARD_FINGERSATZ_FONT_COLOR_BLACK_NOTE)
        elif (noteObj.keyColor == note.keyColor_T.BLACK_KEY) :
          text.render(screenInst, str(noteObj.finger.value), (x0+1, y0+19), 2, KEYBOARD_FINGERSATZ_FONT_COLOR_WHITE_NOTE)
        else :
          pass


  
  # # ---------------------------------------------------------------------------
  # # METHOD Keyboard._singleHandWhiteKeyPress()                        [PRIVATE]
  # # ---------------------------------------------------------------------------
  # def _singleHandWhiteKeyPress(self, screenInst, noteObj) :
  #   """
  #   Renders a keypress on a white note.

  #   Adapts the rendering if the note comes from the score or from the
  #   input keyboard ('fromKeyboardInput' attribute)
  #   """

  #   # Build the little rectangle drawn on top of the note, to show that it is 
  #   # pressed.
  #   eps = 3
  #   u = [x[0] for x in self.polygons[noteObj.pitch]]
  #   x0 = min(u); y0 = self.y + self.c + self.e
  #   h = KEYBOARD_WHITE_NOTE_HEIGHT - (self.c + self.e) - (2*eps)
  #   w = KEYBOARD_WHITE_NOTE_WIDTH - (2*self.e) - (2*eps)
  #   rect = [(x0 + eps, y0 + eps)]
  #   rect += utils.Vector2D(0, h)
  #   rect += utils.Vector2D(w, 0)
  #   rect += utils.Vector2D(0, -h)
    
  #   # Notes played from the MIDI keyboard have a different shape
  #   if (noteObj.fromKeyboardInput) :
  #     #pygame.draw.polygon(screenInst, self.sqWhiteNoteNeutralRGB, sq)
  #     pygame.draw.circle(screenInst, (10, 10, 10), (x0 + 4 + w/2, y0 + 5 + h/2), 5)

  #   else :
  #     (rectColor, rectOutlineColor, _) = noteObj.getNoteColor()
  #     pygame.draw.polygon(screenInst, rectColor, rect)

  #     # Draw the rectangle outline
  #     for i in range(4) :
  #       pygame.draw.line(screenInst, rectOutlineColor, (rect[i][0], rect[i][1]), (rect[(i+1) % 4][0], rect[(i+1) % 4][1]), 1)

  #     # Show finger number
  #     if (noteObj.finger != note.finger_T.UNDEFINED) :
  #       # Font size 1
  #       #text.render(screenInst, str(finger), (x0+10,y0+23), 1, self.fingerFontWhiteNoteRGB)
        
  #       # Font size 2
  #       text.render(screenInst, str(noteObj.finger.value), (x0+7, y0+19), 2, KEYBOARD_FINGERSATZ_FONT_COLOR_BLACK_NOTE)



  # # ---------------------------------------------------------------------------
  # # METHOD Keyboard._singleHandBlackKeyPress()                        [PRIVATE]
  # # ---------------------------------------------------------------------------
  # def _singleHandBlackKeyPress(self, screenInst, noteObj) :
  #   """
  #   Renders a keypress on a black note.

  #   Adapts the rendering if the note comes from the score or from the
  #   input keyboard ('fromKeyboardInput' attribute)
  #   """

  #   # Build the rectangle that will be drawn on top of the note
  #   eps = 2
  #   u = [x[0] for x in self.polygons[noteObj.pitch]]
  #   x0 = min(u); y0 = self.y + 50
  #   h = self.c - self.e - (2*eps) - 50
  #   w = self.d - (2*self.e) - (2*eps)
  #   rect = [(x0 + eps, y0 + eps)]
  #   rect += utils.Vector2D(0, h)
  #   rect += utils.Vector2D(w,0)
  #   rect += utils.Vector2D(0,-h)

  #   # Notes played from the MIDI keyboard have a different shape
  #   if (noteObj.fromKeyboardInput) :
  #     #pygame.draw.polygon(screenInst, self.sqWhiteNoteNeutralRGB, sq)
  #     pygame.draw.circle(screenInst, (200, 200, 200), (x0 + 2 + w/2, y0 + 1 + h/2), 5)

  #   else :
  #     (rectColor, rectOutlineColor, _) = noteObj.getNoteColor()
  #     pygame.draw.polygon(screenInst, rectColor, rect)

  #     # Draw the rectangle outline
  #     for i in range(4) :
  #       pygame.draw.line(screenInst, rectOutlineColor, (rect[i][0], rect[i][1]), (rect[(i+1) % 4][0], rect[(i+1) % 4][1]), 1)

  #     # Show finger number
  #     if (noteObj.finger != note.finger_T.UNDEFINED) :
  #       # Font size 1
  #       #text.render(screenInst, str(noteObj.finger), (x0+3, y0+23), 1, self.fingerFontBlackNoteRGB)
        
  #       # Font size 2
  #       text.render(screenInst, str(noteObj.finger), (x0+1, y0+19), 2, KEYBOARD_FINGERSATZ_FONT_COLOR_WHITE_NOTE)



  # ---------------------------------------------------------------------------
  # METHOD <_doubleHandWhiteKeyPress> (private)
  #
  # Show a given black note on the keyboard as pressed.
  # ---------------------------------------------------------------------------
  def _doubleHandWhiteKeyPress(self, screenInst, noteObj) :

    # Build the rectangle that will be drawn on top of the note
    eps = 3
    u = [x[0] for x in self.polygons[noteObj.pitch]]
    x0 = min(u); y0 = self.y + self.c + self.e
    h = KEYBOARD_WHITE_NOTE_HEIGHT - (self.c + self.e) - (2*eps)
    w = KEYBOARD_WHITE_NOTE_WIDTH - (2*self.e) - (2*eps)
    
    rectLeft = [(x0 + eps, y0 + eps)]
    rectLeft += utils.Vector2D(0, h)
    rectLeft += utils.Vector2D(w-eps, -h)

    rectRight = [(x0 + eps + w, y0 + eps)]
    rectRight += utils.Vector2D(0, h)
    rectRight += utils.Vector2D(-w+eps,0)
    
    if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
      pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapLeftRGB, rectLeft)
    else :
      pygame.draw.polygon(screenInst, KEYBOARD_PLAY_RECT_COLOR_LEFT_HAND_WHITE_NOTE, rectLeft)
    
    if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
      pygame.draw.polygon(screenInst, self.sqWhiteNoteOverlapRightRGB, rectRight)
    else :
      pygame.draw.polygon(screenInst, KEYBOARD_PLAY_RECT_COLOR_RIGHT_HAND_WHITE_NOTE, rectRight)

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
    u = [x[0] for x in self.polygons[noteObj.pitch]]
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
      pygame.draw.polygon(screenInst, KEYBOARD_PLAY_RECT_COLOR_LEFT_HAND_BLACK_NOTE, rectLeft)
    
    if (noteObj.pitch in [x.pitch for x in self.activeNotes]) :
      pygame.draw.polygon(screenInst, self.sqBlackNoteOverlapRightRGB, rectRight)
    else :
      pygame.draw.polygon(screenInst, KEYBOARD_PLAY_RECT_COLOR_RIGHT_HAND_BLACK_NOTE, rectRight)

    # Show finger number
    # TODO


  
  # ---------------------------------------------------------------------------
  # METHOD Keyboard.clickHitTest
  # ---------------------------------------------------------------------------
  def clickHitTest(self, coord) :
    """
    Detects if the click's coordinates are in the hitbox of an active note.
    
    Returns (status, Note) where 'status' is the test result (True/False) and 
    'N' the note object hit (or 'None' if nothing is hit)
    """

    candidates = []
    (x,y) = coord
    for (currLitNotePolygon, currNote) in self.litKeysPolygons :
      if Point(x, y).within(Polygon(currLitNotePolygon)) :
        candidates.append(currNote)

    # Multiple candidates: quite possibly one is pressed, the others are sustained
    # Return the note that was pressed the most recently
    if (len(candidates) > 1) :
      candidates.sort(key = lambda x : -x.startTime)
      return (True, candidates[0])

    # Only one candidate: return it
    elif (len(candidates) == 1) :
      return (True, candidates[0])
    
    # The click didn't hit any active note
    else :
      return (False, None)



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



  # ---------------------------------------------------------------------------
  # METHOD: Keyboard.onExternalMidiEvent()
  # ---------------------------------------------------------------------------
  def onExternalMidiEvent(self, midiMessage) :
    """
    Updates the list of active MIDI notes coming from the keyboard so that 
    they can be displayed at rendering.
    """

    if (midiMessage.type == "note_on") :
      N = note.Note(midiMessage.note)
      N.fromKeyboardInput = True
      self.activeNotesMIDI.append(N)
      
    elif (midiMessage.type == "note_off") :
      self.activeNotesMIDI = [N for N in self.activeNotesMIDI if (N.pitch != midiMessage.note)]



  # ---------------------------------------------------------------------------
  # METHOD: Keyboard._makePolygons()                                  [PRIVATE]
  # ---------------------------------------------------------------------------
  def _makePolygons(self, grandPianoMode = True) :
    """
    Generates the polygons drawing the notes of a full MIDI keyboard 
    (i.e. 128 notes)
    
    If 'grandPianoMode' is set to True, polygon generation is restricted to 
    the notes of a grand piano (i.e. from A0 to C8).

    This function populates the attribute 'polygons'. 
    It is a 128 elements array, such that 'polygons[i]' is an array
    containing the vertices required to draw the note with MIDI code 'i'.

    This function only needs to be called once at init.
    """

    # Initialise output
    self.polygons = [[] for _ in range(128)]

    # Some shortcuts for readability
    wnh = KEYBOARD_WHITE_NOTE_HEIGHT
    wnw = KEYBOARD_WHITE_NOTE_WIDTH
    bnh = KEYBOARD_BLACK_NOTE_HEIGHT 
    bnw = KEYBOARD_BLACK_NOTE_WIDTH
    nc = KEYBOARD_NOTE_CHANFER
    ns = KEYBOARD_NOTE_SPACING

    x0 = self.x - (12*wnw); y0 = self.y

    # Generate polygons for each note
    for i in range(0, 128, 12) :
      
      # Note C
      if (grandPianoMode and (i == 108)) :
        self.polygons[i] = [(x0+ns, y0)]
        self.polygons[i] += utils.Vector2D(0, wnh-nc)
        self.polygons[i] += utils.Vector2D(nc, nc)
        self.polygons[i] += utils.Vector2D(wnw-(2*nc)-(2*ns), 0)
        self.polygons[i] += utils.Vector2D(nc, -nc)
        self.polygons[i] += utils.Vector2D(0, -(wnh-nc))
      else :
        self.polygons[i] = [(x0+ns, y0)]
        self.polygons[i] += utils.Vector2D(0, wnh-nc)
        self.polygons[i] += utils.Vector2D(nc, nc)
        self.polygons[i] += utils.Vector2D(wnw-(2*nc)-(2*ns), 0)
        self.polygons[i] += utils.Vector2D(nc, -nc)
        self.polygons[i] += utils.Vector2D(0, -(wnh-bnh-ns-nc))
        self.polygons[i] += utils.Vector2D(-2*bnw//3, 0)
        self.polygons[i] += utils.Vector2D(0, -(bnh+ns))

      # Note Db
      self.polygons[i+1] = [(x0+wnw-(2*bnw//3)+ns, y0)]
      self.polygons[i+1] += utils.Vector2D(0, bnh-ns)
      self.polygons[i+1] += utils.Vector2D(bnw-(2*ns), 0)
      self.polygons[i+1] += utils.Vector2D(0, -(bnh-ns))

      # Note D
      self.polygons[i+2] = [(x0+wnw+(bnw//3)+ns, y0)]
      self.polygons[i+2] += utils.Vector2D(0, bnh+ns)
      self.polygons[i+2] += utils.Vector2D(-bnw//3, 0)
      self.polygons[i+2] += utils.Vector2D(0, wnh-bnh-ns-nc)
      self.polygons[i+2] += utils.Vector2D(nc,nc)
      self.polygons[i+2] += utils.Vector2D(wnw-(2*nc)-(2*ns),0)
      self.polygons[i+2] += utils.Vector2D(nc,-nc)
      self.polygons[i+2] += utils.Vector2D(0,-(wnh-bnh-ns-nc))
      self.polygons[i+2] += utils.Vector2D(-bnw//3,0)
      self.polygons[i+2] += utils.Vector2D(0,-(bnh+ns))

      # Note Eb
      self.polygons[i+3] = [(x0+(2*wnw)-(bnw//3)+ns, y0)]
      self.polygons[i+3] += utils.Vector2D(0,bnh-ns)
      self.polygons[i+3] += utils.Vector2D(bnw-(2*ns),0)
      self.polygons[i+3] += utils.Vector2D(0,-(bnh-ns))

      # Note E
      self.polygons[i+4] = [(x0+(2*wnw)+(2*bnw//3)+ns, y0)]
      self.polygons[i+4] += utils.Vector2D(0,bnh+ns)
      self.polygons[i+4] += utils.Vector2D(-2*bnw//3,0)
      self.polygons[i+4] += utils.Vector2D(0,wnh-bnh-ns-nc)
      self.polygons[i+4] += utils.Vector2D(nc,nc)
      self.polygons[i+4] += utils.Vector2D(wnw-(2*nc)-(2*ns),0)
      self.polygons[i+4] += utils.Vector2D(nc,-nc)
      self.polygons[i+4] += utils.Vector2D(0,-(wnh-nc))

      # Note F
      self.polygons[i+5] = [(x0+(3*wnw)+ns, y0)]
      self.polygons[i+5] += utils.Vector2D(0,wnh-nc)
      self.polygons[i+5] += utils.Vector2D(nc,nc)
      self.polygons[i+5] += utils.Vector2D(wnw-(2*nc)-(2*ns),0)
      self.polygons[i+5] += utils.Vector2D(nc,-nc)
      self.polygons[i+5] += utils.Vector2D(0,-(wnh-bnh-ns-nc))
      self.polygons[i+5] += utils.Vector2D(-2*bnw//3,0)
      self.polygons[i+5] += utils.Vector2D(0,-(bnh+ns))

      # Note Gb
      self.polygons[i+6] = [(x0+(4*wnw)-(2*bnw//3)+ns, y0)]
      self.polygons[i+6] += utils.Vector2D(0,bnh-ns)
      self.polygons[i+6] += utils.Vector2D(bnw-(2*ns),0)
      self.polygons[i+6] += utils.Vector2D(0,-(bnh-ns))

      # Note G
      self.polygons[i+7] = [(x0+(4*wnw)+(bnw//3)+ns, y0)]
      self.polygons[i+7] += utils.Vector2D(0,bnh+ns)
      self.polygons[i+7] += utils.Vector2D(-bnw//3,0)
      self.polygons[i+7] += utils.Vector2D(0,wnh-bnh-ns-nc)
      self.polygons[i+7] += utils.Vector2D(nc,nc)
      self.polygons[i+7] += utils.Vector2D(wnw-(2*nc)-(2*ns),0)
      self.polygons[i+7] += utils.Vector2D(nc,-nc)
      self.polygons[i+7] += utils.Vector2D(0,-(wnh-bnh-ns-nc))
      self.polygons[i+7] += utils.Vector2D(-bnw//2,0)
      self.polygons[i+7] += utils.Vector2D(0,-(bnh+ns))

      if ((i+8) < 127) :

        # Note Ab
        self.polygons[i+8] = [(x0+(5*wnw)-(bnw//2)+ns, y0)]
        self.polygons[i+8] += utils.Vector2D(0,bnh-ns)
        self.polygons[i+8] += utils.Vector2D(bnw-(2*ns),0)
        self.polygons[i+8] += utils.Vector2D(0,-(bnh-ns))

        # Note A
        if (grandPianoMode and ((i+9) == 21)) :
          self.polygons[i+9] = [(x0+(5*wnw)+ns, y0)]
          self.polygons[i+9] += utils.Vector2D(0,wnh-nc)
          self.polygons[i+9] += utils.Vector2D(nc,nc)
          self.polygons[i+9] += utils.Vector2D(wnw-(2*nc)-(2*ns),0)
          self.polygons[i+9] += utils.Vector2D(nc,-nc)
          self.polygons[i+9] += utils.Vector2D(0,-(wnh-bnh-ns-nc))
          self.polygons[i+9] += utils.Vector2D(-bnw//3,0)
          self.polygons[i+9] += utils.Vector2D(0,-(bnh+ns))
        else :
          self.polygons[i+9] = [(x0+(5*wnw)+(bnw//2)+ns, y0)]
          self.polygons[i+9] += utils.Vector2D(0, bnh+ns)
          self.polygons[i+9] += utils.Vector2D(-bnw//2, 0)
          self.polygons[i+9] += utils.Vector2D(0, wnh-bnh-ns-nc)
          self.polygons[i+9] += utils.Vector2D(nc,nc)
          self.polygons[i+9] += utils.Vector2D(wnw-(2*nc)-(2*ns), 0)
          self.polygons[i+9] += utils.Vector2D(nc, -nc)
          self.polygons[i+9] += utils.Vector2D(0, -(wnh-bnh-ns-nc))
          self.polygons[i+9] += utils.Vector2D(-bnw//3, 0)
          self.polygons[i+9] += utils.Vector2D(0,-(bnh+ns))

        # Note Bb
        self.polygons[i+10] = [(x0+(6*wnw)-(bnw//3)+ns, y0)]
        self.polygons[i+10] += utils.Vector2D(0,bnh-ns)
        self.polygons[i+10] += utils.Vector2D(bnw-(2*ns),0)
        self.polygons[i+10] += utils.Vector2D(0,-(bnh-ns))

        # Note B
        self.polygons[i+11] = [(x0+(6*wnw)+(2*bnw//3)+ns, y0)]
        self.polygons[i+11] += utils.Vector2D(0,bnh+ns)
        self.polygons[i+11] += utils.Vector2D(-2*bnw//3,0)
        self.polygons[i+11] += utils.Vector2D(0,wnh-bnh-ns-nc)
        self.polygons[i+11] += utils.Vector2D(nc,nc)
        self.polygons[i+11] += utils.Vector2D(wnw-(2*nc)-(2*ns),0)
        self.polygons[i+11] += utils.Vector2D(nc,-nc)
        self.polygons[i+11] += utils.Vector2D(0,-(wnh-nc))

      x0 += 7*wnw




# =============================================================================
# UNIT TESTS
# =============================================================================
if (__name__ == "__main__") :
  print("[INFO] There are no unit tests available for 'keyboard.py'.")


