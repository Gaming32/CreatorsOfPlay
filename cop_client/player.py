from pymunk import Vec2d

from cop_client import globvars
from cop_client.pygame_import import *
from cop_common.player import Player


def draw_vec2d_pair(vec1: Vec2d, vec2: Vec2d):
    vec1 = vec1 - globvars.camera
    vec2 = vec2 - globvars.camera
    pygame.draw.line(globvars.screen, (96, 96, 255), (vec1.x, 480 - vec1.y), (vec2.x, 480 - vec2.y), 5)
    # pygame.draw.circle(globvars.screen, (96, 96, 255), (vec1.x, 480 - vec1.y), 30)
    # pygame.draw.circle(globvars.screen, (96, 96, 255), (vec2.x, 480 - vec2.y), 30)


class ClientSidePlayer(Player):
    def render(self):
        draw_vec2d_pair(self.joints[0], self.joints[1])
        draw_vec2d_pair(self.joints[0], self.joints[2])
        draw_vec2d_pair(self.joints[3], self.joints[4])
        draw_vec2d_pair(self.joints[3], self.joints[5])
        draw_vec2d_pair(self.joints[0], self.joints[6])
        head = self.joints[6] - globvars.camera
        pygame.draw.circle(globvars.screen, (96, 96, 255), (head.x, 480 - head.y), 15)
