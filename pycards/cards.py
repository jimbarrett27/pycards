from dataclasses import dataclass
from enum import Enum
import numpy as np
from typing import List

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


@dataclass(frozen=True)
class Card:

    suit: Suit
    value: int

    def __repr__(self):

        return f'{FACE_VALUES[self.value].upper()} OF {self.suit.name}'

@dataclass
class Cards:

    cards: List[Card]

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, key):
        return self.cards[key]

    def shuffle(self):
        np.random.shuffle(self.cards)

    @classmethod
    def empty(cls):
        return cls(cards=[])

    @classmethod
    def standard_deck(cls):
        cards = make_standard_deck()
        return cls(cards=cards)


def make_standard_deck(shuffle: bool = True) -> Cards:
    
    cards = []
    for suit in Suit:
        for value in range(13):
            cards.append(Card(suit, value))

    cards = Cards(cards)

    if shuffle:
        cards.shuffle()

    return cards

