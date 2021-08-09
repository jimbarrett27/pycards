from dataclasses import dataclass
from enum import Enum
import numpy as np

FACE_VALUES = {
    0: 'Ace',
    1: 'Two',
    2: 'Three',
    3: 'Four',
    4: 'Five',
    5: 'Six',
    6: 'Seven',
    7: 'Eight',
    8: 'Nine',
    9: 'Ten',
    10: 'Jack',
    11: 'Queen',
    12: 'King'
}


class Suit(Enum):
    """
    Enum to hold the different possible card suits
    """

    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4


@dataclass
class Card:

    suit: Suit
    value: int

    def __repr__(self):

        return f'{FACE_VALUES[self.value].upper()} OF {self.suit.name}'


class Deck:

    def __init__(self, shuffled: bool = True):

        self.cards = self.init_cards()
        
        if shuffled:
            np.random.shuffle(self.cards)

    @staticmethod
    def init_cards():

        cards = []
        for suit in Suit:
            for value in range(13):
                cards.append(Card(suit, value))
    
        return cards

