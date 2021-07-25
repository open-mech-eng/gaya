from typing import List, Union, cast
import cadquery as cq
from types import MappingProxyType

from cadquery.cq import CQObject


class Clamp:
    def __init__(
        self,
        *,
        bolt_stickout: float = 7.1,
        bolt_thread: str = "M8",
        bolt_spacing_x: float = 80,
        bolt_spacing_y: float = 34,
        x: float = 101.5,
        y: float = 78.6,
        z: float = 62.1,
        upper_x: float = 98.3,
        upper_y: float = 40,
        shoulder_outer_x: float = 65 / 2,
        shoulder_inner_x: float = 31 / 2,
        shoulder_delta_y: float = 15.9,
        hole_diameter: float = 62,
        hole_position_x: float = 0,
        hole_position_z: float = 0,
    ) -> None:
        self.dimensions: MappingProxyType[str, Union[float, str]] = MappingProxyType(
            {
                "bolt_spacing_x": bolt_spacing_x,
                "bolt_spacing_y": bolt_spacing_y,
                "bolt_stickout": bolt_stickout,
                "bolt_thread": bolt_thread,
                "x": x,
                "y": y,
                "z": z,
                "upper_x": upper_x,
                "upper_y": upper_y,
                "lower_x": x,
                "lower_y": y - shoulder_delta_y - upper_y,
                "shoulder_outer_x": shoulder_outer_x,
                "shoulder_inner_x": shoulder_inner_x,
                "shoulder_delta_y": shoulder_delta_y,
                "hole_diameter": hole_diameter,
                "hole_position_x": hole_position_x,
                "hole_position_z": hole_position_z,
                "hole_position_y": (70.2 - (hole_diameter / 2) - 3),
            }
        )

        clamp = (
            cq.Workplane()
            .tag("base")
            .box(
                cast(float, self.dimensions["lower_x"]),
                cast(float, self.dimensions["lower_y"]),
                cast(float, self.dimensions["z"]),
                centered=(True, False, True),
            )
            .workplaneFromTagged("base")
            .center(0, cast(float, self.dimensions["lower_y"]))
            .tag("lower")
            .box(
                cast(float, self.dimensions["upper_x"]),
                cast(float, self.dimensions["upper_y"]),
                cast(float, self.dimensions["z"]),
                centered=(True, False, True),
            )
            .workplaneFromTagged("lower")
            .center(0, cast(float, self.dimensions["upper_y"]))
            .vLine(-1)
            .hLine(cast(float, self.dimensions["shoulder_outer_x"]))
            .vLine(1)
            .lineTo(
                cast(float, self.dimensions["shoulder_inner_x"]),
                cast(float, self.dimensions["shoulder_delta_y"]),
            )
            .hLineTo(0)
            .mirrorY()
            .extrude(cast(float, self.dimensions["z"]) / 2, both=True)
        )

        edges: List[CQObject] = []

        for side in [-1, 1]:
            for y0 in [
                0,
                cast(float, self.dimensions["lower_y"]),
                cast(float, self.dimensions["lower_y"])
                + cast(float, self.dimensions["upper_y"]),
            ]:
                edgeToAppend = (
                    clamp.edges("|Z")
                    .edges(
                        cq.NearestToPointSelector(
                            (side * cast(float, self.dimensions["x"]) / 2, y0, 0)
                        )
                    )
                    .val()
                )
                edges.append(edgeToAppend)
        self.geometry: cq.Workplane = (
            clamp.newObject(edges)
            .chamfer(
                cast(float, self.dimensions["lower_x"]) / 2
                - cast(float, self.dimensions["upper_x"]) / 2
                - 1e-3
            )
            .workplaneFromTagged("base")
            .workplane(offset=cast(float, self.dimensions["z"]) / 2 + 1)
            .center(
                cast(float, self.dimensions["hole_position_x"]),
                cast(float, self.dimensions["hole_position_y"]),
            )
            .hole(cast(float, self.dimensions["hole_diameter"]), clean=False)
            .faces("<Y")
            .workplane()
            .rect(
                cast(float, self.dimensions["bolt_spacing_x"]),
                cast(float, self.dimensions["bolt_spacing_y"]),
            )
            .vertices()
            .hole(9.3)
        )
