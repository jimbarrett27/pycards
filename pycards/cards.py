from dataclasses import dataclass
from enum import Enum
import numpy as np
from typing import List
import random
from itertools import combinations
from copy import deepcopy

FACE_VALUES = {
    0: 'A',
    1: '2',
    2: '3',
    3: '4',
    4: '5',
    5: '6',
    6: '7',
    7: '8',
    8: '9',
    9: 'T',
    10: 'J',
    11: 'Q',
    12: 'K'
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

    def __lt__(self, other):
        """
        Sort cards by their face value
        """
        return self.value < other.value

    def __repr__(self):

        return f'{FACE_VALUES[self.value]}{self.suit.name[0]}'

    @classmethod
    def from_strings(cls, name: str, suit: str):
        name_to_face_value = {name: value for value, name in FACE_VALUES.items()}
        return cls(
            suit=Suit[suit.upper()],
            value=name_to_face_value[name.upper()]
        )


@dataclass
class Cards:

    cards: List[Card]

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, key):
        return self.cards[key]

    def __iadd__(self, other):
        if isinstance(other, Card):
            self.cards.append(other)
        elif isinstance(other, Cards):
            self.cards += other
        else:
            raise TypeError(f"Can't append object of type {type(other)} to cards")

        return self

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

    def contains_flush(self, length: int) -> bool:
        """
        """

        return bool(self.get_flushes(length, length))

    def contains_straight(self, length: int) -> bool:
        """
        
        """

        return bool(self.get_straights(length, length))

    def get_flushes(self, min_length: int, max_length: int) -> List["Cards"]:

        eligible_cards = deepcopy(self)
        flushes = []
        for length in range(max_length, min_length-1, -1):
            for cards in combinations(eligible_cards, length):
                suits = [card.suit for card in cards]
                is_flush = len(set(suits)) == 1
                if is_flush:
                    flushes.append(cards)
                    eligible_cards.play_cards(cards)

        return flushes

    def get_straights(self, min_length: int, max_length: int) -> List["Cards"]:

        eligible_cards = deepcopy(self)
        straights = []
        for length in range(max_length, min_length-1, -1):
            for cards in combinations(eligible_cards, length):
                cards = sorted(cards)
                is_straight = all([c2.value - c1.value == 1 for c1, c2 in zip(cards[:-1], cards[1:])])
                if is_straight:
                    straights.append(cards)
                    eligible_cards.play_cards(cards)

        return straights

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

