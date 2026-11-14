# "Send to slicer" command: export, then hand the file to the
# configured slicer executable. One click, like Fusion's Make tab.

import os

import FreeCAD as App
import FreeCADGui

from MakeWorkbench import exporter
from MakeWorkbench import launcher
from MakeWorkbench import settings
from MakeWorkbench.export_command import export_via_dialog


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

        path = export_via_dialog("Send to slicer")
        if not path:
            return

        try:
            launcher.launch(slicer, path)
            App.Console.PrintMessage(
                "Make: opened in %s\n" % os.path.basename(slicer))
        except OSError as exc:
            App.Console.PrintError(
                "Make: could not start slicer: %s\n" % exc)
