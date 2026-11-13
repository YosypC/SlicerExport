# MakeWorkbench/exporter.py
#
# The pure logic of exporting: object -> STL file on disk.
#
# This module must never touch the GUI - no dialogs, no FreeCADGui.
# That is the rule that keeps it testable without opening FreeCAD's
# interface (PLAN.md, requirement N3). The command in
# export_command.py owns everything the user sees.

import os

import FreeCAD as App
import Mesh          # FreeCAD's mesh workbench module; ships with FreeCAD


def has_printable_shape(obj):
    """Return True if obj carries solid geometry we can mesh.

    A "printable" object is anything with a non-empty Shape that
    contains at least one solid: Bodies, Part features, etc.
    Sketches and datum objects have no solids and are rejected by
    this check.
    """
    if not hasattr(obj, "Shape"):
        return False
    shape = obj.Shape
    if shape is None or shape.isNull():
        return False
    return len(shape.Solids) > 0


def default_filename(obj):
    """Derive a sensible '.stl' filename from the object's label.

    Label is what the user sees in the tree (Name is the unchangeable
    internal identifier). Windows forbids some characters in
    filenames; we replace them with underscores so export never
    fails over a name like "Br#cket 1".
    """
    forbidden = '\\/:*?"<>|'
    clean = "".join("_" if ch in forbidden else ch for ch in obj.Label)
    return clean.strip() or "part"          # never empty
    # note: extension ".stl" is appended later


def export_to_stl(obj, path, deviation=0.1):
    """Write obj's geometry to an STL file at path.

    deviation is the tessellation tolerance in millimetres: how far
    the mesh triangles may deviate from the true curved surface.
    Smaller = finer mesh + bigger file. 0.1 mm is M1's hardcoded
    value; the Coarse/Standard/Fine presets (requirement R2) will
    replace it in M2 once we benchmark real numbers.

    Mesh.export raises an exception on failure; the caller decides
    how to report it to the user.
    """
    Mesh.export([obj], path, deviation)
    return path
