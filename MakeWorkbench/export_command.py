# Toolbar command for exporting. Owns everything the user sees;
# the actual export logic is in exporter.py.

import os

import FreeCAD as App
import FreeCADGui
from PySide6 import QtWidgets

from MakeWorkbench import exporter
from MakeWorkbench import settings


class ExportCommand:
    """Export the selected body or part to STL."""

    def GetResources(self):
        return {
            "MenuText": "Export STL",
            "ToolTip": "Export the selected body or part to an STL"
                       " file for 3D printing.",
        }

    def IsActive(self):
        """Clickable only while a printable object is selected."""
        return any(exporter.has_printable_shape(o)
                   for o in FreeCADGui.Selection.getSelection())

    def Activated(self):
        printable = [o for o in FreeCADGui.Selection.getSelection()
                     if exporter.has_printable_shape(o)]
        if not printable:
            App.Console.PrintError("Make: select a body or part first.\n")
            return

        obj = printable[0]

        # Qt directly, because this build has no
        # FreeCADGui.getSaveFileName (PLAN.md, M0 lessons).
        # Cancelling the dialog returns an empty path. The dialog
        # starts in the last folder exported to.
        suggested = os.path.join(settings.last_dir(),
                                 exporter.default_filename(obj))
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            FreeCADGui.getMainWindow(), "Export STL", suggested,
            "STL Mesh (*.stl)")
        if not path:
            return

        try:
            linear_dev, angular_dev = settings.deviation()
            exporter.export_to_stl(obj, path, linear_dev, angular_dev)
        except Exception as exc:
            App.Console.PrintError("Make: export failed: %s\n" % exc)
            return

        settings.set_last_dir(os.path.dirname(path))
        App.Console.PrintMessage(
            "Make: exported '%s' -> %s\n" % (obj.Label, path))
