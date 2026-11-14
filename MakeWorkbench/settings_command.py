# "Settings" button: dialog for the export quality preset.
# All parameter access goes through settings.py.

import FreeCAD as App
import FreeCADGui
from PySide6 import QtWidgets

from MakeWorkbench import settings


class SettingsCommand:
    """Open the Make workbench settings dialog."""

    def GetResources(self):
        return {
            "MenuText": "Settings",
            "ToolTip": "Export quality and other Make settings.",
        }

    def IsActive(self):
        return True

    def Activated(self):
        dialog = QtWidgets.QDialog(FreeCADGui.getMainWindow())
        dialog.setWindowTitle("Make workbench settings")
        layout = QtWidgets.QFormLayout(dialog)

        # combo pre-set to the stored value; PRESETS order is the
        # display order.
        current = settings.quality_preset()
        combo = QtWidgets.QComboBox(dialog)
        combo.addItems(list(settings.PRESETS))
        combo.setCurrentText(current)
        layout.addRow("Export quality", combo)

        # Standard Qt OK/Cancel pair, wired to close the dialog.
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        # exec() blocks until the user closes the dialog; the return
        # value tells which button was used.
        if dialog.exec() == QtWidgets.QDialog.Accepted:
            settings.set_quality_preset(combo.currentText())
            App.Console.PrintMessage(
                "Make: export quality preset -> %s\n"
                % combo.currentText())
