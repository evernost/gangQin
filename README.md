# gangQin (v1.5)
Piano learning app, for those who can't read music scores.

## What do I need?
A piano keyboard with MIDI output, plugged into a computer running your favorite Python interpreter.

## Features (current release)
- **MIDI import**: import your songs from standard MIDI files
- **Bookmarking**: navigate quickly from one important section to the other without scrolling through the entire song
- **_fingersatz_ edition**: edit and display the finger to use for each note
- **Looped practice**: define a complex section you want to practice, play it on repeat
- **Single hand practice**: practice the left or right hand only
- **Key highlighting**: highlight the notes associated to the current key of the song (Cmaj, Dmin, etc.) Highlighting changes dynamically if there are key changes
- **Readable work file**: annotated score, bookmarks, fingersatz, ... are saved in a human readable '.pr' file (JSON)
- **Combo counter**: keep track of the number of correct notes played in a row
- **Quick find**: a given chord whose location is unknown can be found just pressing the query chord on the MIDI keyboard.
- **Perfect loop practice**: in looped practice, progress can be reset as soon as a mistake is made 😈
- **Lookahead view**: the keyboard shows the notes to be pressed, but also the upcoming ones with different shades for improved 'sightreading'. Lookahead distance can be adjusted.
- **Metronome**: practice with perfect timing.
- **Unbound looped practice**: define a start point and try to play. Any mistake jumps you back to the starting point

## Upcoming features
- Metronome with dynamic tempo, ajusts automatically throughout the score
- Enhanced fingersatz edition, with more shortcuts
- Dynamic comments display, updated based on the location in the score
- More flexible MIDI loading: select the tracks you want to import


## Screenshot

![image](https://github.com/user-attachments/assets/0b3f73a9-8bc5-4def-a016-6dabc6d473cd)



## Shortcuts

| Key           | Function      |
|:------------- |:-------------|
| ←             |Previous  cursor|
| →             |Next cursor     |
| ↑             |Next bookmark   |
| ↓             |Previous bookmark|
| S             |Save to .pr file|
| B             |Toggle bookmark on the current cursor|
| L             |Toggle left hand practice|
| R             |Toggle right hand practice|
| M             |Toggle metronome|
| M+            |Increase metronome tempo|
| M-            |Decrease metronome tempo|
| F2            |Increase lookahead distance|
| F3            |Toggle 'strict' mode in looped practice|
| F9            |Set the beginning of the loop at the current cursor|
| F10           |Set the end of the loop at the current cursor|
| F11           |Erase loop information|



## Requirements

- **pygame** (tested with version 2.6)
- **numpy**
- **shapely** (tested with version 2.0.4)
- **playsound**
  - pip install --upgrade setuptools wheel
  - pip install playsound
- **mido** (tested with version 1.3.2)
- **rtmidi** (tested with version 1.5.8)
  - pip install python-rtmidi
