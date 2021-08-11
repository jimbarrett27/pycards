from .cards import Cards
from dataclasses import dataclass

@dataclass
class Player:

    is_dealer: bool
    name: str
    
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

    @dealer.setter
    def dealer(self, value: Player):

        if value not in self.players:
            raise ValueError(f"Player {value} doesn't exist")

        for player in self.players:
            if player == value:
                player.is_dealer = True
            else:
                player.is_dealer = False


    def _permute_dealer(self):
        """
        Moves the dealer to the next player
        """

        current_dealer_ind = self.players.index()
        self.players[current_dealer_ind].is_dealer = False
        self.players[(current_dealer_ind + 1) % len(self)].is_dealer = True
        
        


