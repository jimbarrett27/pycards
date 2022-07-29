from pycards.cards import Card, FaceValue


def cribbage_card_value(card: Card):

    if card.value < FaceValue.TEN:
        return card.value.value + 1

    return 10
