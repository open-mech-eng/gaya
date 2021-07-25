from typing import List, Tuple, cast
import cadquery as cq

from types import MappingProxyType
from examples.spindle_assembly.clamp import Clamp


class Bracket:
    def __init__(
        self,
        *,
        width: float = 100,
        height: float = 95,
        thickness: float = 13,
        clamp: Clamp,
        tee_nut_spacing: float = 30,
        hole_diameter: float = 8,
        vslot_face_to_top_measurement: float = (10.4 + 0.6)
    ):
        self.dimensions: MappingProxyType[str, float] = MappingProxyType(
            {
                "width": width,
                "height": height,
                "thickness": thickness,
                "tee_nut_spacing": tee_nut_spacing,
                "vslot_face_to_top_measurement": vslot_face_to_top_measurement,
            }
        )

        v_slot_x = [(-1.5 + idx) * 20 for idx in [0, 3]]
        tee_nut_holes_y = [
            (idx - 1) * self.dimensions["tee_nut_spacing"] for idx in range(3)
        ]
        points: List[Tuple[float, float]] = []
        for xval in v_slot_x:
            for yval in tee_nut_holes_y:
                points.append((xval, yval))

        self.geometry = (
            cq.Workplane("XZ")
            .tag("base")
            .box(
                self.dimensions["width"],
                self.dimensions["height"],
                self.dimensions["thickness"],
                centered=(True, True, False),
            )
            .workplaneFromTagged("base")
            .workplane(offset=self.dimensions["thickness"])
            .tag("holeplane")
            .rect(
                xLen=cast(float, clamp.dimensions["bolt_spacing_x"]),
                yLen=cast(float, clamp.dimensions["bolt_spacing_y"]),
                forConstruction=True,
            )
            .vertices()
            .hole(hole_diameter)
            .pushPoints(points)
            .cboreHole(
                5 * 1.2,
                10,
                self.dimensions["thickness"]
                - self.dimensions["vslot_face_to_top_measurement"],
            )
            .faces(">Y")
            .edges("|Z")
            .chamfer(5)
        )
