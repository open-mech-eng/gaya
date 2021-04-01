import cadquery as cq


class SpindleAssemby(cq.Assembly):
    def __init__(
        self,
        *
        ,
        obj: cq.AssemblyObjects = None,
        loc: cq.Optional[cq.Location] = None,
        name: cq.Optional[str] = None,
        color: cq.Optional[cq.Color] = None,
    ):
        super().__init__(obj=obj, loc=loc, name=name, color=color)
