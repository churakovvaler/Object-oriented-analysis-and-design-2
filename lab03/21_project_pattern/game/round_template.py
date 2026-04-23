class RoundTemplate:
    def play_round(self):
        self.deal_cards()
        self.player_turn()
        self.dealer_turn()
        self.resolve_round()

    def deal_cards(self):
        raise NotImplementedError

    def player_turn(self):
        raise NotImplementedError

    def dealer_turn(self):
        raise NotImplementedError

    def resolve_round(self):
        raise NotImplementedError