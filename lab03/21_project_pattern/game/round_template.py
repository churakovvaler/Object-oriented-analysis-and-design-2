from abc import ABC, abstractmethod


class RoundTemplate(ABC):

    def play_round(self):
        self.deal_cards()
        self.player_turn()
        self.dealer_turn()
        self.resolve_round()

    @abstractmethod
    def deal_cards(self):
        pass

    @abstractmethod
    def player_turn(self):
        pass

    @abstractmethod
    def dealer_turn(self):
        pass

    @abstractmethod
    def resolve_round(self):
        pass