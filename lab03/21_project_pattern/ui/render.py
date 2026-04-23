import pygame
import os
from config import WIDTH, HEIGHT, CARD_WIDTH, CARD_HEIGHT, FONT, BIG_FONT, ASSET_PATH

def draw_text(screen, text, x, y):
    img = FONT.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

def draw_center_text(screen, text, offset_y=0):
    img = BIG_FONT.render(text, True, (255, 255, 0))
    rect = img.get_rect(center=(WIDTH // 2, HEIGHT // 2 + offset_y))
    screen.blit(img, rect)

def load_card(card):
    rank, suit = card
    path = os.path.join(ASSET_PATH, f"{rank}_of_{suit}.png")
    img = pygame.image.load(path)
    return pygame.transform.scale(img, (CARD_WIDTH, CARD_HEIGHT))

def draw_hand(screen, hand, y, hide_first=False):
    start_x = WIDTH // 2 - (len(hand) * 90) // 2

    for i, card in enumerate(hand):
        x = start_x + i * 90

        # 👇 скрытая первая карта дилера
        if hide_first and i == 0:
            pygame.draw.rect(screen, (0, 0, 150),
                             (x, y, CARD_WIDTH, CARD_HEIGHT),
                             border_radius=8)
            pygame.draw.rect(screen, (255, 255, 255),
                             (x, y, CARD_WIDTH, CARD_HEIGHT), 2,
                             border_radius=8)
        else:
            img = load_card(card)
            screen.blit(img, (x, y))

def draw_slots(screen, count, y):
    start_x = WIDTH // 2 - (count * 90) // 2

    for i in range(count):
        rect = pygame.Rect(start_x + i * 90, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)