from cop_client.consts import FRAMERATE
from cop_client.pygame_import import *

pygame.init()


screen = pygame.display.set_mode((640, 480))


clock = pygame.time.Clock()


running = True

while running:
    delta_time = clock.tick(FRAMERATE)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    screen.fill((255, 255, 255))

    pygame.display.update()
