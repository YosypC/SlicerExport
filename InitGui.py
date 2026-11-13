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

import FreeCAD as App      # FreeCAD core: documents, objects, console
import FreeCADGui          # FreeCAD GUI: windows, toolbars, commands

# Every workbench inherits from the class Workbench. Where it lives
# depends on the FreeCAD version: some expose it in FreeCADGui, older
# versions inject it as a builtin. Try both; one of them always works.
try:
    from FreeCADGui import Workbench
except ImportError:
    from builtins import Workbench

from MakeWorkbench.hello_command import HelloCommand


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
        # "Make_Hello" is the permanent command name. FreeCAD uses it
        # in toolbars, menus and saved settings, so never change it
        # once released.
        FreeCADGui.addCommand("Make_Hello", HelloCommand())

        # A toolbar with one button, and the same button under a
        # "Make" top menu.
        self.appendToolbar("Make tools", ["Make_Hello"])
        self.appendMenu("Make", ["Make_Hello"])

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
