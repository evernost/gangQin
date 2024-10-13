# -*- coding: utf-8 -*-
# =============================================================================
# Project       : gangQin
# Module name   : database
# File name     : database.py
# Purpose       : score capture database class
# Author        : QuBi (nitrogenium@hotmail.com)
# Creation date : Tuesday, 01 October 2024
# -----------------------------------------------------------------------------
# Best viewed with space indentation (2 spaces)
# =============================================================================






# =============================================================================
# External libs 
# =============================================================================
import json
import os
import random
import snapshot
import string



# =============================================================================
# Constants pool
# =============================================================================



# =============================================================================
# Main code
# =============================================================================
class Database :
  def __init__(self, prFile) :
    
    self.nSnapshots = 0
    self.snapshots = []
    self.isEmpty = True
    
    self.songName = ""      # Name of the song file
    self.jsonName = ""      # Name of the database file
    self.jsonFile = ""      # Full name of the databse file (path + filename)
    
    self.snapFolder = ""    # Directory where all the snapshots of the song are stored
    
    self.hasUnsavedChanges = False

    self.indexLastInsertion = -1

    self._makeDatabaseFileName(prFile)
    self._init()
    self._sanityCheck()



  # ---------------------------------------------------------------------------
  # METHOD Database._makeDatabaseFileName()
  # ---------------------------------------------------------------------------
  def _makeDatabaseFileName(self, prFile) :
    """
    Generates the name of the database file based on the .pr file.
    """
    
    # TODO: forbid any whitespace in the name, or dots, commas, etc.
    
    (rootDir, rootNameExt) = os.path.split(prFile)
    (rootName, _) = os.path.splitext(rootNameExt)
    self.songName   = rootNameExt
    self.jsonName   = rootName + ".json"          # Example: "my_song.json"
    self.jsonFile   = f"./snaps/{self.jsonName}"  # Example: "./snaps/my_song.json"
    self.snapFolder = f"./snaps/db__{rootName}"   # Example: "./snaps/db__my_song"



  # ---------------------------------------------------------------------------
  # METHOD Database._init()
  # ---------------------------------------------------------------------------
  def _init(self) :
    """
    Loads the database file (JSON), creates one if it does not exist.
    
    NOTE: the JSON and the snapshot folder are seen as inseparable. 
    If any is missing, it starts over with a new database.
    We do not want to deal with partial databases, attempt recoveries or any sort
    of thing. Just don't touch the database files and let the app access and manage it!
    """
        
    # Snapshot folder inexistent: the JSON is discarded for a new one.
    if not(os.path.exists(self.snapFolder)) :
      os.makedirs(self.snapFolder)

      # This is where we would eventually initialise the rest of the 
      # Database attributes. 
      # But try to avoid it and design the default attributes so that
      # we don't have to.
      # Otherwise it creates a double init and that's ugly.
      # self.nSnapshots = 0
      # ...


    # Snapshot folder exists
    else :
      if not(os.path.exists(self.jsonFile)) :
        print("[DEBUG] The snapshot directory exists, but there is no JSON.")
        
        # Rename the current snapshot folder
        # ...
        

        # Create a brand new one
        # ...
        
      else : 
        with open(self.jsonFile, "r") as jsonFile :
          data = json.load(jsonFile)
          self.fromDict(data)
        


    
  # ---------------------------------------------------------------------------
  # METHOD Database._sanityCheck()
  # ---------------------------------------------------------------------------
  def _sanityCheck(self) :
    """
    Make sure the all the files listed in the database exist.
    """
    print("[WARNING] Method 'Database._sanityCheck' is not implemented yet.")
  
  
  
  # ---------------------------------------------------------------------------
  # METHOD Database.insert()
  # ---------------------------------------------------------------------------
  def insert(self, img, index = -1) :
    """
    Inserts a new snapshot (PIL image object) in the snapshot list at the 
    specified index.
    
    After the insertion, image will be located at 'self.snapshots[index]'.

    If index = -1 (default) the image is inserted at the end of the list.
    """
    
    # Invalid input detection
    if (index < -1) :
      print(f"[DEBUG] Database.insert: index cannot be less than -1 (got: {index})")
      return None
    elif (index > self.nSnapshots) :
      print(f"[DEBUG] Database.insert: cannot insert beyond the last index (nSnapshots = {self.nSnapshots}, index = {index})")
      return None
    elif (index == -1) : 
      insertIndex = self.nSnapshots
    else : 
      insertIndex = index

    # Get a name for the snapshot file
    filename = self.generateFileName() + ".png"

    # Save the snapshot image
    img.save(f"{self.snapFolder}/{filename}")
    print(f"[DEBUG] Screenshot saved as '{filename}'")
    
    # Create the snapshot object 
    s = snapshot.Snapshot()
    s.dir         = self.snapFolder
    s.file        = filename
    s.index       = insertIndex
    s.displayName = f"Capture {insertIndex+1}"
    
    # Insert the snapshot in the list
    self.snapshots.insert(insertIndex, s)
    
    # If inserted before the end, all indices after need to be updated.
    if ((insertIndex >= 0) and (insertIndex <= (self.nSnapshots-1))) :
      for i in range(insertIndex+1, self.nSnapshots) :
        self.snapshots[i].index = i+1
    
    self.nSnapshots += 1
    self.isEmpty = False
    self.hasUnsavedChanges = True

    print(f"[DEBUG] nSnapshots = {self.nSnapshots}")

    

  # ---------------------------------------------------------------------------
  # METHOD Database.delete()
  # ---------------------------------------------------------------------------
  def delete(self) :
    """
    Deletes the snapshot from the snapshot list at the specified index.
    
    If index = -1 (default) the last item of the list is deleted.
    """
  
    print("[WARNING] Method 'Database.delete' is not implemented yet.")

    # Don't forget to update this flag
    self.isEmpty = (self.nSnapshots == 0)

  

  # ---------------------------------------------------------------------------
  # METHOD Database.getListBoxDescriptor()
  # ---------------------------------------------------------------------------  
  def getListBoxDescriptor(self) :
    """
    Returns the list of items that need to be shown in the scoreShot GUI's listbox.
    """
    L = [s.displayName for s in self.snapshots]
    return L
  
  

  # ---------------------------------------------------------------------------
  # METHOD Database.generateFileName()
  # ---------------------------------------------------------------------------  
  def generateFileName(self) :
    """
    Generates a unique file name for a snapshot.
    
    NOTE: generation shall be done at the database level (not Snapshot object level)
    because unicity requires knowledge of all names in the db.
    """

    # Restrain to a subset of chars 
    allowedChars = "ABCDEFGHKMNPQRTUVWXYZ" + "23456789"    
    return "".join(random.choice(allowedChars) for _ in range(6))



  # ---------------------------------------------------------------------------
  # METHOD Database.fromDict()
  # ---------------------------------------------------------------------------
  def fromDict(self, data) :
    """
    Loads the content of the Database class from a dictionary for easier 
    serialisation.
    """
    
    self.nSnapshots         = data["nSnapshots"]
    self.snapshots          = []
    self.isEmpty            = data["isEmpty"]
    self.songName           = data["songName"]
    self.jsonName           = data["jsonName"]
    self.jsonFile           = data["jsonFile"]
    self.snapFolder         = data["snapFolder"]
    self.hasUnsavedChanges  = data["hasUnsavedChanges"]
    #self.indexLastInsertion = data["indexLastInsertion"]     # No need to retrieve that.
    


  # ---------------------------------------------------------------------------
  # METHOD Database.toDict()
  # ---------------------------------------------------------------------------
  def toDict(self) :
    """
    Converts the content of the Database class to a dictionary for easier 
    serialisation.
    """
    return {
      "nSnapshots"        : self.nSnapshots,
      "snapshots"         : [s.toDict() for s in self.snapshots],
      "isEmpty"           : self.isEmpty,
      "songName"          : self.songName,
      "jsonName"          : self.jsonName,
      "jsonFile"          : self.jsonFile,
      "snapFolder"        : self.snapFolder,
      "hasUnsavedChanges" : self.hasUnsavedChanges
    }



  # ---------------------------------------------------------------------------
  # METHOD Database.save()
  # ---------------------------------------------------------------------------  
  def save(self) :
    """
    Saves the current database state in a JSON file.
    """
    d = self.toDict()
    with open(self.jsonFile, "w") as jsonFile :
      json.dump(d, jsonFile, indent = 2)



# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  db = Database("TEST")
  
  s = db.generateFileName()
  print(f"[DEBUG] Sample internal file name: '{s}'")
