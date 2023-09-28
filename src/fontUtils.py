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

# charPolygons["1"] = [
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0],
#   [0, 0, 0, 0, 0]
# ]

def render(screenInst, char, loc, size, col = (40,50,60)) :
  x0 = loc[0]; y0 = loc[1]
  w = size; h = size

  for l in charPolygons[char] :
    for c in l :
      if (c > 0) :
        p = [(x0, y0), (x0 + (w-1), y0), (x0 + (w-1), y0 + (h-1)), (x0, y0 + (h-1))]
        pygame.draw.polygon(screenInst, col, p)

      x0 += w
    
    x0 = loc[0]; y0 += h


