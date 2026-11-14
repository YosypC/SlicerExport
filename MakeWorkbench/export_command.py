# Export toolbar command and the interactive export routine shared
# with the Send-to-slicer command. Owns everything the user sees;
# the actual export logic is in exporter.py.

import os

import FreeCAD as App
import FreeCADGui
from PySide6 import QtWidgets

from MakeWorkbench import exporter
from MakeWorkbench import settings
from MakeWorkbench import icon


def get_printable_selection():
    """The first printable selected object, or None (with a console
    error explaining why). Shared by both toolbar commands."""
    printable = [o for o in FreeCADGui.Selection.getSelection()
                 if exporter.has_printable_shape(o)]
    if not printable:
        App.Console.PrintError("Make: select a body or part first.\n")
        return None
    return printable[0]


def export_via_dialog(window_title="Export STL"):
    """Interactive export: selection -> save dialog -> STL.

    Returns the written file path, or None if nothing printable is
    selected, the dialog is cancelled, or the export fails (failures
    are reported to the console).
    """
    obj = get_printable_selection()
    if not obj:
        return None

    # Qt directly, because this build has no
    # FreeCADGui.getSaveFileName (PLAN.md, M0 lessons).
    # The dialog starts in the last folder exported to; the format
    # filter the user picks decides which exporter runs.
    suggested = os.path.join(settings.last_dir(),
                             exporter.default_filename(obj))
    path, chosen_filter = QtWidgets.QFileDialog.getSaveFileName(
        FreeCADGui.getMainWindow(), window_title, suggested,
        "STL Mesh (*.stl);;STEP (*.step *.stp)")
    if not path:
        return None

    try:
        if exporter.format_from_filter(chosen_filter, path) == "STEP":
            exporter.export_to_step(obj, path)
        else:
            linear_dev, angular_dev = settings.deviation()
            exporter.export_to_stl(obj, path, linear_dev, angular_dev)
    except Exception as exc:
        App.Console.PrintError("Make: export failed: %s\n" % exc)
        return None

    settings.set_last_dir(os.path.dirname(path))
    App.Console.PrintMessage(
        "Make: exported '%s' -> %s\n" % (obj.Label, path))
    return path


class ExportCommand:
    """Export the selected body or part to STL."""

    def GetResources(self):
        return {
            "MenuText": "Export",
            "ToolTip": "Export the selected body or part to an STL"
                       " or STEP file.",
            "Pixmap": icon("export_stl.svg"),
        }

    def IsActive(self):
        """Clickable only while a printable object is selected."""
        return any(exporter.has_printable_shape(o)
                   for o in FreeCADGui.Selection.getSelection())

    def Activated(self):
        export_via_dialog()
