# M0 placeholder button. Kept as a smoke test of the toolbar plumbing.

import FreeCAD as App


class HelloCommand:
    """Prints one message to the console."""

    def GetResources(self):
        return {
            "MenuText": "Hello (workbench test)",
            "ToolTip": "Test button - prints a message, does nothing else.",
        }

    def IsActive(self):
        return True

    def Activated(self):
        App.Console.PrintMessage(
            "Hello from the Make workbench - plumbing works.\n")
