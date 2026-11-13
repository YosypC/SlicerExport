# MakeWorkbench package
#
# A Python "package" is just a folder whose modules (files) can be
# imported by other code, e.g. "from MakeWorkbench.hello_command import
# HelloCommand". The __init__.py file is what turns the folder into a
# package - it can stay (almost) empty.
#
# Design rule for this package (see PLAN.md, N3): only InitGui.py and
# task_panel.py may touch FreeCAD's GUI. Everything else is plain,
# testable logic.
