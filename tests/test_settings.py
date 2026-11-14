# Layer 1 tests for SlicerExport/settings.py.
# Only the parts that do not touch FreeCAD's parameter system:
# those would need FreeCAD running (testing layer 2, PLAN.md).

import pytest

from SlicerExport import settings


# --- preset validation --------------------------------------------

def test_all_presets_have_two_values():
    for name, values in settings.PRESETS.items():
        assert isinstance(values, tuple) and len(values) == 2, name

def test_unknown_preset_is_rejected():
    with pytest.raises(ValueError):
        settings.set_quality_preset("Bogus")

def test_deviation_returns_preset_pair():
    # exact numbers from the M1 benchmark (PLAN.md, R2)
    assert settings.deviation("Coarse") == (0.20, 0.50)
    assert settings.deviation("Standard") == (0.05, 0.35)
    assert settings.deviation("Fine") == (0.01, 0.10)

def test_deviation_with_unknown_preset_raises():
    with pytest.raises(KeyError):
        settings.deviation("Bogus")


# --- send format --------------------------------------------------

def test_send_formats_are_stl_and_step():
    assert settings.SEND_FORMATS == ("STL", "STEP")

def test_unknown_send_format_is_rejected():
    with pytest.raises(ValueError):
        settings.set_send_format("Bogus")
