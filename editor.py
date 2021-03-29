import pygame
import pygame.display
import pygame.draw
import pygame.event
import pygame.time
from pygame import *
from pygame.locals import *

lines = []


screen = pygame.display.set_mode((640, 480))


prog_line = None


clock = pygame.time.Clock()
running = True
while running:
    clock.tick(60)
    pushed = None
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                pushed = (event.pos[0], 480 - event.pos[1])

    if pushed is not None:
        if prog_line is None:
            prog_line = pushed
        else:
            lines.extend(prog_line + pushed)
            prog_line = None

    screen.fill((255, 255, 255))

    for i in range(0, len(lines), 4):
        pygame.draw.line(screen, (96, 96, 255), (lines[i], 480 - lines[i + 1]), (lines[i + 2], 480 - lines[i + 3]), 5)

    pygame.display.update()

print(lines)
