# Manual smoke test - Make workbench

Tick every line after changes to the workbench or after rebuilding
FreeCAD. Automated checks: `uvx pytest tests` (14 green). This list
covers what automation cannot: the GUI itself.

## Setup

- FreeCAD restarted after the last workbench change
- A document open with at least one Body
- OrcaSlicer installed; path configured once via Make settings

## Buttons

- [] Workbench "Make" appears in the dropdown
- [] Toolbar shows: Export STL, Send to slicer, Settings (with icons)
- [] With nothing selected: all three action buttons greyed out
- [] Selecting the Body enables them; selecting only a sketch
      (no solids) keeps them greyed

## Export STL

- [] Save dialog opens in the folder of the last export, filename
      pre-filled with the body's name
- [] After saving, console prints `Make: exported '<label>' -> <path>`
- [] Reopening the file in OrcaSlicer shows the correct geometry

## Send to slicer

- [] No save dialog appears
- [] OrcaSlicer opens directly with the part loaded
- [] Console prints `Make: sent '<label>' to ... (temp file: ...)`
- [] With no slicer configured (clear the setting to test): console
      prints the "no slicer configured" error, nothing opens

## Settings

- [] Quality preset survives a FreeCAD restart
- [] Higher presets produce visibly smoother curved surfaces in
      OrcaSlicer (compare Coarse vs Fine on a sphere)
- [] Slicer path browse button only accepts executables
