import cadquery as cq


class VSlot:
    def __init__(
        self,
        *,
        outer_x: float,
        outer_y: float,
        base_depth: float,
        c_beam_dxf_profile_loc: str = "C-Beam-DXF.dxf",
        slot_length: float
    ):
        imported_profile = (
            cq.importers.importDXF(c_beam_dxf_profile_loc)
            .translate((0, base_depth, 0))
            .wires()
            .toPending()
            .extrude(slot_length)
        )

        part = (
            cq.Workplane()
            .tag("base")
            .box(outer_x, base_depth, slot_length, centered=(True, False, False))
            .workplaneFromTagged("base")
            .center(outer_x / 2 - base_depth / 2, 0)
            .box(base_depth, outer_y, slot_length, centered=(True, False, False))
            .workplaneFromTagged("base")
            .center(-outer_x / 2 + base_depth / 2, 0)
            .box(base_depth, outer_y, slot_length, centered=(True, False, False))
            .tag("unslotted")
        )
        self.geometry = part.newObject(imported_profile.objects)
