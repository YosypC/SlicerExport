# FreeCAD "Make" Workbench — Plan

A simple FreeCAD workbench that solves the same functions as the "Make" tab on
Autodesk Fusion: quickly export a part or body, ready to be sent off to a 3D
printing slicer.

Goals for the project as a whole:

- Maintained by a human without AI assistance.
- Code written to be readable by a programming novice. Comments explain the
  *why* and the Python idioms, not just the syntax.
- No external Python dependencies beyond what ships with FreeCAD.
- Scope grows step by step. Each milestone is independently usable.

Assumptions: FreeCAD 1.0+, Windows as primary platform (code kept
cross-platform anyway).

## What Fusion's "Make" tab actually does

Stripped down, it is three things:

1. Detect a solid/body selection (or take the whole document),
2. Export it to a mesh format a slicer understands (STL now; 3MF, STEP later),
3. Hand it off — via a save dialog or by opening the slicer with the file.

Everything else (presets, multi-body, orientations) is sugar.

## Requirements

### Functional

- R1: Export the active or selected Body/Part to STL (later: 3MF, STEP).
- R2: Mesh quality setting — Coarse / Standard / Fine presets controlling the
  tessellation deviation used on export, persisted per user. Exact numeric
  values are tuned during M1 once we can compare real output.
- R3: Optional "open in slicer" action: launch a user-configured slicer
  executable with the exported file as argument.
- R4: Live in FreeCAD's UI as a proper workbench (toolbar icon + a small task
  panel), not a macro run from the Python console.

Filenames derive from the body's name; the save destination uses FreeCAD's
native save dialog. No export-folder configuration in v1 — dropped in favor of
R2. A slicer "watched folder" workflow remains possible by pointing the save
dialog at it.

### Non-functional

- N1: Readable, commented code a novice maintainer can follow.
- N2: No external Python dependencies beyond what ships with FreeCAD.
- N3: Core export logic works headless (no GUI) so it can be tested
  automatically.

Functional requirements say *what it does*; non-functional ones say *how well
it does it*. They fail differently: a failing R leaves a feature missing, a
failing N makes the project rot over time. Hence separate prefixes (R / N,
from "Requirement" / "Non-functional requirement").

### Out of scope for v1

3MF, multi-body batch export, print presets, slicer profile management, export
folder configuration, cloud anything.

## Why a workbench and not a macro

A macro is one big script living in a user folder. A workbench is a proper
module: an `InitGui.py` that registers the workbench, a core module with the
export logic, icons, and a place for tests. Same effort to write, much easier
to maintain and version in git.

## Architecture

```
FreeCADWorkbench/
├── InitGui.py          # FreeCAD entry point; registers workbench, toolbar, menus
├── MakeWorkbench/      # (name TBD) the actual Python package
│   ├── exporter.py     # PURE logic: Body + quality -> STL on disk. No GUI.
│   ├── settings.py     # read/write user preferences (quality preset, slicer path)
│   ├── launcher.py     # run the slicer executable (subprocess, guarded)
│   └── task_panel.py   # the ONLY file that touches FreeCAD's GUI
└── tests/
    └── test_exporter.py
```

Key idea: the GUI layer is a thin skin over pure logic. `exporter.py` takes a
FreeCAD object, a quality preset, and a path, and returns success/failure — it
never shows a dialog. That separation is what lets ~80% of the workbench be
tested without launching FreeCAD's interface.

## Testing strategy

One honest rule: every bug fixed gets a test that would have caught it.

- **Layer 1 — logic tests, no FreeCAD needed**: filename generation from a
  body's name, quality preset -> deviation mapping, bad-input handling
  (no selection, non-solid selected). Plain Python, run in seconds.
- **Layer 2 — FreeCAD headless tests**: run `FreeCADCmd` (the console build,
  ships with the install), load a test document, export it at each quality
  preset, verify the STL file exists and contains a mesh of the expected
  triangle count range.
- **Layer 3 — manual smoke test checklist**: a short `TESTING.md` — open demo
  part -> select body -> click export -> check file opens in the slicer.

## Roadmap

- **M0 — skeleton**: workbench appears in FreeCAD's workbench dropdown with
  one toolbar button that logs "hello". Proves the plumbing. Hardest step;
  do it first.
- **M1 — export**: button exports the selected body to STL via a save dialog,
  at a hardcoded quality. Then benchmark Coarse/Standard/Fine deviation values
  and lock in R2's numbers.
- **M2 — settings**: quality presets (plus slicer path for R3) configurable in
  FreeCAD preferences.
- **M3 — launch slicer**: pass the exported file to the configured executable.
- **M4 — polish**: task panel with quality selector + filename preview,
  single-click "Export & Print", error messages a human can read.
