"""
Util functions for cribbage
"""

from pycards.cards import Card, Cards, FaceValue


def cribbage_card_value(card: Card):
    """
    Maxs out the value of a card at 10
    """

    if card.value < FaceValue.TEN:
        return card.value.value + 1

    return 10

def compute_current_pegging_score(pegged_cards: Cards):
    return sum(map(cribbage_card_value, pegged_cards))