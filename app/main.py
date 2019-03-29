import pygame
import random as r
from app.handler import *
import numpy as np

weights = np.random.random((15, 20))
print(weights)
print(weights[len(weights)-1][len(weights[0])-1])


handler = Handler.get_instance()

pygame.init()

window = handler.start()

while handler.is_running:
    pygame.time.delay(handler.run_speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            handler.is_running = False

    window.fill((0, 0, 0))
    handler.update(pygame.key.get_pressed())
    handler.next_frame(window)

pygame.quit()
