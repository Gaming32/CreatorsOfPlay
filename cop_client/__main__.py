from cop_client.player import draw_vec2d_pair
import logging

from pymunk.vec2d import Vec2d

from cop_client import globvars
from cop_client.client import Client
from cop_client.consts import FRAMERATE
from cop_client.pygame_import import *
from cop_common.network import DEFAULT_PORT

pygame.init()


logging.basicConfig(
        format='[%(asctime)s] [%(threadName)s/%(levelname)s] [%(filename)s:%(lineno)i]: %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO
    )


screen = pygame.display.set_mode((640, 480))
globvars.screen = screen


clock = pygame.time.Clock()


client = Client()
client.connect('localhost', DEFAULT_PORT)


globvars.camera = Vec2d(-320, -240)


running = True

SPEED = 5000

while running:
    movement = None
    globvars.delta_time = clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                movement = Vec2d(0, SPEED)
            elif event.key == K_LEFT:
                movement = Vec2d(-SPEED, 0)
            elif event.key == K_RIGHT:
                movement = Vec2d(SPEED, 0)
            elif event.key == K_DOWN:
                movement = Vec2d(0, -SPEED)
    
    screen.fill((255, 255, 255))

    client.handle()

    if movement is not None:
        # client.move(movement)
        client.move(Vec2d(10000, 10000))

    lines = client.level['data']
    for i in range(0, len(lines), 4):
        draw_vec2d_pair(Vec2d(lines[i], lines[i + 1]), Vec2d(lines[i + 2], lines[i + 3]))

    client.player.render()

    pygame.display.update()
