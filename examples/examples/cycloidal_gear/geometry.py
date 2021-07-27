from typing import Tuple
import cadquery as cq
from math import sin, cos, pi, floor

# define the generating function
def hypocycloid(t: float, r1: float, r2: float) -> Tuple[float, float]:
    return (
        (r1 - r2) * cos(t) + r2 * cos(r1 / r2 * t - t),
        (r1 - r2) * sin(t) + r2 * sin(-(r1 / r2 * t - t)),
    )


def epicycloid(t: float, r1: float, r2: float) -> Tuple[float, float]:
    return (
        (r1 + r2) * cos(t) - r2 * cos(r1 / r2 * t + t),
        (r1 + r2) * sin(t) - r2 * sin(r1 / r2 * t + t),
    )


def gear(t: float, r1: float = 4, r2: float = 1) -> Tuple[float, float]:
    if (-1) ** (1 + floor(t / 2 / pi * (r1 / r2))) < 0:
        return epicycloid(t, r1, r2)
    else:
        return hypocycloid(t, r1, r2)


def generate_geometry() -> cq.Workplane:
    return (
        cq.Workplane("XY")
        .parametricCurve(lambda t: gear(t * 2 * pi, 6, 1))
        .twistExtrude(15, 90)
        .faces(">Z")
        .workplane()
        .circle(2)
        .cutThruAll()
    )
