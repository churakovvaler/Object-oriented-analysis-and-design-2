import pygame
from config import FONT

class Button:
    def __init__(self, text, x, y, w, h):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=6)

        text = FONT.render(self.text, True, (0, 0, 0))
        screen.blit(text, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)