# -*- coding: utf-8 -*-
# =============================================================================
# Module name   : text
# File name     : text.py
# Purpose       : provides text printing features in a Pygame window.
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Friday, 22 Sept 2023
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# External libs
# =============================================================================
# Project specific constants
from src.commons import *

import pygame



# =============================================================================
# Guards
# =============================================================================
if (__name__ == "__main__") :
  print("[WARNING] This lib is not intended to be called as a main.")



# =============================================================================
# Constants pool
# =============================================================================
LEFT_JUSTIFY = 0
RIGHT_JUSTIFY = 1


# Font design is based on old school calculators LCD
# Example at https://www.dafont.com/fr/pixelmix.font

# This one wouldn't be bad either, but requires some more work: https://www.dafont.com/fr/perfect-dos-vga-437.font

CHAR_POLYGONS = {}

CHAR_POLYGONS["0"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 1, 1],
  [1, 0, 1, 0, 1],
  [1, 1, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["1"] = [
  [0, 0, 1, 0, 0],
  [0, 1, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["2"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

CHAR_POLYGONS["3"] = [
  [1, 1, 1, 1, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["4"] = [
  [0, 0, 0, 1, 0],
  [0, 0, 1, 1, 0],
  [0, 1, 0, 1, 0],
  [1, 0, 0, 1, 0],
  [1, 1, 1, 1, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0]
]

CHAR_POLYGONS["5"] = [
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 0],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["6"] = [
  [0, 0, 1, 1, 0],
  [0, 1, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["7"] = [
  [1, 1, 1, 1, 1],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0]
]

CHAR_POLYGONS["8"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["9"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 1],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 1, 0],
  [0, 1, 1, 0, 0]
]

CHAR_POLYGONS["A"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

CHAR_POLYGONS["B"] = [
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0]
]

CHAR_POLYGONS["C"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["D"] = [
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0]
]

CHAR_POLYGONS["E"] = [
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

CHAR_POLYGONS["F"] = [
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0]
]

CHAR_POLYGONS["G"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 1, 1, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 1]
]

CHAR_POLYGONS["H"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

CHAR_POLYGONS["I"] = [
  [0, 1, 1, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["J"] = [
  [0, 0, 1, 1, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [1, 0, 0, 1, 0],
  [0, 1, 1, 0, 0]
]

CHAR_POLYGONS["K"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 1, 0],
  [1, 0, 1, 0, 0],
  [1, 1, 0, 0, 0],
  [1, 0, 1, 0, 0],
  [1, 0, 0, 1, 0],
  [1, 0, 0, 0, 1]
]

CHAR_POLYGONS["L"] = [
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

CHAR_POLYGONS["M"] = [
  [1, 0, 0, 0, 1],
  [1, 1, 0, 1, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

CHAR_POLYGONS["N"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 0, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 0, 1, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

CHAR_POLYGONS["O"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["P"] = [
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0]
]

CHAR_POLYGONS["Q"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 0, 1, 0],
  [0, 1, 1, 0, 1]
]

CHAR_POLYGONS["R"] = [
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0],
  [1, 0, 1, 0, 0],
  [1, 0, 0, 1, 0],
  [1, 0, 0, 0, 1]
]

CHAR_POLYGONS["S"] = [
  [0, 1, 1, 1, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [0, 1, 1, 1, 0],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 0, 1],
  [1, 1, 1, 1, 0]
]

CHAR_POLYGONS["T"] = [
  [1, 1, 1, 1, 1],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0]
]

CHAR_POLYGONS["U"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

CHAR_POLYGONS["V"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 0, 1, 0],
  [0, 1, 0, 1, 0],
  [0, 0, 1, 0, 0]
]

CHAR_POLYGONS["W"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1],
  [0, 1, 0, 1, 0]
]

CHAR_POLYGONS["X"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

CHAR_POLYGONS["Y"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0]
]

CHAR_POLYGONS["Z"] = [
  [1, 1, 1, 1, 1],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

CHAR_POLYGONS[" "] = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]
]

CHAR_POLYGONS["#"] = [
  [0, 0, 0, 0, 0],
  [0, 1, 0, 1, 0],
  [1, 1, 1, 1, 1],
  [0, 1, 0, 1, 0],
  [0, 1, 0, 1, 0],
  [1, 1, 1, 1, 1],
  [0, 1, 0, 1, 0]
]

CHAR_POLYGONS["("] = [
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 1, 0]
]

CHAR_POLYGONS[")"] = [
  [0, 1, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0]
]

CHAR_POLYGONS[":"] = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0]
]

CHAR_POLYGONS["/"] = [
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0]
]

CHAR_POLYGONS["?"] = [
  [0, 1, 1, 0, 0],
  [1, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 1, 0, 0, 0]
]

CHAR_POLYGONS["-"] = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [1, 1, 1, 1, 1],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]
]

CHAR_POLYGONS["_"] = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

CHAR_POLYGONS["."] = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 1, 1, 0, 0],
  [0, 1, 1, 0, 0]
]

CHAR_POLYGONS[","] = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 1, 1, 0, 0],
  [0, 0, 1, 0, 0]
]

CHAR_POLYGONS[";"] = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 1, 1, 0, 0],
  [0, 0, 1, 0, 0]
]

CHAR_POLYGONS["["] = [
  [0, 1, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 1, 0, 0]
]

CHAR_POLYGONS["]"] = [
  [0, 0, 1, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 1, 0]
]

