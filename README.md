# Slicer Export

A small FreeCAD workbench for quickly exporting parts and bodies to be
sent off to a 3D printing slicer. See `PLAN.md` for requirements and the
milestone roadmap.

## What it does

- **Export** - writes the selected body or part to an STL or STEP file. STL export's quality can be selected.
- **Send to slicer** - writes a temporary STL or STEP to OS's temporary folder and opens it directly in the configured slicer. One click!
- **Settings** - export quality (Coarse / Standard / Fine), the slicer executable, and the Send to slicer format.

## Installing for development

FreeCAD loads workbenches from its user "Mod" directory. Don't copy
files there - copies go stale. Link this folder in once, under the
name `SlicerExport` (the InitGui fallback depends on the name -
see PLAN.md, M0 lessons).

Find your Mod folder first: run `FreeCAD.getUserAppDataDir()` in
FreeCAD's Python console (View -> Panels -> Python console) and
append `Mod`. Then, from the repo's parent folder:

- **Windows** (`cmd.exe`):

      mklink /J "<Mod>\SlicerExport" "<repo folder>"

- **Linux / macOS**:

      ln -s "<repo folder>" "<Mod>/SlicerExport"

## Testing

- Automated logic tests: `uvx pytest tests`
- Manual GUI checklist: `TESTING.md` - run through it after workbench
  changes or a FreeCAD rebuild.
