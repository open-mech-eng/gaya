from typing import Tuple
import cadquery as cq
from types import MappingProxyType


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
        z: float = 62.1
    ) -> None:
        self.dimensions: MappingProxyType = MappingProxyType(
            {
                "bolt_spacing_x": bolt_spacing_x,
                "bolt_spacing_y": bolt_spacing_y,
                "bolt_stickout": bolt_stickout,
                "bolt_thread": bolt_thread,
                "x": x,
                "y": y,
                "z": z,
            }
        )
        self.geometry: cq.Workplane = None
