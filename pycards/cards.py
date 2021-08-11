from dataclasses import dataclass
from enum import Enum
import numpy as np
from typing import List
import random

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

    def __IADD__(self, other):
        if isinstance(other, Card):
            self.cards.append(other)
        elif isinstance(other, Cards):
            self.cards += other
        else:
            raise TypeError(f"Can't append object of type {type(other)} to cards")

    def shuffle(self):
        np.random.shuffle(self.cards)

    def deal_card(self):
        """
        deals a single card from the top of the deck, removing it from the deck
        """
        card = self.cards[0]
        self.cards = self.cards[1:]
        return card

    def play_card(self, card: Card):
        """
        Returns the specified card, and removes it from the cards
        """

        self.cards.remove(card)
        return card

    def play_cards(self, cards: "Cards"):
        """
        Returns the specified cards, and removes it from the cards
        """
        return Cards([self.play_card(card) for card in cards])

    def play_random_card(self):
        """
        Returns a random card from the cards and removes it from the pile
        """
        card_to_play = random.choice(self.cards)
        return self.play_card(card_to_play)

    def play_all(self):
        """
        returns all cards and removes them from the cards
        """
        return self.play_cards(self.cards)


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

