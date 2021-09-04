"""
Cadquery Adapters for various functionality
"""
from typing import Union, cast
from cadquery.occ_impl.exporters.json import JsonMesh
from cadquery.occ_impl.exporters.utils import toCompound
import cadquery as cq


def export_json(
    geometry: Union[cq.Shape, cq.Workplane],
    *,
    tolerance: float = 0.1,
    angularTolerance: float = 0.1,
) -> str:
    """
    Export a cadquery object to a JSON string
    """
    shape = toCompound(geometry) if isinstance(geometry, cq.Workplane) else geometry
    tess = shape.tessellate(tolerance, angularTolerance)
    mesher = JsonMesh()

    # add vertices
    for v in tess[0]:
        mesher.addVertex(v.x, v.y, v.z)

    # add triangles
    for ixs in tess[1]:
        mesher.addTriangleFace(*ixs)

    return cast(str, mesher.toJson())
