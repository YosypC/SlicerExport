# Launch the configured slicer executable with an exported file.
# Pure logic, no GUI (PLAN.md, N3).

import subprocess


def launch(executable, file_to_open):
    """Start executable with file_to_open as its argument.

    Does not wait for the slicer to exit. Raises FileNotFoundError
    if the executable does not exist.
    """
    return subprocess.Popen([executable, file_to_open])
