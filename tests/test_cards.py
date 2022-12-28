# pylint: disable=missing-function-docstring,protected-access

"""
Test for the cards objects and associated methods
"""

import numpy as np
import pytest
from hypothesis import given

from pycards.cards import Card, Cards, FaceValue, Suit
from tests.strategies import cards_strategy





def test_face_value_single_character_rep():

    for f in FaceValue:
        as_single_char = f.single_char_rep()
        assert isinstance(as_single_char, str)
        assert len(as_single_char) == 1

def test_face_value_comparison():

    # make sure we can sort the whole list
    sorted(FaceValue)

    # make sure ace is less than everything
    for fv in FaceValue:
        if fv is fv.ACE:
            continue
        assert FaceValue.ACE < fv

    # make sure king is greater than everything
    for fv in FaceValue:
        if fv is fv.KING:
            continue
        assert FaceValue.KING > fv



def test_card_from_string():

    examples = {
        "AH": Card(suit=Suit.HEARTS, value=FaceValue.ACE),
        "2D": Card(suit=Suit.DIAMONDS, value=FaceValue.TWO),
        "3C": Card(suit=Suit.CLUBS, value=FaceValue.THREE),
        "4S": Card(suit=Suit.SPADES, value=FaceValue.FOUR),
        "5H": Card(suit=Suit.HEARTS, value=FaceValue.FIVE),
        "6D": Card(suit=Suit.DIAMONDS, value=FaceValue.SIX),
        "7C": Card(suit=Suit.CLUBS, value=FaceValue.SEVEN),
        "8S": Card(suit=Suit.SPADES, value=FaceValue.EIGHT),
        "9H": Card(suit=Suit.HEARTS, value=FaceValue.NINE),
        "TD": Card(suit=Suit.DIAMONDS, value=FaceValue.TEN),
        "JC": Card(suit=Suit.CLUBS, value=FaceValue.JACK),
        "QS": Card(suit=Suit.SPADES, value=FaceValue.QUEEN),
        "KC": Card(suit=Suit.CLUBS, value=FaceValue.KING),
    }

    for string, card in examples.items():
        assert Card.from_string(string) == card
        assert repr(card) == string

    for bad_string in ("AAH", "9CC", "5", "H"):
        with pytest.raises(ValueError):
            Card.from_string(bad_string)

    for bad_string in ("1D", "11", "H6"):
        with pytest.raises(KeyError):
            Card.from_string(bad_string)


def test_make_standard_deck():

    standard_deck = Cards.standard_deck()

    assert len(standard_deck) == 52
    assert len(set(standard_deck)) == len(standard_deck)

    unshuffled_deck = Cards.standard_deck(shuffle=False)

    assert standard_deck != unshuffled_deck


def test_flushes():

    # check we find the flush
    example_hand = Cards.from_string("AH 2H 3H 4H")
    assert example_hand.contains_flush(4)
    assert len(example_hand.get_flushes(4, 4)) == 1
    assert example_hand.get_flushes(4, 4)[0] == example_hand

    # check we don't count the sub-flushes
    assert len(example_hand.get_flushes(3, 4)) == 1

    # check we find flushes smaller than max length
    example_hand = Cards.from_string("7D 8H JD 9D")
    assert not example_hand.contains_flush(4)
    assert len(example_hand.get_flushes(3, 4)) == 1
    assert len(example_hand.get_flushes(2, 4)) == 1


def test_straights():

    # check we find the straight
    example_hand = Cards.from_string("AH 2H 3H 4H")
    assert example_hand.contains_straight(4)
    assert len(example_hand.get_straights(4, 4)) == 1
    assert example_hand.get_straights(4, 4)[0] == example_hand

    # check we don't count the sub-straights
    assert len(example_hand.get_straights(2, 4)) == 1

    # check we find straights smaller than max length
    example_hand = Cards.from_string("7D 8H JC 9D")
    assert not example_hand.contains_straight(4)
    assert len(example_hand.get_straights(3, 4)) == 1
    assert len(example_hand.get_straights(2, 4)) == 1

    # check we can get multiple straights with the same cards
    example_hand = Cards.from_string("5S 5D 6H 7C")
    assert example_hand.contains_straight(3) is True
    assert len(example_hand.get_straights(3, 4)) == 2

    # check we find out of order straights
    example_hand = Cards.from_string("JH TS QD")
    assert example_hand.contains_straight(3)
    assert len(example_hand.get_straights(3, 3)) == 1

    # check if we can get multiple straights
    example_hand = Cards.from_string("AD 2S 3H JH TS QD")
    assert example_hand.contains_straight(3)
    assert len(example_hand.get_straights(3, 3)) == 2

    # check we don't loop straights round
    example_hand = Cards.from_string("QH KH AH")
    assert not example_hand.contains_straight(3)
    assert len(example_hand.get_straights(3,3)) == 0

    # check we get straights in reverse
    example_hand = Cards.from_string("8D 7D 6D")
    assert example_hand.contains_straight(3) is True
    assert len(example_hand.get_straights(3, 4)) == 1

    # check we get straights in out of order
    example_hand = Cards.from_string("2D 5C 4S 3H")
    assert example_hand.contains_straight(4) is True
    assert len(example_hand.get_straights(4, 4)) == 1

def test_deal_card():

    cards = Cards.standard_deck()

    assert len(cards) == 52

    first_card = cards[0]
    dealt_card = cards.deal_card()

    assert len(cards) == 51
    assert first_card == dealt_card

    cards.deal_card()

    assert first_card == dealt_card


@given(cards=cards_strategy())
def test_play_card(cards):

    n_cards = len(cards)

    for i in range(len(cards)):
        # play the cards in a random order
        card = cards[np.random.choice(np.arange(n_cards - i))]
        assert len(cards) == n_cards - i

        # figure out how many copies of this card there are
        n_copies = sum(c == card for c in cards)
        assert n_copies >= 1

        cards.play_card(card)
        assert sum(c == card for c in cards) == n_copies - 1
        assert len(cards) == n_cards - i - 1


@given(cards=cards_strategy())
def test_play_cards(cards):

    # choose some random cards to play
    n_cards = len(cards)
    n_to_play = np.random.randint(0, n_cards)

    cards_to_play = np.random.choice(cards, size=n_to_play, replace=False)

    n_copies_before = [sum(c == card for c in cards) for card in cards_to_play]

    cards.play_cards(cards_to_play)

    n_copies_after = [sum(c == card for c in cards) for card in cards_to_play]

    assert all(n1 > n2 for n1, n2 in zip(n_copies_before, n_copies_after))
    assert len(cards) == n_cards - len(cards_to_play)


@given(cards=cards_strategy())
def test_play_all(cards):

    n_cards = len(cards)
    played_cards = cards.play_all()

    assert len(cards) == 0
    assert len(played_cards) == n_cards

def test_face_value_single_char_rep():

    for face_value in FaceValue:
        char_rep = face_value.single_char_rep()
        assert isinstance(char_rep, str)
        assert len(char_rep) == 1

def test_suit_from_string():

    valid_strings = ['S', 'H', 'D', 'C']

    produced_suits = []
    for valid_string in valid_strings:
        produced_suits.append(Suit.from_string(valid_string))

    # check they're all suits
    assert all(isinstance(suit, Suit) for suit in produced_suits)
    
    # check all suits are represented
    assert all(suit in produced_suits for suit in Suit)

    invalid_strings = ['5', 5, None, 'SD', 'Å']
    for invalid_string in invalid_strings:
        with pytest.raises(ValueError):
            Suit.from_string(invalid_string)

