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

while running:
    globvars.delta_time = clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    screen.fill((255, 255, 255))

    client.handle()
    client.player.render()

    pygame.display.update()
