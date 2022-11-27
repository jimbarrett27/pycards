"""
The different cribbage player innterfaces
"""

import numpy as np

from pycards.cards import Card, Cards
from pycards.games.cribbage.util import cribbage_card_value, sum_cribbage_card_values
from pycards.players import Player


class CribbagePlayer(Player):
    """
    Child class of PLayer to add cribbage specific functionality.

    Base class for the various cribbage strategies
    """

    pegging_hand: Cards

    def can_peg(self, pegged_cards: Cards):
        """
        If the player can go in the pegging phase
        """

        if len(self.pegging_hand) == 0:
            return False

        min_value = min(map(cribbage_card_value, self.pegging_hand))
        current_pegging_score = sum_cribbage_card_values(pegged_cards)
        if current_pegging_score + min_value > 31:
            return False

        return True

    def give_cards_to_crib(self, n_required: int) -> Cards:
        """
        Asbtract function, representing the strategy of giving cards to the crib
        """

        raise NotImplementedError()

    def play_pegging_card(self, pegged_cards: Cards) -> Card:
        """
        Asbtract function, representing the strategy of giving cards to the crib
        """

        raise NotImplementedError()


class RandomCribbagePlayer(CribbagePlayer):
    """
    Plays random valid cards, for quick testing purposes
    """

    def give_cards_to_crib(self, n_required) -> Cards:
        """
        Choose which cards to give to the crib
        """

        if n_required not in {1, 2}:
            raise ValueError("Requested weird number of cards for crib")

        cards_to_play = Cards(
            np.random.choice(self.hand, size=n_required, replace=False)
        )
        return self.hand.play_cards(cards_to_play)

    def play_pegging_card(
        self, pegged_cards: Cards
    ) -> Card:  # pylint: disable=unused-argument
        """
        Choose a card from the players hand to play during the
        pegging phase.

        Requires the current pegging score.
        """

        min_card_value = min(map(cribbage_card_value, self.pegging_hand))

        for card in self.pegging_hand:
            if cribbage_card_value(card) == min_card_value:
                return self.pegging_hand.play_card(card)

        raise ValueError("No valid pegging card")


class CommandLinePlayer(CribbagePlayer):
    """
    Class to handle waiting for command line input from a player
    """

    def give_cards_to_crib(self, n_required: int) -> Cards:

        print(f"Your current hand is\n{self.hand}")

        while True:
            try:
                cards = Cards.from_string(
                    input(f"Choose {n_required} cards for the crib\n")
                )
                if len(cards) != n_required:
                    print("Wrong number of cards chosen")
                    continue
                if sum(card in self.hand for card in cards) != n_required:
                    print("Cards not in you hand")
                    continue
                break
            except ValueError:
                print("Not a valid card, try again")

        return self.hand.play_cards(cards)

    def play_pegging_card(self, pegged_cards: Cards) -> Card:

        print(f"The pegging sequence so far is {pegged_cards}")
        print(f"Your cards available for pegging are {self.pegging_hand}")

        current_pegging_total = sum_cribbage_card_values(pegged_cards)
        while True:
            try:
                card = Card.from_string(input("Choose card to play\n"))
                if card not in self.pegging_hand:
                    print("Card not in you hand")
                    continue
                if cribbage_card_value(card) + current_pegging_total > 31:
                    print("That would exceed 31")
                    continue
                break
            except ValueError:
                print("Not a valid card, try again")

        return self.pegging_hand.play_card(card)
