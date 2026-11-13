# Pure export logic: object -> STL on disk. No GUI code here (PLAN.md, N3).

import Mesh


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


def export_to_stl(obj, path, deviation=0.1):
    """Mesh obj and write it to path as STL. Raises on failure.

    deviation is the tessellation tolerance in mm. The R2 quality
    presets (PLAN.md) replace it in M2; they need MeshPart.meshFromShape
    for separate linear/angular control.
    """
    Mesh.export([obj], path, deviation)
    return path
