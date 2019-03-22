import pygame
from app.handler import *

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
    pygame.draw.rect(window, (255, 0, 0), (50, 50, 10, 10))
    handler.next_frame(window)


pygame.quit()
