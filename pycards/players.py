from .cards import Cards
from dataclasses import dataclass
from typing import Generator, List

@dataclass
class Player:

    is_dealer: bool
    name: str
    seat_position: int
    
    hand: Cards = Cards.empty()
    score: int = 0

@dataclass
class Players:

    players: List[Player]

    def __getitem__(self, key):
        return self.players[key]

    def __len__(self):
        return len(self.players)

    @property
    def dealer(self):
        for player in self.players:
            if player.is_dealer:
                return player

        return None

    @property
    def n_players(self):
        return len(self)

    @dealer.setter
    def dealer(self, new_dealer: Player):

        if new_dealer not in self.players:
            raise ValueError(f"Player {new_dealer} doesn't exist")

        for player in self.players:
            if player == new_dealer:
                player.is_dealer = True
            else:
                player.is_dealer = False


    def _permute_dealer(self):
        """
        Moves the dealer to the next player
        """

        current_dealer_ind = self.players.index(self.dealer)
        self.players[current_dealer_ind].is_dealer = False
        self.players[(current_dealer_ind + 1) % len(self)].is_dealer = True

    def get_player_order_generator(self) -> Generator[Player, None, None]:

        current_dealer_ind = self.players.index(self.dealer)

        def player_order_gen():
            i = 0
            while True:
                i += 1
                yield self.players[(current_dealer_ind + i) % self.n_players]

        
        return player_order_gen()

    def deal_cards_to_players(self, cards: Cards, cards_per_player: int):
        """
        deal cards one by one to each player, starting from the left of the 
        dealer, until each player has cards_per_player cards
        """
        
        # TODO

