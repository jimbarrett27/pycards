"""
Code for manipulating individual cards and groups of cards
"""

import random
from collections import Counter, defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import product
from typing import List

import numpy as np

FACE_VALUE_TO_STR = {
    0: "A",
    1: "2",
    2: "3",
    3: "4",
    4: "5",
    5: "6",
    6: "7",
    7: "8",
    8: "9",
    9: "T",
    10: "J",
    11: "Q",
    12: "K",
}

STR_TO_FACE_VALUE = {s: v for v, s in FACE_VALUE_TO_STR.items()}


class Suit(Enum):
    """
    Enum to hold the different possible card suits
    """

    SPADES = 1
    HEARTS = 2
    DIAMONDS = 3
    CLUBS = 4

    @classmethod
    def from_string(cls, string):
        """
        Construct a suit from a string (the first letter of the suit name)
        """

        if string == "S":
            return cls.SPADES
        if string == "H":
            return cls.HEARTS
        if string == "D":
            return cls.DIAMONDS
        if string == "C":
            return cls.CLUBS

        raise ValueError(f"Can't make a card from suit string {string}")


@dataclass(frozen=True)
class Card:
    """
    Dataclass to store info about a single card
    """

    suit: Suit
    value: int

    def __lt__(self, other):
        """
        Sort cards by their face value
        """
        return self.value < other.value

    def __repr__(self):
        return f"{FACE_VALUE_TO_STR[self.value]}{self.suit.name[0]}"

    def __hash__(self):
        return self.suit.__hash__() + self.value.__hash__()

    @classmethod
    def from_string(cls, card_str: str):
        """
        Takes a 2 character string representing the card and returns that card

        e.g.,
        AH = Ace of Hearts
        5D = Five of Diamonds
        JC = Jack of Clubs
        TS = Ten of Spades
        """

        if len(card_str) != 2:
            raise ValueError(f"The card string {card_str} is in the wrong format")

        value = STR_TO_FACE_VALUE[card_str[0].upper()]
        suit = Suit.from_string(card_str[1].upper())

        return cls(suit=suit, value=value)


@dataclass
class Cards:
    """
    Class to manipulate collections of cards
    """

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

    def __repr__(self) -> str:
        return " ".join([str(card) for card in self.cards])

    @classmethod
    def from_string(cls, string, delimiter=" "):
        """
        Construct cards from a delimited set of card strings
        """
        return cls([Card.from_string(s) for s in string.split(delimiter)])

    def shuffle(self):
        """
        Randomise the order of the cards
        """
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
        """ "
        Checks if there is a flush of the given length amongst the cards
        """

        return bool(self.get_flushes(length, length))

    def contains_straight(self, length: int) -> bool:
        """
        Checks if theres a striaght of the given length amonsts the cards
        """

        return bool(self.get_straights(length, length))

    def get_flushes(self, min_length: int, max_length: int) -> List["Cards"]:
        """
        Gets all flushes from the cards (cards sharing the same suit, between the
        minimum and maximum length. Subsets of flushes are not counted.
        """

        suits = [card.suit for card in self.cards]
        counts = Counter(suits)

        flushes = []
        for suit, count in counts.most_common():
            if max_length >= count >= min_length:
                flushes.append(
                    Cards([card for card in self.cards if card.suit == suit])
                )

        return flushes

    def get_straights(self, min_length: int, max_length: int) -> List["Cards"]:
        """
        Gets all straights (runs of consecutive values). Cards can be used in multiple
        straights. Does not return sub-straights
        """

        val_to_cards = defaultdict(list)
        for card in self.cards:
            val_to_cards[card.value].append(card)

        vals = np.sort(list(val_to_cards))
        diffs = np.diff(vals)

        runs = []
        current_run = [vals[0]]
        for start_ind, diff in enumerate(diffs):
            if diff == 1:
                current_run.append(vals[start_ind + 1])
            else:
                runs.append(current_run)
                current_run = [vals[start_ind + 1]]

        runs.append(current_run)

        card_runs = []
        for run in runs:
            if not min_length <= len(run) <= max_length:
                continue

            all_runs = product(*[val_to_cards[val] for val in run])
            runs_as_cards = [Cards(list(r)) for r in all_runs]

            card_runs += runs_as_cards

        return card_runs

    @classmethod
    def empty(cls):
        """
        Returns an empty set of cards
        """
        return cls(cards=[])

    @classmethod
    def standard_deck(cls, shuffle: bool = True):
        """
        Returns a standard 52 card deck
        """

        cards = []
        for suit in Suit:
            for value in range(13):
                cards.append(Card(suit, value))

        cards = Cards(cards)

        if shuffle:
            cards.shuffle()

        return cls(cards=cards)
