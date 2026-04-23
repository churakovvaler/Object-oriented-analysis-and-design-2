from game.round_template import RoundTemplate
from game.logic import calculate_score

class BlackjackRound(RoundTemplate):
    def __init__(self, game):
        self.game = game

    def deal_cards(self):
        self.game.player = [self.game.deck.pop(), self.game.deck.pop()]
        self.game.dealer = [self.game.deck.pop(), self.game.deck.pop()]

        player_scores = calculate_score(self.game.player)
        dealer_scores = calculate_score(self.game.dealer)

        player_blackjack = (len(self.game.player) == 2 and 21 in player_scores)
        dealer_blackjack = (len(self.game.dealer) == 2 and 21 in dealer_scores)

        # 🎯 логика blackjack
        if player_blackjack and dealer_blackjack:
            self.game.message = "Ничья (Blackjack)"
            self.game.state = "end"

        elif player_blackjack:
            self.game.stack += int(self.game.bet * 1.5)
            self.game.message = "BLACKJACK!"
            self.game.state = "end"

        elif dealer_blackjack:
            self.game.stack -= self.game.bet
            self.game.message = "У дилера Blackjack!"
            self.game.state = "end"

        else:
            self.game.state = "player"

    def player_turn(self):
        self.game.state = "player"

    def dealer_turn(self):
        while max(calculate_score(self.game.dealer)) < 17:
            self.game.dealer.append(self.game.deck.pop())

    def resolve_round(self):
        player_best = max([s for s in calculate_score(self.game.player) if s <= 21], default=0)
        dealer_best = max([s for s in calculate_score(self.game.dealer) if s <= 21], default=0)

        if dealer_best > 21 or player_best > dealer_best:
            self.game.stack += self.game.bet
            self.game.message = "Ты выиграл!"
        elif player_best == dealer_best:
            self.game.message = "Ничья"
        else:
            self.game.stack -= self.game.bet
            self.game.message = "Ты проиграл"