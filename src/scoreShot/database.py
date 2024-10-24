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



# =============================================================================
# Constants pool
# =============================================================================
# None.



# =============================================================================
# Main code
# =============================================================================
class Database :

  """
  Defines the class for the snapshot database.
  This class only manages the snapshots and their arrangement within the database.
  """
  def __init__(self, prFile) :
    
    self.nSnapshots = 0
    self.snapshots = []
    self.isEmpty = True
    
    self.songName     = ""          # Name of the song file
    self.jsonName     = ""          # Name of the database file
    self.jsonFile     = ""          # Full name of the databse file (path + filename)
    self.depotFolder  = ""          # Directory where all the snapshots of the song are stored
    
    self.description  = ""          # Description string for the database
                                    # e.g. name of the PDF file for the score, display settings used etc.

    self.hasUnsavedChanges = False  # Turns True if anything has been modified in the database
    self.changeLog = []

    self.indexLastInsertion = -1    # Index where the last snapshot insertion occured


    # Initialisation procedures
    self._loadNames(prFile)
    self._loadJSON()
    self._integrityCheck()



  # ---------------------------------------------------------------------------
  # METHOD Database._loadNames()
  # ---------------------------------------------------------------------------
  def _loadNames(self, prFile) :
    """
    Generates the various names of files and directories associated with the 
    database.
    """
    
    # TODO: forbid any whitespace in the name, or dots, commas, etc.
    
    (rootDir, rootNameExt) = os.path.split(prFile)
    (rootName, _) = os.path.splitext(rootNameExt)
    self.songName     = rootName
    self.songFile     = rootNameExt
    self.jsonName     = rootName + ".json"          # Example: "my_song.json"
    self.jsonFile     = f"./snaps/{self.jsonName}"  # Example: "./snaps/my_song.json"
    self.depotFolder  = f"./snaps/db__{rootName}"   # Example: "./snaps/db__my_song"



  # ---------------------------------------------------------------------------
  # METHOD Database._loadJSON()
  # ---------------------------------------------------------------------------
  def _loadJSON(self) :
    """
    Loads the database file (JSON), creates one if it does not exist.
    
    NOTE: the JSON and the snapshot folder are seen as inseparable. 
    If any is missing, it starts over with a new database.
    We do not want to deal with partial databases, attempt recoveries or any sort
    of thing. Just don't touch the database files and let the app access and manage it!
    """
        
    # Snapshot folder inexistent: the JSON is discarded for a new one.
    if not(os.path.exists(self.depotFolder)) :
      os.makedirs(self.depotFolder)

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
  # METHOD Database._integrityCheck()
  # ---------------------------------------------------------------------------
  def _integrityCheck(self) :
    """
    Make sure the all the files listed in the database exist.
    """
    print("[WARNING] Method 'Database._integrityCheck' is not implemented yet.")
  
  
  
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
    img.save(f"{self.depotFolder}/{filename}")
    print(f"[DEBUG] Screenshot saved as '{filename}'")
    
    # Create the snapshot object 
    s = snapshot.Snapshot()
    s.dir         = self.depotFolder
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
    self.changeLog.append(f"- snap insertion at {insertIndex}")

    print(f"[DEBUG] nSnapshots = {self.nSnapshots}")

    

  # ---------------------------------------------------------------------------
  # METHOD Database.delete()
  # ---------------------------------------------------------------------------
  def delete(self, index) :
    """
    Deletes the snapshot from the snapshot list at the specified index.
    
    If index = -1 (default) the last item of the list is deleted.
    """
  
    print("[WARNING] Method 'Database.delete' is not implemented yet.")

    # Don't forget to update this flag
    self.isEmpty = (self.nSnapshots == 0)
    
    self.changeLog.append(f"- snap insertion at {index}")

  

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
  # METHOD Database.getSnapshotFileByIndex()
  # ---------------------------------------------------------------------------  
  def getSnapshotFileByIndex(self, index) :
    """
    Returns the full name (path + file) of the .png from its index in the database.
    Returns an empty string if the index is invalid.
    """
    
    if ((index >= 0) and (index <= (self.nSnapshots-1))) :
      s = self.snapshots[index]
      return f"{s.dir}/{s.file}"
    
    else :
      print(f"[DEBUG] Database.getSnapshotFileByIndex(): requested index {index} cannot be loaded.")
      return ""
    


  # ---------------------------------------------------------------------------
  # METHOD Database.getIndexByCursor()
  # ---------------------------------------------------------------------------  
  def getIndexByCursor(self, cursor) :
    """
    Finds the snapshot in the database that covers the cursor value passed as argument.
    Returns its index in the database if found, otherwise returns -1.
    """
    
    print("[DEBUG] Database.getIndexByCursor() is TODO.")






  # ---------------------------------------------------------------------------
  # METHOD Database.generateFileName()
  # ---------------------------------------------------------------------------  
  def generateFileName(self) :
    """
    Generates a unique file name for a snapshot.
    
    NOTE: generation shall be done here (at the database level) because unicity 
    requires knowledge of all names in the db.
    """

    # Restrain to a subset of chars 
    allowedChars = "ABCDEFGHKMNPQRTUVWXYZ" + "23456789"    
    
    # TODO: make sure the name does not already exist
    # ...
    
    
    return "".join(random.choice(allowedChars) for _ in range(6))

    

  # ---------------------------------------------------------------------------
  # METHOD Database.fromDict()
  # ---------------------------------------------------------------------------
  def fromDict(self, data) :
    """
    Loads the content of the Database class from a dictionary for easier 
    serialisation.
    """
    
    # TODO: iterate over the attributes (except for "snapshots" who's a bit of an oddity)
    #       instead of manually listing all of them. 
    #       The list tends to change regularly.
    self.nSnapshots         = data["nSnapshots"]
    self.snapshots          = [(s := snapshot.Snapshot()).fromDict(snapData) or s for snapData in data["snapshots"]]
    self.isEmpty            = data["isEmpty"]
    self.songName           = data["songName"]
    self.songFile           = data["songFile"]
    self.jsonName           = data["jsonName"]
    self.jsonFile           = data["jsonFile"]
    self.depotFolder        = data["depotFolder"]
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

    # TODO: iterate over the attributes instead of manually listing all of them.
    return {
      "nSnapshots"        : self.nSnapshots,
      "snapshots"         : [s.toDict() for s in self.snapshots],
      "isEmpty"           : self.isEmpty,
      "songName"          : self.songName,
      "songFile"          : self.songFile,
      "jsonName"          : self.jsonName,
      "jsonFile"          : self.jsonFile,
      "depotFolder"       : self.depotFolder,
      "hasUnsavedChanges" : self.hasUnsavedChanges
    }



  # ---------------------------------------------------------------------------
  # METHOD Database.save()
  # ---------------------------------------------------------------------------  
  def save(self) :
    """
    Saves the current database state in a JSON file.
    """
    
    self._changeLogClear()

    d = self.toDict()
    with open(self.jsonFile, "w") as jsonFile :
      json.dump(d, jsonFile, indent = 2)

    

  # ---------------------------------------------------------------------------
  # METHOD Database._changeLogClear()
  # ---------------------------------------------------------------------------  
  def _changeLogClear(self) :
    """
    Clears the change log.
    """
    
    self.hasUnsavedChanges = False
    self.changeLog = []
    


# =============================================================================
# Unit tests
# =============================================================================
if (__name__ == "__main__") :
  db = Database("TEST")
  
  s = db.generateFileName()
  print(f"[DEBUG] Sample internal file name: '{s}'")
