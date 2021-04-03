import cadquery as cq

from types import MappingProxyType


class Spindle:
    def __init__(
        self,
        *,
        nut_length: float = 12,
        shaft_length: float = 15,
        bearing_cap_height: float = 5.1,
        body_clamp_end_offset: float = 16
    ) -> None:
        self.dimensions: MappingProxyType = MappingProxyType(
            {
                "nut_length": nut_length,
                "shaft_length": shaft_length,
                "bearing_cap_height": bearing_cap_height,
                "body_clamp_end_offset": body_clamp_end_offset,
            }
        )
        self.geometry: cq.Workplane = None
