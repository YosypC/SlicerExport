# Pure export logic: object -> STL/STEP on disk. No GUI code here
# (PLAN.md, N3).

# NOTE: MeshPart and Part are imported inside the functions that need
# them, not at module top: they only exist inside FreeCAD, and
# top-level imports would break the plain-Python tests in tests/
# (PLAN.md, testing layer 1).

import os


def has_printable_shape(obj):
    """True if obj carries at least one solid (Body, Part feature...)."""
    if not hasattr(obj, "Shape"):
        return False
    shape = obj.Shape
    if shape is None or shape.isNull():
        return False
    return len(shape.Solids) > 0


def default_filename(obj):
    """Derive a safe '.stl' filename from the object's label."""
    forbidden = '\\/:*?"<>|'
    clean = "".join("_" if ch in forbidden else ch for ch in obj.Label)
    return clean.strip() or "part"


def export_to_stl(obj, path, linear_dev, angular_dev):
    """Mesh obj and write it to path as STL. Raises on failure.

    linear_dev [mm] and angular_dev [rad] are the OCC deflections;
    settings.py supplies them from the quality presets (PLAN.md, R2).
    """
    import MeshPart
    mesh = MeshPart.meshFromShape(Shape=obj.Shape,
                                  LinearDeflection=linear_dev,
                                  AngularDeflection=angular_dev,
                                  Relative=False)
    mesh.write(path)
    return path


def export_to_step(obj, path):
    """Write obj's exact geometry to path as STEP. Raises on failure.

    STEP carries the true curved surfaces (B-rep), not a triangle
    mesh - so the quality presets do not apply (PLAN.md, R2).
    """
    import Part
    obj.Shape.exportStep(path)
    return path


def format_from_filter(selected_filter, path):
    """'STEP' or 'STL', based on the save dialog's chosen filter.

    The filter text is authoritative ("STEP (*.step *.stp)" etc.);
    the file extension is only consulted when the filter is empty.
    """
    chosen = (selected_filter or "").lower()
    if "step" in chosen or ".stp" in chosen:
        return "STEP"
    if "stl" in chosen:
        return "STL"
    extension = os.path.splitext(path)[1].lower()
    return "STEP" if extension in (".step", ".stp") else "STL"