# -----------------------------------------------------------------------------
# METHOD render
# -----------------------------------------------------------------------------
def render(screenInst, string, loc, size, col = (40, 50, 60), justify = LEFT_JUSTIFY) :
  """
  Prints a string on a pygame screen.
  - "size" (int): each element of charPolygon is drawn as a square of pixel
    This arguments defines the size of each square (in pixels)
  - "col" = (R,G,B): text color in RGB values
  
  In LEFT_JUSTIFY mode, the text starts at the coordinate pointed by 'loc'.
  In RIGHT_JUSTIFY mode, the text ends at the coordinate pointed by 'loc'.
  Default is LEFT_JUSTIFY mode.
  """
  x0 = loc[0]; y0 = loc[1]
  w = size; h = size

  if (justify == RIGHT_JUSTIFY) :
    x0 = x0 - 6*w*len(string)

  for char in string :
    for l in CHAR_POLYGONS[char] :
      for c in l :
        if (c > 0) :
          squareCoord = [(x0, y0), (x0 + (w-1), y0), (x0 + (w-1), y0 + (h-1)), (x0, y0 + (h-1))]
          pygame.draw.polygon(screenInst, col, squareCoord)

        x0 += w
      
      x0 -= 5*w; y0 += h

    x0 += 6*w; y0 = loc[1]



# -----------------------------------------------------------------------------
# METHOD renderPlus
# -----------------------------------------------------------------------------
def renderPlus(screenInst, string, colorSpec, colorDict, formatSpec, loc, size, justify = LEFT_JUSTIFY) :
  """
  Improved version of "render", with format specifiers.
  """

  x0 = loc[0]; y0 = loc[1]
  w = size; h = size

  if (justify == RIGHT_JUSTIFY) :
    x0 = x0 - 6*w*len(string)

  # Loop on the characters in the string
  for (i, char) in enumerate(string) :
    cS    = colorSpec[i]
    color = colorDict[cS]
    
    # Draw the character
    for (y,charLine) in enumerate(CHAR_POLYGONS[char]) :
      for (x,pixel) in enumerate(charLine) :
        
        # Strike line: combine the char with "/"
        # TODO
        
        if (pixel > 0) :
          squareCoord = [(x0, y0), (x0 + (w-1), y0), (x0 + (w-1), y0 + (h-1)), (x0, y0 + (h-1))]
          pygame.draw.polygon(screenInst, color, squareCoord)
        x0 += w
      
      # CR/LF
      x0 -= 5*w; y0 += h

    # Draw the underline
    if (formatSpec[i] == "_") :
      y0 += h
      for pixel in range(5) :
        squareCoord = [(x0, y0), (x0 + (w-1), y0), (x0 + (w-1), y0 + (h-1)), (x0, y0 + (h-1))]
        pygame.draw.polygon(screenInst, color, squareCoord)
        x0 += w
      
      # CR/LF
      x0 -= 5*w; y0 += h

    x0 += 6*w; y0 = loc[1]



# -----------------------------------------------------------------------------
# FUNCTION showCursor
# -----------------------------------------------------------------------------
def showCursor(screen, cursor, scoreLength) :
  render(screen, f"CURSOR: {cursor+1} / {scoreLength}", (12, 20), 2, GUI_TEXT_COLOR)



# -----------------------------------------------------------------------------
# FUNCTION showBookmark
# -----------------------------------------------------------------------------
def showBookmark(screen, bookmarkIndex) :
  if (bookmarkIndex != -1) :
    render(screen, f"BOOKMARK #{bookmarkIndex}", (10, 470), 2, GUI_TEXT_COLOR)



# -----------------------------------------------------------------------------
# FUNCTION showActiveHands
# -----------------------------------------------------------------------------
def showActiveHands(screen, activeHands) :
  render(screen, activeHands, (1288, 470), 2, GUI_TEXT_COLOR)



# -----------------------------------------------------------------------------
# FUNCTION showLoop
# -----------------------------------------------------------------------------
def showLoop(screen, loopEnable, loopStart, loopEnd, cursor) :
  if loopEnable :
    render(screen, f"LOOP: [{loopStart+1} ... {cursor+1} ... {loopEnd+1}]", (400, 20), 2, GUI_TEXT_COLOR)
  else :
    if (loopStart >= 0) :
      render(screen, f"LOOP: [{loopStart+1} ... {cursor+1} ... _]", (400, 20), 2, GUI_TEXT_COLOR)

    if (loopEnd >= 0) :
      render(screen, f"LOOP: [_  ... {cursor+1} ... {loopEnd+1}]", (400, 20), 2, GUI_TEXT_COLOR)



# -----------------------------------------------------------------------------
# FUNCTION showCombo
# -----------------------------------------------------------------------------
def showCombo(screen, comboCount, comboHighestSession, comboHighestAllTime) :
  render(screen, f"COMBO: {comboCount} (MAX: {comboHighestSession} / ALLTIME: {comboHighestAllTime})", (1312, 20), 2, GUI_TEXT_COLOR, justify = RIGHT_JUSTIFY)



# -----------------------------------------------------------------------------
# FUNCTION showMetronome
# -----------------------------------------------------------------------------
def showMetronome(screen, metronomeObj) :
  if metronomeObj.enable :
    render(screen, f"BPM:{metronomeObj.bpm} - {metronomeObj.num}/{metronomeObj.denom} - {metronomeObj.counter}", (950, 470), 2, GUI_TEXT_COLOR)



