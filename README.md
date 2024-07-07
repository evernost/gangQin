# gangQin (v1.2)
Piano learning app, for those who can't read music scores.

## Features (current release)
- **MIDI import**: scores can be imported from standard MIDI files
- **Bookmarking**: navigate quickly from one section to the other without scrolling the entire song
- **_fingersatz_**: edit and display the finger to use for each note
- **Loop practice**: define the location of the complex section, play it on repeat
- **Single hand practice**: practice the left or right hand only
- **Key highlight**: highlight the notes associated to the current key of the song. Highlighting changes dynamically if there are key changes
- **Readable work file**: annotated score, bookmarks, fingersatz, ... are saved in a human readable file (JSON)
- **Combo counter**: keep track of the number of correct notes played in a row
- **Quick find**: a given chord whose location is unknown can be found just pressing the query chord on the MIDI keyboard.

## Upcoming features
- Note 'lookahead' display
- 'heading' indicator, pointing for each hand the direction they are about to aim to
- Dynamic comments display, updated based on the location in the score
- Relative difficulty display (based on user playing info analysis)

## Screenshot

![image](https://github.com/evernost/gangQin/assets/106398901/ba9d3e4b-d4fe-4194-b2f6-0df6440085b4)


## Requirements

- **pygame** (tested with version 2.6)
- **shapely** (tested with version 2.0.4)
- **playsound**
  - pip install --upgrade setuptools wheel
  - pip install playsound
- **mido** (tested with version 1.3.2)
- **rtmidi** (tested with version 1.5.8)
  - pip install python-rtmidi
