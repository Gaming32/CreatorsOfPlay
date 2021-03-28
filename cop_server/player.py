from pymunk import Vec2d


class Player:
    joints: list[Vec2d]

    def __init__(self) -> None:
        self.joints = [Vec2d(0, 0) for _ in range(7)]
