# InitGui.py
#
# This file is the entry point FreeCAD reads when it starts up.
# Any folder in FreeCAD's "Mod" directory that contains an InitGui.py
# is treated as a workbench.
#
# InitGui.py is ONLY loaded when FreeCAD runs with its graphical
# interface ("FreeCAD.exe"). The headless "FreeCADCmd.exe" skips it
# entirely. Because of that, this file must stay thin: everything that
# can be tested without a window lives in the MakeWorkbench package,
# and only the registration of the workbench happens here.

import os
import sys

import FreeCAD as App      # FreeCAD core: documents, objects, console
import FreeCADGui          # FreeCAD GUI: windows, toolbars, commands

# Every workbench inherits from the class Workbench. Where it lives
# depends on the FreeCAD version: some expose it in FreeCADGui, older
# versions inject it as a builtin. Try both; one of them always works.
try:
    from FreeCADGui import Workbench
except ImportError:
    from builtins import Workbench


class MakeWorkbench(Workbench):
    """The Make workbench: quick export of bodies for 3D printing.

    The class NAME is the internal identifier FreeCAD uses for the
    workbench ("MakeWorkbench"). The attributes below are what the
    user actually sees in the dropdown and menus.
    """

    MenuText = "Make"   # shown in the workbench dropdown
    ToolTip = "Export parts and bodies for a 3D printing slicer"

    def Initialize(self):
        """Called once, the first time this workbench is activated."""
        # Make the folder this file lives in importable.
        #
        # Normally __file__ (the path of InitGui.py itself) tells us
        # where that is. Some FreeCAD builds load InitGui.py in a
        # namespace where __file__ does not exist - so we fall back
        # to FreeCAD's own user directory, where the workbench is
        # installed as Mod/MakeWorkbench.
        if "__file__" in globals():
            mod_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            mod_dir = os.path.join(
                App.getUserAppDataDir(), "Mod", "MakeWorkbench")

        # Put that folder at the FRONT of sys.path (position 0) so
        # our MakeWorkbench package is found before anything similar.
        if mod_dir not in sys.path:
            sys.path.insert(0, mod_dir)

        # Import the command here - inside Initialize - not at the top
        # of the file. Some FreeCAD builds load InitGui.py in a way
        # where top-level imports of sibling modules do not reach the
        # code that runs later. All mature workbenches import their
        # commands exactly like this.
        from MakeWorkbench.hello_command import HelloCommand
        from MakeWorkbench.export_command import ExportCommand

        # "Make_ExportSTL" and "Make_Hello" are the permanent command
        # names. FreeCAD uses them in toolbars, menus and saved
        # settings, so never change them once released.
        FreeCADGui.addCommand("Make_ExportSTL", ExportCommand())
        FreeCADGui.addCommand("Make_Hello", HelloCommand())

        # A toolbar with both buttons, and the same under a
        # "Make" top menu.
        self.appendToolbar("Make tools", ["Make_ExportSTL", "Make_Hello"])
        self.appendMenu("Make", ["Make_ExportSTL", "Make_Hello"])

        App.Console.PrintMessage(
            "Make workbench initialized. It has no features yet - "
            "see PLAN.md for the roadmap.\n"
        )

    def Activated(self):
        """Called every time the user switches to this workbench."""
        pass

    def Deactivated(self):
        """Called when the user switches away."""
        pass


# Register the workbench with FreeCAD.
# In a live FreeCAD this happens automatically at startup, because
# FreeCAD imports every Mod/<name>/InitGui.py it can find.
FreeCADGui.addWorkbench(MakeWorkbench())
