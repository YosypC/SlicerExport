# MakeWorkbench/export_command.py
#
# The toolbar button for exporting. A "command" object like this is
# FreeCAD's standard way to describe a button: what it says, when it
# is clickable, and what happens on click (Activated).
#
# This module owns everything the user SEES (button state, save
# dialog, console messages) and delegates everything else to
# exporter.py - the pure, testable logic.

import os

import FreeCAD as App
import FreeCADGui
from PySide6 import QtWidgets      # Qt, ships with FreeCAD
from MakeWorkbench import exporter


class ExportCommand:
    """Export the selected body or part to STL for 3D printing."""

    def GetResources(self):
        """Button metadata. Returns a plain dictionary."""
        return {
            "MenuText": "Export STL",
            "ToolTip": "Export the selected body or part to an STL"
                       " file for 3D printing.",
            "Accel": "",
        }

    def IsActive(self):
        """Clickable only if a printable object is selected.

        FreeCAD calls this repeatedly; keep it fast. When it returns
        False the button is greyed out.
        """
        selection = FreeCADGui.Selection.getSelection()
        return any(exporter.has_printable_shape(o) for o in selection)
        # "any(...)" = at least one selected object is printable

    def Activated(self):
        """Called when the user clicks the button."""
        selection = FreeCADGui.Selection.getSelection()
        printable = [o for o in selection
                     if exporter.has_printable_shape(o)]
        if not printable:
            App.Console.PrintError(
                "Make: select a body or part first.\n")
            return

        obj = printable[0]     # first printable object wins

        # Native save dialog. We use Qt directly (QFileDialog) because
        # this FreeCAD build has no FreeCADGui.getSaveFileName. The
        # dialog's parent is FreeCAD's main window so it sits on top
        # of the right application. QFileDialog.getSaveFileName
        # returns a (path, filter) pair; an empty path means the
        # user cancelled.
        suggested = exporter.default_filename(obj)
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            FreeCADGui.getMainWindow(),
            "Export STL",
            suggested,
            "STL Mesh (*.stl)")
        if not path:
            return

        try:
            exporter.export_to_stl(obj, path)
        except Exception as exc:
            # Any failure here is a FreeCAD/geometry problem we did
            # not anticipate; surface it instead of crashing the GUI.
            App.Console.PrintError("Make: export failed: %s\n" % exc)

        App.Console.PrintMessage(
            "Make: exported '%s' -> %s\n" % (obj.Label, path))
