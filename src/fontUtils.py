# -*- coding: utf-8 -*-
# =============================================================================
# Module name     : fontUtils
# File name       : fontUtils.py
# Purpose         : lib to show some fonts
# Author          : Quentin Biache
# Creation date   : September 22nd, 2023
# =============================================================================

# =============================================================================
# Imports 
# =============================================================================
import pygame



# =============================================================================
# Main code 
# =============================================================================
# Font design is based on old school calculators LCD
# Example at https://www.dafont.com/fr/pixelmix.font
#
# This one wouldn't be bad either, but requires some more work: https://www.dafont.com/fr/perfect-dos-vga-437.font

charPolygons = {}

charPolygons["0"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 1, 1],
  [1, 0, 1, 0, 1],
  [1, 1, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["1"] = [
  [0, 0, 1, 0, 0],
  [0, 1, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 1, 1, 0]
]

charPolygons["2"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

charPolygons["3"] = [
  [1, 1, 1, 1, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["4"] = [
  [0, 0, 0, 1, 0],
  [0, 0, 1, 1, 0],
  [0, 1, 0, 1, 0],
  [1, 0, 0, 1, 0],
  [1, 1, 1, 1, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0]
]

charPolygons["5"] = [
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 0],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["6"] = [
  [0, 0, 1, 1, 0],
  [0, 1, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["7"] = [
  [1, 1, 1, 1, 1],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0]
]

charPolygons["8"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["9"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 1],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 1, 0],
  [0, 1, 1, 0, 0]
]

charPolygons["A"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

charPolygons["B"] = [
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0]
]

charPolygons["C"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["D"] = [
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0]
]

charPolygons["E"] = [
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

charPolygons["F"] = [
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0]
]

charPolygons["G"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 1, 1, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 1]
]

charPolygons["H"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

charPolygons["I"] = [
  [0, 1, 1, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 1, 1, 0]
]

charPolygons["J"] = [
  [0, 0, 1, 1, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [1, 0, 0, 1, 0],
  [0, 1, 1, 0, 0]
]

charPolygons["K"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 1, 0],
  [1, 0, 1, 0, 0],
  [1, 1, 0, 0, 0],
  [1, 0, 1, 0, 0],
  [1, 0, 0, 1, 0],
  [1, 0, 0, 0, 1]
]

charPolygons["L"] = [
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

charPolygons["M"] = [
  [1, 0, 0, 0, 1],
  [1, 1, 0, 1, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

charPolygons["N"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 0, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 0, 1, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

charPolygons["O"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["P"] = [
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0]
]

charPolygons["Q"] = [
  [0, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 0, 1, 0],
  [0, 1, 1, 0, 1]
]

charPolygons["R"] = [
  [1, 1, 1, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 1, 1, 1, 0],
  [1, 0, 1, 0, 0],
  [1, 0, 0, 1, 0],
  [1, 0, 0, 0, 1]
]

charPolygons["S"] = [
  [0, 1, 1, 1, 1],
  [1, 0, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [0, 1, 1, 1, 0],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 0, 1],
  [1, 1, 1, 1, 0]
]

charPolygons["T"] = [
  [1, 1, 1, 1, 1],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0]
]

charPolygons["U"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 1, 1, 0]
]

charPolygons["V"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 0, 1, 0],
  [0, 1, 0, 1, 0],
  [0, 0, 1, 0, 0]
]

charPolygons["W"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 1, 0, 1],
  [1, 0, 1, 0, 1],
  [0, 1, 0, 1, 0]
]

charPolygons["X"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 1, 0],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1]
]

charPolygons["Y"] = [
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [1, 0, 0, 0, 1],
  [0, 1, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 1, 0, 0]
]

charPolygons["Z"] = [
  [1, 1, 1, 1, 1],
  [0, 0, 0, 0, 1],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [1, 0, 0, 0, 0],
  [1, 1, 1, 1, 1]
]

charPolygons[" "] = [
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0]
]

charPolygons["#"] = [
  [0, 0, 0, 0, 0],
  [0, 1, 0, 1, 0],
  [1, 1, 1, 1, 1],
  [0, 1, 0, 1, 0],
  [0, 1, 0, 1, 0],
  [1, 1, 1, 1, 1],
  [0, 1, 0, 1, 0]
]

charPolygons["("] = [
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 1, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 1, 0]
]

charPolygons[")"] = [
  [0, 1, 0, 0, 0],
  [0, 0, 1, 0, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 0, 1, 0],
  [0, 0, 1, 0, 0],
  [0, 1, 0, 0, 0]
]


def render(screenInst, string, loc, size, col = (40,50,60)) :
  x0 = loc[0]; y0 = loc[1]
  w = size; h = size

  for char in string :
    for l in charPolygons[char] :
      for c in l :
        if (c > 0) :
          p = [(x0, y0), (x0 + (w-1), y0), (x0 + (w-1), y0 + (h-1)), (x0, y0 + (h-1))]
          pygame.draw.polygon(screenInst, col, p)

        x0 += w
      
      x0 -= 5*w; y0 += h

    x0 += 6*w; y0 = loc[1]

