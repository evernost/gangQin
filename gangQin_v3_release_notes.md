# gangQin v3.0 - Release notes (June 2025)

## What's New
### gangQin Player
- [X] new backgrounds available
- [ ] new keyboard style
- [ ] perspective view in the pianoroll
- [ ] bookmarks visible in staffscope
- [ ] edit notes with wrong pitch directly from the app (no more manual file edition)
- [ ] added a rehearsal mode
- [ ] added a transposed mode (either transposed input, or transposed output)
- [ ] added a weak arbitration mode
- [ ] added a versatile metronome
- [ ] status bar indicating various kind of messages (errors in the score, warnings, etc.)

## Improvements
- [ ] major code refactor, more modular, overall code more coherent and less duplicates
- [X] constants centralised and reorganised in 'commons.py'

### gangQin Player:
- [X] track selection for MIDI file now fully integrated
- [ ] cursor auto-increment during fingersatz edition when a single hand is playing
- [ ] song selector proposes the most practiced songs first
- [ ] wrong note counter is disabled in looped practice (so that the counter does not go crazy. See issue #15)
- [ ] added more shortcuts for the finger selector
- [ ] improved hand selector for the single hand practice
- [ ] auto-backup of .gq if overwritten by a new generation from .mid
- [ ] auto-backup of .gq during practice
- [X] more robust single hand practice
- [ ] double key press replaced by an orange note, the user must indicate what hand should play
- [ ] auto-detection of odd fingersatz in chords
- [ ] clearer stat cues

### gangQin Fusion:
- [ ] auto-repeat function for the playglows
- [ ] song selector defaults to the last song
- [ ] ghost mode on the mouse cursor to help placing the playglow

### gangQin Capture:
- [ ] added snapshot counter
- [ ] added context to the score (page number, capture number within the page, editor's name, etc.)

## Bug Fixes
- [ ] more robust MIDI keyboard detection (issue #9)
- [ ] playglows disappearing (issue #13)
- [X] crash during some MIDI file imports (issue #16)

# Performance
TODO

# Known Issues
None.