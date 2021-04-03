from types import MappingProxyType
import cadquery as cq
from examples.spindle_assembly.bracket import Bracket
from examples.spindle_assembly.clamp import Clamp
from examples.spindle_assembly.spindle import Spindle

from examples.spindle_assembly.vslot import VSlot


class SpindleAssembly:
    def __init__(self, *, vslot_dxf_profile_location: str):
        self.dimensions: MappingProxyType = MappingProxyType({})
        back = VSlot(
            outer_x=80,
            outer_y=40,
            base_depth=20,
            slot_length=250,
            c_beam_dxf_profile_loc=vslot_dxf_profile_location,
        )

        clamp = Clamp()
        bracket = Bracket(clamp=clamp)
        spindle = Spindle()

        bottom_of_vslot_to_bottom_of_bracket = (
            -6
            + spindle.dimensions["nut_length"]
            + spindle.dimensions["shaft_length"]
            + spindle.dimensions["bearing_cap_height"]
            + spindle.dimensions["body_clamp_end_offset"]
            + clamp.dimensions["z"] / 2
            - bracket.dimensions["height"] / 2
        )

        backpoint = (
            back.geometry.faces("<Z", tag="unslotted")
            .edges("<Y")
            .translate((0, 0, bottom_of_vslot_to_bottom_of_bracket))
            .val()
        )
        bracketpoint = bracket.geometry.faces("<Z").edges(">Y").val()

        self.geometry = (
            cq.Assembly(name="SpindleAssembly")
            .add(
                back.geometry,
                name="back",
                color=cq.Color(0.8, 0.8, 0.8),
            )
            .add(bracket.geometry, name="bracket", color=cq.Color(0.9, 0.9, 0.95))
            .constrain("back", backpoint, "bracket", bracketpoint, "Point")
            .constrain(
                "back",
                back.geometry.faces("<Y", tag="unslotted").val(),
                "bracket",
                bracket.geometry.faces(">Y").val(),
                "Axis",
            )
            .constrain(
                "back",
                back.geometry.faces("<Z", tag="unslotted").val(),
                "bracket",
                bracket.geometry.faces(">Z").val(),
                "Axis",
            )
            .solve()
        )
