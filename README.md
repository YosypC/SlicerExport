# Make Workbench

A small FreeCAD workbench for quickly exporting parts and bodies to be
sent off to a 3D printing slicer - the FreeCAD answer to Fusion's
"Make" tab. See `PLAN.md` for requirements and the milestone roadmap.

## What it does

- **Export STL** - write the selected body or part to an STL file.
  Uses the quality preset from settings; the save dialog starts in
  the folder of the last export.
- **Send to slicer** - write a temporary STL (no dialog) and open it
  directly in the configured slicer. One click.
- **Settings** - export quality (Coarse / Standard / Fine) and the
  slicer executable.

## Installing for development

FreeCAD loads workbenches from its "Mod" directory. Link this folder
into Mod instead of copying files (they would go stale):

    cd <FreeCAD's user Mod folder>
    mklink /J MakeWorkbench C:\...\FreeCAD_3D_printing_project

Run `mklink` in `cmd.exe`, not Git Bash. The workbench must live under
the name `MakeWorkbench` - the InitGui fallback depends on it
(PLAN.md, M0 lessons). FreeCAD's user Mod folder is printed under
Edit -> Preferences -> General -> Additional module paths, or run
`FreeCAD.getUserAppDataDir()` in the Python console and append `Mod`.

## Testing

- Automated logic tests: `uvx pytest tests`
- Manual GUI checklist: `TESTING.md` - run through it after workbench
  changes or a FreeCAD rebuild.
