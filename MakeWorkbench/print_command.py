# "Send to slicer" command: export the selection to a temporary STL
# - no save dialog, like Fusion's Make/print utility - and open it
# in the configured slicer.

import os
import tempfile

import FreeCAD as App
import FreeCADGui

from MakeWorkbench import exporter
from MakeWorkbench import launcher
from MakeWorkbench import settings
from MakeWorkbench.export_command import get_printable_selection


class PrintCommand:
    """Export the selection and open it in the slicer."""

    def GetResources(self):
        return {
            "MenuText": "Send to slicer",
            "ToolTip": "Export the selected body or part and open it"
                       " directly in your slicer.",
        }

    def IsActive(self):
        """Clickable only while a printable object is selected."""
        return any(exporter.has_printable_shape(o)
                   for o in FreeCADGui.Selection.getSelection())

    def Activated(self):
        slicer = settings.slicer_path()
        if not slicer:
            App.Console.PrintError(
                "Make: no slicer configured - set one in"
                " Make settings.\n")
            return

        obj = get_printable_selection()
        if not obj:
            return

        # A separate process can only be handed a real file, so write
        # to the OS temp folder silently. One fixed name: every send
        # overwrites the same file, so the temp folder never grows.
        path = os.path.join(tempfile.gettempdir(), "MakeWorkbenchExport.stl")
        try:
            linear_dev, angular_dev = settings.deviation()
            exporter.export_to_stl(obj, path, linear_dev, angular_dev)
        except Exception as exc:
            App.Console.PrintError(
                "Make: temporary export failed: %s\n" % exc)
            return

        try:
            launcher.launch(slicer, path)
            App.Console.PrintMessage(
                "Make: sent '%s' to %s (temp file: %s)\n"
                % (obj.Label, os.path.basename(slicer), path))
        except OSError as exc:
            App.Console.PrintError(
                "Make: could not start slicer: %s\n" % exc)
