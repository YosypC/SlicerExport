# SlicerExport package
#
# A Python "package" is a folder whose modules (files) can be
# imported by other code, e.g. "from SlicerExport.export_command
# import ExportCommand". The __init__.py file is what turns the
# folder into a package - it can stay (almost) empty.
#
# Design rule for this package (see PLAN.md, N3): only InitGui.py and
# the *_command.py files may touch FreeCAD's GUI. Everything else is
# plain, testable logic.

import os


def icon(name):
    """Absolute path to an icon in Resources/icons, or '' if missing.

    __file__ is this file's own path; two dirname()s climb from
    SlicerExport/ up to the workbench root where Resources/ lives.
    The path is stored, so a missing icon simply means no picture -
    FreeCAD then shows a text-only button instead of an error.
    """
    path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Resources", "icons", name)
    return path if os.path.exists(path) else ""
