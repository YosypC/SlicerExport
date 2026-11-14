# FreeCAD entry point, loaded at startup by GUI builds only.
# Keep this thin: all logic lives in the MakeWorkbench package.

import os
import sys

import FreeCAD as App
import FreeCADGui

# The base class is exposed differently across FreeCAD versions.
try:
    from FreeCADGui import Workbench
except ImportError:
    from builtins import Workbench


class MakeWorkbench(Workbench):
    """Quick export of parts and bodies for 3D printing."""

    MenuText = "Make"
    ToolTip = "Export parts and bodies for a 3D printing slicer"

    def Initialize(self):
        """Runs once, on first activation."""
        # This dev build loads InitGui without __file__ (PLAN.md, M0
        # lessons); fall back to the user Mod directory. The workbench
        # must be installed as Mod/MakeWorkbench for that to work.
        if "__file__" in globals():
            mod_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            mod_dir = os.path.join(
                App.getUserAppDataDir(), "Mod", "MakeWorkbench")

        if mod_dir not in sys.path:
            sys.path.insert(0, mod_dir)

        # Import commands here, not at module top (PLAN.md, M0 lessons).
        from MakeWorkbench.hello_command import HelloCommand
        from MakeWorkbench.export_command import ExportCommand
        from MakeWorkbench.print_command import PrintCommand
        from MakeWorkbench.settings_command import SettingsCommand

        # Command names are permanent identifiers; never rename them.
        FreeCADGui.addCommand("Make_ExportSTL", ExportCommand())
        FreeCADGui.addCommand("Make_Print", PrintCommand())
        FreeCADGui.addCommand("Make_Settings", SettingsCommand())
        FreeCADGui.addCommand("Make_Hello", HelloCommand())

        self.appendToolbar(
            "Make tools",
            ["Make_ExportSTL", "Make_Print", "Make_Settings", "Make_Hello"])
        self.appendMenu(
            "Make", ["Make_ExportSTL", "Make_Print", "Make_Settings",
                     "Make_Hello"])

        App.Console.PrintMessage("Make workbench initialized.\n")

    def Activated(self):
        pass

    def Deactivated(self):
        pass


FreeCADGui.addWorkbench(MakeWorkbench())
