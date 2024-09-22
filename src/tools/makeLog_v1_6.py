# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : makeLogTool_v1_6
# File name     : makeLogTool_v1_6.py
# Purpose       : build a .log file from an old school .pr file
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Sunday, 22 September 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================

# =============================================================================
# Description
# =============================================================================
# Starting from revision 1.6, the playing statistics in gangQin have ceased to 
# be stored in the score file (.pr) and are stored in a separate file (.log)
# 
# The reason being that the playing statistics are specific to a user whereas
# the score is 'universal'. Having performance data in a score made little 
# sense.
#
# For all scores saved in version 1.5 and below, this tool can be used to 
# extract the performance information to a proper .log file.
#
# HOW TO USE IT
# Run this script. 
# A window will show to ask you to select the files you wish to process
# (you can select 1 or several files)
# Logs will be automatically generated in the ./logs folder.
#
# NOTES
# - there are no adverse consequences in case you keep using old school .pr
#   files with newer versions of gangQin (1.6 and above)
#   It still works, but the statistics in the .pr will not be updated.
#   Besides, a .log file will be created anyway, but statistics will be reset.
# - after using this tool, the statistics in the .pr file will be deleted.
# - if there are existing .log files already, the tool will not overwrite them.



# =============================================================================
# External libs 
# =============================================================================
import json
import os
import tkinter as tk
from tkinter import filedialog



# =============================================================================
# Constants pool
# =============================================================================
LOG_DIR = "./logs"
LOG_OVERWRITE_OUTPUT = True



# =============================================================================
# Main code
# =============================================================================
root = tk.Tk()
root.withdraw()

print("[NOTE] Please select the .pr file(s) you wish to extract the statistics from...")
pianoRollFiles = filedialog.askopenfilenames(
    title = "Select one or more .pr file(s)",
    initialdir = "./songs",
    filetypes = (("gangQin piano roll file (.pr)", "*.pr"), ("All files", "*.*"))
)

# No file selected!
nFiles = len(pianoRollFiles)
if (nFiles == 0) :
  print("[NOTE] No file selected, exiting...")
  exit()
print("")

if not os.path.exists(LOG_DIR):
  os.mkdir(LOG_DIR)

# Loop on the .pr files
for (i, pr) in enumerate(pianoRollFiles) :

  (rootDir, rootNameExt) = os.path.split(pr)
  (rootName, _) = os.path.splitext(rootNameExt)
  



  print(f"- Processing file ({i+1}/{nFiles}): '{rootName}'")
  with open(pr, "r") as jsonFile:
    data = json.load(jsonFile)

  if ("statsCursor" in data.keys()) :
    data_statsCursor = data["statsCursor"]
  else :
    print("[WARNING] No statistics found (possibly a very old .pr file)")
    data_statsCursor = []
  
  scoreLength = len(data_statsCursor)
  print(f"File revision: {data['revision']}")
  print(f"Score length : {scoreLength}")
  
  
  
  targetDict = {}

  targetDict["scoreLength"] = scoreLength

  if ("sessionCount" in data.keys()) :
    targetDict["sessionCount"] = data["sessionCount"]
  else :
    targetDict["sessionCount"] = 0
  
  if ("sessionLog" in data.keys()) :
    targetDict["sessionLog"] = data["sessionLog"]
  else :
    targetDict["sessionLog"] = []

  if ("sessionTotalPracticeTime" in data.keys()) :
    targetDict["totalPracticeTimeSec"] = data["sessionTotalPracticeTime"]
  else :
    targetDict["totalPracticeTimeSec"] = 0

  targetDict["comboHighestAllTime"] = data["comboHighestAllTime"]

  targetDict["cursorHistogram"]      = data_statsCursor
  targetDict["cursorWrongNoteCount"] = [0 for _ in range(scoreLength)]

  logFile = os.path.join(".", "logs", rootName + ".log")
  if (not(os.path.exists(logFile)) or (os.path.exists(logFile) and LOG_OVERWRITE_OUTPUT)) :
    with open(logFile, "w") as jsonFile :
      json.dump(targetDict, jsonFile, indent = 2)

    print(f"Log generated: '{logFile}'")
  else :
    print("[WARNING] A .log file already exists. To overwrite, please set 'LOG_OVERWRITE_OUTPUT' to True.")
    
  print("")
