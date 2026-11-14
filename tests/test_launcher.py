# Layer 1 tests for MakeWorkbench/launcher.py.
# Cross-platform: uses Python itself as the launched process, so no
# Windows-only executables are involved.

import sys

import pytest

from MakeWorkbench import launcher


def test_missing_executable_raises():
    # FileNotFound, not a silent success or a hang
    with pytest.raises(FileNotFoundError):
        launcher.launch(r"C:\does-not-exist\nope.exe", "file.stl")

def test_launches_and_does_not_wait():
    # launch the test run's own Python with '-V' (print version,
    # exit 0); wait() is OUR choice, meaning launch() returned early.
    proc = launcher.launch(sys.executable, "-V")
    assert proc.wait(timeout=10) == 0
