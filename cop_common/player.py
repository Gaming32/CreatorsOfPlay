from pymunk import Vec2d, Segment
from pymunk.body import Body
from pymunk.constraints import PivotJoint


class Player:
    # Joints are as follows:
    # + Torso
    # + Left Foot
    # + Right Foot
    # + Shoulders
    # + Left Hand
    # + Right Hand
    # + Head
    joints: list[Vec2d]

    bodies: list[Body]
    segments: list[Segment]
    pins: list[PivotJoint]

    def __init__(self) -> None:
        self.joints = [Vec2d(0, 0) for _ in range(7)]
        self.bodies = [] # Initialized by server, not used on client
        self.segments = [] # Initialized by server, not used on client
        self.pins = [] # Initialized by server, not used on client
