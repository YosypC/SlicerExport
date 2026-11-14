# Pure export logic: object -> STL on disk. No GUI code here (PLAN.md, N3).

# NOTE: MeshPart is imported inside export_to_stl, not at module top:
# it only exists inside FreeCAD, and a top-level import would break
# the plain-Python tests in tests/ (PLAN.md, testing layer 1).


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
