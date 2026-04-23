import pygame
from config import WIDTH
from game.logic import create_deck, calculate_score
from game.round_template import RoundTemplate
from game.blackjack_round import BlackjackRound
from ui.render import draw_text, draw_center_text, draw_hand, draw_slots
from ui.panel import draw_panel
from ui.button import Button

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.reset()
        self.round: RoundTemplate

    def reset(self):
        self.deck = create_deck()
        self.player = []
        self.dealer = []
        self.stack = 0
        self.bet = 0
        self.state = "start"
        self.message = ""

        self.round = BlackjackRound(self)

        self.stack_buttons = [
            Button("100",300,250,100,60),
            Button("300",420,250,100,60),
            Button("500",540,250,100,60),
            Button("1000",660,250,100,60),
        ]

        self.bet_buttons = [Button(x,0,0,80,40) for x in ["10%","20%","50%","100%"]]
        self.hit = Button("HIT",0,0,100,50)
        self.stand = Button("STAND",0,0,120,50)
        self.restart = Button("RESTART",0,0,150,50)

    def handle_click(self, pos):
        if self.state == "start":
            for b in self.stack_buttons:
                if b.is_clicked(pos):
                    self.stack = int(b.text)
                    self.state = "betting"

        elif self.state == "betting":
            for i,b in enumerate(self.bet_buttons):
                if b.is_clicked(pos):
                    self.bet = int(self.stack * [0.1,0.2,0.5,1][i])
                    self.round.deal_cards()

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
                self.player = []
                self.dealer = []
                self.bet = 0
                self.state = "betting" if self.stack > 0 else "game_over"

        elif self.state == "game_over":
            if self.restart.is_clicked(pos):
                self.reset()

    def update(self):
        if self.state == "dealer":
            self.round.dealer_turn()
            self.round.resolve_round()
            self.state = "end"

    def draw(self):
        self.screen.fill((0,100,0))

        if self.state == "start":
            draw_center_text(self.screen,"Выбери стек")
            for b in self.stack_buttons:
                b.draw(self.screen)

        elif self.state == "game_over":
            draw_center_text(self.screen,"СТЕК 0! ИДИ В ЛОМБАРД!")
            self.restart.draw(self.screen)

        else:
            hide = self.state == "player"

            draw_text(self.screen,"Дилер", WIDTH//2-40,40)
            draw_slots(self.screen,len(self.dealer),70)
            draw_hand(self.screen,self.dealer,70,hide_first=hide)

            draw_text(self.screen,"Игрок", WIDTH//2-40,330)
            draw_slots(self.screen,len(self.player),360)
            draw_hand(self.screen,self.player,360)

            if self.player:
                scores = calculate_score(self.player)
                draw_text(self.screen," / ".join(map(str,scores)),WIDTH//2-30,520)

            if self.state == "end":
                draw_center_text(self.screen,self.message,-80)

            draw_panel(self.screen,self.stack,self.bet,self.state,
                       self.bet_buttons,self.hit,self.stand,self.restart)