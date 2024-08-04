# gangQin (v1.3)
Piano learning app, for those who can't read music scores.

## Features (current release)
- **MIDI import**: scores can be imported from standard MIDI files
- **Bookmarking**: navigate quickly from one important section to the other without scrolling the entire song
- **_fingersatz_**: edit and display the finger to use for each note
- **Loop practice**: define a complex section you want to practice, play it on repeat
- **Single hand practice**: practice the left or right hand only
- **Key highlight**: highlight the notes associated to the current key of the song. Highlighting changes dynamically if there are key changes
- **Readable work file**: annotated score, bookmarks, fingersatz, ... are saved in a human readable file (JSON)
- **Combo counter**: keep track of the number of correct notes played in a row
- **Quick find**: a given chord whose location is unknown can be found just pressing the query chord on the MIDI keyboard.
- **Perfect loop practice**: in loop practice, progress can be reset as soon as a mistake is made 😈
- **Lookahead view**: the keyboard shows the notes to be pressed, but also the upcoming ones with different shades for improved 'sightreading'. Lookahead distance can be adjusted.

## Upcoming features
- Enhanced fingersatz edition, with more shortcuts
- 'heading' indicator, pointing for each hand the direction they are about to aim to
- Dynamic comments display, updated based on the location in the score
- Relative difficulty display (based on user playing info analysis)

## Screenshot

![image](https://github.com/user-attachments/assets/7074402e-3e76-420b-b5c5-e5a7e0cd500a)



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
| F2            |Increase lookahead distance|
| F3            |Toggle 'strict' mode in looped practice|
| F9            |Set the beginning of the loop at the current cursor|
| F10           |Set the end of the loop at the current cursor|
| F11           |Erase loop information|



## Requirements

- **pygame** (tested with version 2.6)
- **shapely** (tested with version 2.0.4)
- **playsound**
  - pip install --upgrade setuptools wheel
  - pip install playsound
- **mido** (tested with version 1.3.2)
- **rtmidi** (tested with version 1.5.8)
  - pip install python-rtmidi
