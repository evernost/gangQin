# -*- coding: utf-8 -*-
# =============================================================================
# Module name     : midiFileTest
# File name       : midiFileTest.py
# Purpose         : test d'exploitation de fichier MIDI
# Author          : Quentin Biache
# Creation date   : September 3rd, 2023
# =============================================================================

# Gestion MIDI
import mido 



# =============================================================================
# Ouverture du fichier
# =============================================================================
mid = mido.MidiFile("D:/recherche/projets/gangQin/Rachmaninoff_Piano_Concerto_No2_Op18.mid")
print("fichier ouvert")

# =============================================================================
# Lecture des métadata
# =============================================================================
numTracks = len(mid.tracks)

print(f"Nombre de pistes : {numTracks}")

# =============================================================================
# Génération d'un "piano roll"
# =============================================================================
track0 = mid.tracks[0]

pianoRoll = {}



currTime = 0

for msg in track0 :

  # Mise à jour de la date courante -------------------------------------------
  currTime += msg.time
  


  # Touche pressée ------------------------------------------------------------
  if (msg.type == 'note_on') and (msg.velocity > 0) :
    # print(f"[{currTime}] press: {msg.note}")
    
    # Initialisation du pianoroll pour la note si première occurence
    if not(msg.note in pianoRoll) :
      pianoRoll = pianoRoll | {msg.note : []}

    pianoRoll[msg.note].append([currTime, -1])  # la date de fin n'est pas encore connue
    
    
    
  # Touche relâchée -----------------------------------------------------------
  if ((msg.type == 'note_off') or ((msg.type == 'note_on') and (msg.velocity == 0))) :
    # print(f"[{currTime}] release: {msg.note}")
  
    # Pas impossible, mais chelou : une note est relâchée sans être pressée
    if not(msg.note in pianoRoll) :
      print("Bizarre.")
      pianoRoll = pianoRoll | {msg.note : []}

    pianoRoll[msg.note][-1][1] = currTime

  
print("fin")

