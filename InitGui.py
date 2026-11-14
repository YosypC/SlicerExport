# FreeCAD entry point, loaded at startup by GUI builds only.
# Keep this thin: all logic lives in the SlicerExport package.
#
# LOADER QUIRK (this dev build, PLAN.md M0 lessons): top-level
# assignments in this file do not reliably reach the class body or
# the methods. Everything the workbench needs elsewhere is computed
# locally, inside the scope that uses it.

import os
import sys

import FreeCAD
import FreeCADGui

# The base class is exposed differently across FreeCAD versions.
try:
    from FreeCADGui import Workbench
except ImportError:
    from builtins import Workbench


class SlicerExport(Workbench):
    """Send bodies and parts to a 3D printing slicer."""

    # The class NAME ("SlicerExport") is the workbench's internal ID.
    MenuText = "Slicer Export"
    ToolTip = "Export parts and bodies for a 3D printing slicer"

    # Workbench icon in the dropdown. Computed inline because module
    # constants are not visible here (loader quirk, see file header).
    try:
        _dir = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        # No __file__ in this build's InitGui namespace.
        import FreeCAD as _App
        _dir = os.path.join(_App.getUserAppDataDir(),
                            "Mod", "SlicerExport")
    _icon = os.path.join(_dir, "Resources", "icons", "slicer_export.svg")
    Icon = _icon if os.path.exists(_icon) else ""

    def Initialize(self):
        """Runs once, on first activation."""
        # Same folder logic as above, recomputed locally.
        try:
            mod_dir = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            import FreeCAD as App
            mod_dir = os.path.join(App.getUserAppDataDir(),
                                   "Mod", "SlicerExport")
        if mod_dir not in sys.path:
            sys.path.insert(0, mod_dir)

        # Import commands here, not at module top (PLAN.md, M0 lessons).
        from SlicerExport.export_command import ExportCommand
        from SlicerExport.print_command import PrintCommand
        from SlicerExport.settings_command import SettingsCommand

        # Command names are permanent identifiers; never rename them.
        FreeCADGui.addCommand("SlicerExport_Export", ExportCommand())
        FreeCADGui.addCommand("SlicerExport_Send", PrintCommand())
        FreeCADGui.addCommand("SlicerExport_Settings", SettingsCommand())

        self.appendToolbar(
            "Slicer Export tools",
            ["SlicerExport_Export", "SlicerExport_Send",
             "SlicerExport_Settings"])
        self.appendMenu(
            "Slicer Export",
            ["SlicerExport_Export", "SlicerExport_Send",
             "SlicerExport_Settings"])

        FreeCAD.Console.PrintMessage(
            "Slicer Export workbench initialized.\n")

    def Activated(self):
        pass

    def Deactivated(self):
        pass


FreeCADGui.addWorkbench(SlicerExport())
