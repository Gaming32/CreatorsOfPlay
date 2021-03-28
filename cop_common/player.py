from pymunk import Vec2d
from pymunk.body import Body
from pymunk.constraints import PinJoint


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

    body: Body
    joint: PinJoint

    def __init__(self) -> None:
        self.joints = [Vec2d(0, 0) for _ in range(7)]
        self.body = None # Initialized by server, not used on client
        self.joint = None # Initialized by server, not used on client
