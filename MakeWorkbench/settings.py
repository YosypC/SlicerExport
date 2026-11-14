# User settings, stored in FreeCAD's parameter system (persists across
# restarts, per user - not per document). Keys live under
# "User parameter:BaseApp/Preferences/MakeWorkbench".

import FreeCAD as App

# Preset -> (LinearDeflection, AngularDeflection); values locked by the
# M1 benchmark (PLAN.md, requirement R2).
PRESETS = {
    "Coarse":   (0.20, 0.50),
    "Standard": (0.05, 0.35),
    "Fine":     (0.01, 0.10),
}
DEFAULT_PRESET = "Standard"


def _params():
    return App.ParamGet(
        "User parameter:BaseApp/Preferences/MakeWorkbench")


def quality_preset():
    """The stored preset name, falling back to the default if missing
    or unknown."""
    name = _params().GetString("QualityPreset", DEFAULT_PRESET)
    return name if name in PRESETS else DEFAULT_PRESET


def set_quality_preset(name):
    """Store the preset name; refuses names that are not in PRESETS."""
    if name not in PRESETS:
        raise ValueError("unknown quality preset: %r" % name)
    _params().SetString("QualityPreset", name)


def deviation(preset=None):
    """(LinearDeflection, AngularDeflection) for a preset.
    Called without arguments: the user's stored preset."""
    return PRESETS[preset or quality_preset()]


def last_dir():
    """Last folder exported to ('' if none yet)."""
    return _params().GetString("LastExportDir", "")


def set_last_dir(path):
    """Remember the folder of the last successful export."""
    _params().SetString("LastExportDir", path)


def slicer_path():
    """Configured slicer executable ('' -> launch after export off)."""
    return _params().GetString("SlicerPath", "")


def set_slicer_path(path):
    """Store the slicer executable path. Empty disables launching."""
    _params().SetString("SlicerPath", path)
