"""
Util functions for cribbage
"""

from pycards.cards import Card, FaceValue


def cribbage_card_value(card: Card):
    """
    Maxs out the value of a card at 10
    """

    if card.value < FaceValue.TEN:
        return card.value.value + 1

    return 10
