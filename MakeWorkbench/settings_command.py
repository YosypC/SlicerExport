# "Settings" button: dialog for the export quality preset.
# All parameter access goes through settings.py.

import FreeCAD as App
import FreeCADGui
from PySide6 import QtWidgets

from MakeWorkbench import settings
from MakeWorkbench import icon


class SettingsCommand:
    """Open the Make workbench settings dialog."""

    def GetResources(self):
        return {
            "MenuText": "Settings",
            "ToolTip": "Export quality and other Make settings.",
            "Pixmap": icon("settings.svg"),
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
        layout.addRow("Export quality (STL only)", combo)

        # Slicer executable: launching after export is off while empty.
        slicer_edit = QtWidgets.QLineEdit(settings.slicer_path(), dialog)
        # QToolButton, not QPushButton: FreeCAD's global stylesheet
        # forces QPushButton to min-width 80px, which beats any fixed
        # width we set. QToolButton is FreeCAD's small utility button.
        browse = QtWidgets.QToolButton(dialog)
        browse.setText("...")
        browse.setFixedWidth(22)
        browse.clicked.connect(
            lambda: slicer_edit.setText(_browse_executable(dialog)))
        path_row = QtWidgets.QHBoxLayout()
        path_row.addWidget(slicer_edit)
        path_row.addWidget(browse)
        layout.addRow("Slicer executable (optional)", path_row)

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
            settings.set_slicer_path(slicer_edit.text().strip())
            App.Console.PrintMessage(
                "Make: settings saved\n")


def _browse_executable(dialog):
    """File picker for the slicer executable; empty on cancel."""
    path, _ = QtWidgets.QFileDialog.getOpenFileName(
        dialog, "Choose slicer executable", "", "Executable (*.exe)")
    return path
