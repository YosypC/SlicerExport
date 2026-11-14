# Loaded automatically by pytest before the tests. Its job: make the
# workbench package importable from the tests, without installing it.
import os
import sys

# This file sits in tests/, so the repo root is one level up.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)
