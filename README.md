# gangQin v2.0 (beta)
Piano learning app, for those who struggle with the conventional music scores.

![image](https://github.com/user-attachments/assets/1cd22e89-eea6-40ad-90cc-525259448a2c)

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
- **Built-in metronome**: practice with perfect timing.
- **Unbound looped practice**: define a start point and try to play from it on. Any mistake sends you back to the starting point.
- **Direct view on the real score**: import the real score and have it displayed while playing.

## Upcoming features (one day)

- **Enhanced _fingersatz_ edition**: more shortcuts, make it quicker and easier to edit
- **More complete playing statistics**: provide some hindsight on the overall playing performance of a song
- **Dynamic comments display**: a comment, or notes show at a certain cursor, for a certain section, like a copilot
- **Flexible MIDI loading**: select the specific tracks you want to import (MIDI might have way more than 2)
- **Metronome with dynamic tempo**: tempo is adjusted automatically throughout the score. It also helps to monitor your playing speed, hence your progress
- **Semi-automated _fingersatz_ edition**: simplify the assignation of repeated sections (repeated chords, codas, etc.)
- **Auto-highlight of the complex sections**: in the staffScope view, a color code shows the section that caused the most trouble, based on the playing statistics
- **Time accuracy score display**: shows how well you play the notes at the right time

## Shortcuts

| Key           | Function      |
|:------------- |:-------------|
| ←             |Previous cursor|
| →             |Next cursor     |
| ↑             |Next bookmark   |
| ↓             |Previous bookmark|
| S             |Save to .pr file|
| B             |Bookmark the current cursor|
| L             |Toggle ON/OFF left hand practice|
| R             |Toggle ON/OFF right hand practice|
| M             |Toggle ON/OFF the metronome|
| M+            |Increase metronome tempo|
| M-            |Decrease metronome tempo|
| V             |Toggle pianoroll/staffscope view|
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


## TODO / Ideas

Remaining tasks: 
- [ ] CTRL+ and CTRL- adjust the view span in pianoroll mode.
- [ ] terminate properly when the last cursor is reached.
- [ ] staffscope: highlight the sections that causes the most trouble.
- [ ] scoreShot-capture: on the capture window, show the snapshot count number.
- [ ] staffscope: print a "no signal" message when there is no staff available for the current cursor
