# gangQin (v1.2)
Piano learning app, for those who can't read music scores.

## Features (current release)
- Scores imported from MIDI files
- Bookmarking: navigate from one section to the other
- _fingersatz_ edition and display
- Loop practice mode
- Single hand practice mode
- Keyboard dynamically highlights some of its notes based on the key of the current section
- Annotated score with all user info can be saved/restored in a human readable file (JSON)
- Combo counter: how many corrects notes in a row

## Upcoming features
- Note 'lookahead' display
- 'heading' indicator, pointing for each hand the direction they are about to aim to
- Dynamic comments display, updated based on the location in the score
- Relative difficulty display (based on user playing info analysis)

## Screenshot

![image](https://github.com/evernost/gangQin/assets/106398901/ba9d3e4b-d4fe-4194-b2f6-0df6440085b4)


## Requirements

- pygame (tested with version 2.6)
- shapely (tested with version 2.0.4)
- playsound
  - pip install --upgrade setuptools wheel
  - pip install playsound
- mido (tested with version 1.3.2)
- rtmidi (tested with version 1.5.8)
  - pip install python-rtmidi
