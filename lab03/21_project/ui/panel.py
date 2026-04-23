import pygame
from config import HEIGHT
from ui.render import draw_text

def draw_panel(screen, stack, bet, state, bet_buttons, hit, stand, restart):
    panel = pygame.Rect(0, HEIGHT - 120, 1000, 120)
    pygame.draw.rect(screen, (30, 30, 30), panel)

    draw_text(screen, f"Баланс: {stack}", 20, HEIGHT - 100)
    draw_text(screen, f"Ставка: {bet}", 20, HEIGHT - 60)

    if state == "betting":
        for i, b in enumerate(bet_buttons):
            b.rect.x = 250 + i * 110
            b.rect.y = HEIGHT - 80
            b.draw(screen)

    elif state == "player":
        hit.rect.x, hit.rect.y = 250, HEIGHT - 80
        stand.rect.x, stand.rect.y = 380, HEIGHT - 80

        hit.draw(screen)
        stand.draw(screen)


    elif state == "end":
        restart.rect.x, restart.rect.y = 350, HEIGHT - 80
        restart.draw(screen)