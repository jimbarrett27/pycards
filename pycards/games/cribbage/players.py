import numpy as np

from pycards.cards import Cards
from pycards.games.cribbage.util import cribbage_card_value
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
        current_pegging_score = sum(map(cribbage_card_value, pegged_cards))

        if current_pegging_score + min_value > 31:
            return False

        return True

    def give_cards_to_crib(self, n_required: int):

        raise NotImplementedError()

    def play_pegging_card(self, pegged_cards: Cards):

        raise NotImplementedError()


class RandomCribbagePlayer(CribbagePlayer):
    def give_cards_to_crib(self, n_required):
        """
        Choose which cards to give to the crib
        """

        if n_required not in {1, 2}:
            raise ValueError("Requested weird number of cards for crib")

        cards_to_play = Cards(
            np.random.choice(self.hand, size=n_required, replace=False)
        )
        return self.hand.play_cards(cards_to_play)

    def play_pegging_card(self, pegged_cards: Cards):  # pylint: disable=unused-argument
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
