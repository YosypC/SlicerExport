# MakeWorkbench/hello_command.py
#
# A "command" in FreeCAD is an object like HelloCommand below that
# describes a button: its text, its tooltip, and what happens when it
# is clicked (Activated). FreeCAD needs nothing more - addCommand()
# in InitGui.py turns it into a toolbar/menu button.
#
# This command is a placeholder for milestone M0: it only prints a
# message, proving that registration, toolbar and click all work.
# It gets replaced by the real export command in M1.

import FreeCAD as App


class HelloCommand:
    """M0 smoke-test button: prints a message to the console."""

    def GetResources(self):
        """Metadata for the button. Returns a plain dictionary."""
        return {
            "MenuText": "Hello (workbench test)",
            "ToolTip": "M0 test button - prints a message to the console"
                       " and does nothing else.",
            # No "Pixmap" yet: FreeCAD shows a plain button without one.
            # Icons come with the M4 polish milestone.
            "Accel": "",
        }

    def IsActive(self):
        """FreeCAD calls this constantly to decide if the button is
        clickable (enabled). Returning True means "always available".
        The future export command will return False when nothing is
        selected, which greys the button out.
        """
        return True

    def Activated(self):
        """Called when the user clicks the button."""
        App.Console.PrintMessage(
            "Hello from the Make workbench - plumbing works.\n"
        )
