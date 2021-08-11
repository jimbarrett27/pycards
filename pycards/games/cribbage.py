from pycards.cards import make_standard_deck, Cards
from pycards.players import Players

class Cribbage:

    def __init__(self, players: Players):

        self.players = players
        self.deal_pile = Cards.standard_deck()
        self.discard_pile = Cards.empty()
        self.crib = Cards.empty()

        self._decide_dealer()

    def _decide_dealer(self) -> Player:
        
        self.players.dealer = np.random.choice(self.players) 

    def _check_for_winner(self):

        for player in self.players:
            if player.score >= 121:
                return True

        return False
    
    def _deal_cards_to_players(self):
        pass

    def _receive_crib_cards_from_players(self):
        pass

    def _play_pegging_phase(self):
        pass

    def _score_hands(self):
        pass

    def _discard_hands_and_crib(self):
        pass

    def play(self):

        while True:
            self._deal_cards_to_players()
            self._receive_crib_cards_from_players()
            self._play_pegging_phase()
            self._score_hands()
            self._discard_hands_and_crib()


            

        


