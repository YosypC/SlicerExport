# Layer 1 tests for MakeWorkbench/exporter.py.
# No FreeCAD here: fakes stand in for its objects.

from MakeWorkbench import exporter


class FakeBody:
    """Stands in for a FreeCAD object: only the attribute used."""
    def __init__(self, label, shape=None, has_shape=True):
        self.Label = label
        if has_shape:
            self.Shape = shape


class FakeShape:
    """Stands in for obj.Shape: what has_printable_shape looks at."""
    def __init__(self, solids, null=False):
        self.Solids = solids
        self._null = null

    def isNull(self):
        return self._null


# --- default_filename ---------------------------------------------

def test_normal_name_unchanged():
    assert exporter.default_filename(FakeBody("Bracket v2")) == "Bracket v2"

def test_forbidden_characters_replaced():
    # every character Windows forbids in a filename
    assert exporter.default_filename(FakeBody('a\\b/c:d*e?f"g<h>i|j')) \
        == "a_b_c_d_e_f_g_h_i_j"

def test_empty_label_falls_back_to_part():
    assert exporter.default_filename(FakeBody("   ")) == "part"

def test_surrounding_spaces_stripped():
    assert exporter.default_filename(FakeBody("  part  ")) == "part"


# --- has_printable_shape ------------------------------------------

def test_object_without_shape_is_not_printable():
    assert exporter.has_printable_shape(FakeBody("x", has_shape=False)) is False

def test_null_shape_is_not_printable():
    body = FakeBody("x", shape=FakeShape(solids=[1], null=True))
    assert exporter.has_printable_shape(body) is False

def test_shape_without_solids_is_not_printable():
    # e.g. a sketch-like object: has a Shape, no solid geometry
    body = FakeBody("x", shape=FakeShape(solids=[]))
    assert exporter.has_printable_shape(body) is False

def test_shape_with_solids_is_printable():
    body = FakeBody("x", shape=FakeShape(solids=[object()]))
    assert exporter.has_printable_shape(body) is True


# --- format_from_filter -------------------------------------------

def test_step_filter_selects_step():
    assert exporter.format_from_filter("STEP (*.step *.stp)",
                                       "part.step") == "STEP"

def test_stl_filter_selects_stl():
    assert exporter.format_from_filter("STL Mesh (*.stl)",
                                       "part.stl") == "STL"

def test_empty_filter_falls_back_to_extension():
    assert exporter.format_from_filter("", "part.stp") == "STEP"
    assert exporter.format_from_filter("", "part.STEP") == "STEP"
    assert exporter.format_from_filter("", "part.stl") == "STL"

def test_no_filter_no_extension_defaults_to_stl():
    assert exporter.format_from_filter("", "part") == "STL"
