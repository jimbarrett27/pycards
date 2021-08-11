import random

from pycards.cards import make_standard_deck, Cards
from pycards.players import Players, Player

from itertools import combinations


class CribbagePlayer(Player):

    def give_cards_to_crib(self, n_required):

        if n_required not in {1,2}:
            raise ValueError("Requested weird number of cards for crib")

        cards_to_play = Cards(random.choices(self.hand, k=n_required))
        return self.hand.play_cards(cards_to_play)

class Cribbage:

    def __init__(self, players: Players):

        self.players = players
        self.deal_pile = Cards.standard_deck()
        self.discard_pile = Cards.empty()
        self.crib = Cards.empty()
        self.turn_up_card = None

        self._decide_dealer()

    @property
    def n_players(self):
        return len(self.players)

    @property
    def cards_per_player(self) -> int:

        if self.n_players == 2:
            return 6
        elif self.n_players in {3,4}:
            return 5
        else:
            raise ValueError("Invalid number of players")


    def _decide_dealer(self) -> Player:
        
        self.players.dealer = np.random.choice(self.players) 

    def _check_for_winner(self):

        for player in self.players:
            if player.score >= 121:
                return True

        return False

    def _fix_deal_pile(self, n_required_cards):
        """
        If there aren't the required number of cards in the deal pile
        then shuffle the discard pile and append them
        """
        if required_cards > len(self.deal_pile):
            self.discard_pile.shuffle()
            self.deal_pile += self.discard_pile
    
    def _deal_cards_to_players(self):
        
        n_required_cards = self.n_players * self.cards_per_player
        self._fix_deal_pile(n_required_cards)

        for _ in range(self.cards_per_player):
            for player in self.players:
                player.hand += self.deal_pile.deal_card()


    def _score_hand(self, hand: Cards):

        hand_score = 0

        # look for 15s
        for n_cards in [2,3,4,5]:
            for cards in combinations(hand, n_cards):
                if sum(card.value for card in cards) == 15:
                    hand_score += 2

        # look for runs

        # look for flushes

        # look for knobs

        pass

    def _receive_crib_cards_from_players(self):
        
        for player in self.players:
            if self.n_players == 2:
                self.crib += player.give_cards_to_crib(n_required=2)
            elif self.n_players in {3, 4}:
                self.crib += player.give_cards_to_crib(n_required=1)

        if self.n_players == 3:
            n_required_cards = 1
            self._fix_deal_pile(n_required_cards)
            self.crib += self.deal_pile.deal_card()

    def _choose_turn_up(self):
        n_required_cards = 1
        self._fix_deal_pile(n_required_cards)
        self.turn_up_card = self.deal_pile.play_random_card()

        if self.turn_up_card.value == 11:
            self.players.dealer.score += 2

    def _play_pegging_phase(self):
        pass

    def _score_hands(self):
        
        for player in self.players:
            player.score += self._score_hand(player.hand)


    def _discard_hands_and_crib(self):
        
        for player in self.players:
            self.discard_pile += player.hand.play_all()

        self.discard_pile += self.crib.play_all()
        self.discard_pile += self.turn_up_card

    def play(self):

        while True:
            self._deal_cards_to_players()
            self._receive_crib_cards_from_players()
            self._play_pegging_phase()
            self._score_hands()
            self._discard_hands_and_crib()


            

        


