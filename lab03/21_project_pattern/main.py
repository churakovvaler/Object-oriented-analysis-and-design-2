import pygame
from config import WIDTH, HEIGHT
from game.game import Game

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

game = Game(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game.handle_click(event.pos)

    game.update()
    game.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()