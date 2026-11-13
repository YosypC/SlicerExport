# Make Workbench

A small FreeCAD workbench for quickly exporting parts and bodies to be
sent off to a 3D printing slicer - the FreeCAD answer to Fusion's "Make"
tab. See `PLAN.md` for requirements and the milestone roadmap.

Status: **M0 (skeleton)**. The workbench appears in FreeCAD's workbench
dropdown and has a single test button that prints a message to the
console.

## Installing for development

FreeCAD loads workbenches from its "Mod" directory. Instead of copying
files there (they would go stale), link this folder into Mod once:

    cd <FreeCAD's user Mod folder>
    mklink /J MakeWorkbench C:\...\FreeCAD_3D_printing_project

On Windows, `mklink /J` needs to run in `cmd.exe` (not Git Bash). FreeCAD
prints the exact Mod folder location in
**Edit -> Preferences -> General -> Additional module paths**, or run
`FreeCAD.getUserAppDataDir()` in the Python console and append `Mod`.

## Testing M0 by hand

1. Start FreeCAD.
2. Open the Python console (View -> Panels -> Python console).
3. Switch to the "Make" workbench in the dropdown.
4. Click "Hello (workbench test)".
5. The console should print: `Hello from the Make workbench - plumbing works.`
