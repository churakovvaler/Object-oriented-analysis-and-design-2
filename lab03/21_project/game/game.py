import pygame
from config import WIDTH, HEIGHT
from game.logic import create_deck, calculate_score
from ui.render import draw_text, draw_center_text, draw_hand, draw_slots
from ui.panel import draw_panel
from ui.button import Button


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.reset()

    def reset(self):
        self.deck = create_deck()
        self.player = []
        self.dealer = []

        self.stack = 0
        self.bet = 0

        self.state = "start"
        self.message = ""

        # кнопки
        self.stack_buttons = [
            Button("100", 300, 250, 100, 60),
            Button("300", 420, 250, 100, 60),
            Button("500", 540, 250, 100, 60),
            Button("1000", 660, 250, 100, 60),
        ]

        self.bet_buttons = [
            Button("10%", 0, 0, 80, 40),
            Button("20%", 0, 0, 80, 40),
            Button("50%", 0, 0, 80, 40),
            Button("100%", 0, 0, 80, 40),
        ]

        self.hit = Button("HIT", 0, 0, 100, 50)
        self.stand = Button("STAND", 0, 0, 120, 50)
        self.restart = Button("RESTART", 0, 0, 150, 50)

    # -----------------------------
    # КЛИКИ
    # -----------------------------
    def handle_click(self, pos):
        if self.state == "start":
            for b in self.stack_buttons:
                if b.is_clicked(pos):
                    self.stack = int(b.text)
                    self.state = "betting"

        elif self.state == "betting":
            for i, b in enumerate(self.bet_buttons):
                if b.is_clicked(pos):
                    self.bet = int(self.stack * [0.1, 0.2, 0.5, 1.0][i])

                    # 🎴 раздача
                    self.player = [self.deck.pop(), self.deck.pop()]
                    self.dealer = [self.deck.pop(), self.deck.pop()]

                    player_scores = calculate_score(self.player)
                    dealer_scores = calculate_score(self.dealer)

                    player_blackjack = (len(self.player) == 2 and 21 in player_scores)
                    dealer_blackjack = (len(self.dealer) == 2 and 21 in dealer_scores)

                    # 🎯 обработка blackjack
                    if player_blackjack and dealer_blackjack:
                        self.message = "Ничья (Blackjack)"
                        self.state = "end"

                    elif player_blackjack:
                        self.stack += int(self.bet * 1.5)
                        self.message = "BLACKJACK!"
                        self.state = "end"

                    elif dealer_blackjack:
                        self.stack -= self.bet
                        self.message = "У дилера Blackjack!"
                        self.state = "end"

                    else:
                        self.state = "player"

        elif self.state == "player":
            if self.hit.is_clicked(pos):
                self.player.append(self.deck.pop())

                if min(calculate_score(self.player)) > 21:
                    self.stack -= self.bet
                    self.message = "Перебор!"
                    self.state = "end"

            if self.stand.is_clicked(pos):
                self.state = "dealer"

        elif self.state == "end":
            if self.restart.is_clicked(pos):

                if self.stack <= 0:
                    self.state = "game_over"
                else:
                    self.state = "betting"

                # очистка стола
                self.player = []
                self.dealer = []
                self.bet = 0
                self.message = ""

        elif self.state == "game_over":
            if self.restart.is_clicked(pos):
                self.reset()

    # -----------------------------
    # ЛОГИКА
    # -----------------------------
    def update(self):
        if self.state == "dealer":
            if max(calculate_score(self.dealer)) < 17:
                self.dealer.append(self.deck.pop())
            else:
                player_best = max(
                    [s for s in calculate_score(self.player) if s <= 21],
                    default=0
                )
                dealer_best = max(
                    [s for s in calculate_score(self.dealer) if s <= 21],
                    default=0
                )

                if dealer_best > 21 or player_best > dealer_best:
                    self.stack += self.bet
                    self.message = "Ты выиграл!"
                elif player_best == dealer_best:
                    self.message = "Ничья"
                else:
                    self.stack -= self.bet
                    self.message = "Ты проиграл"

                self.state = "end"

    # -----------------------------
    # ОТРИСОВКА
    # -----------------------------
    def draw(self):
        self.screen.fill((0, 100, 0))

        if self.state == "start":
            draw_center_text(self.screen, "Выбери стек")
            for b in self.stack_buttons:
                b.draw(self.screen)

        elif self.state == "game_over":
            draw_center_text(self.screen, "СТЕК 0! ИДИ В ЛОМБАРД 💀")
            self.restart.draw(self.screen)

        else:
            hide = self.state == "player"

            # дилер
            draw_text(self.screen, "Дилер", WIDTH // 2 - 40, 40)
            draw_slots(self.screen, len(self.dealer), 70)
            draw_hand(self.screen, self.dealer, 70, hide_first=hide)

            # очки дилера
            if self.dealer:
                if self.state == "player":
                    visible = [self.dealer[1]]
                    score = calculate_score(visible)
                    draw_text(self.screen, f"{score[0]} + ?", WIDTH // 2 - 20, 200)
                else:
                    scores = calculate_score(self.dealer)
                    draw_text(self.screen, " / ".join(map(str, scores)), WIDTH // 2 - 20, 200)

            # игрок
            draw_text(self.screen, "Игрок", WIDTH // 2 - 40, 330)
            draw_slots(self.screen, len(self.player), 360)
            draw_hand(self.screen, self.player, 360)

            # очки игрока
            if self.player:
                scores = calculate_score(self.player)
                draw_text(self.screen, " / ".join(map(str, scores)), WIDTH // 2 - 30, 520)

            if self.state == "end":
                draw_center_text(self.screen, self.message, -80)

            draw_panel(
                self.screen,
                self.stack,
                self.bet,
                self.state,
                self.bet_buttons,
                self.hit,
                self.stand,
                self.restart
            )