from tests.strategies import card_strategy, cards_strategy

from hypothesis import given
from pycards.games.cribbage.util import cribbage_card_value, sum_cribbage_card_values
from pycards.cards import Card, Cards

@given(card=card_strategy())
def test_cribbage_card_value(card: Card):

    val = cribbage_card_value(card)
    assert isinstance(val, int)
    assert val <= 10

@given(cards=cards_strategy())
def test_sum_cribbage_card_values(cards: Cards):
    
    summed_vals = sum_cribbage_card_values(cards)
    
    assert isinstance(summed_vals, int)
    assert summed_vals <= sum(card.value.value + 1 for card in cards)

