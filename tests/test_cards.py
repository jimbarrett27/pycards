import pytest
from pycards.cards import make_standard_deck, Card, Suit, Cards

def test_card_from_string():

    examples = {
        'AH': Card(suit=Suit.HEARTS, value=0),
        '2D': Card(suit=Suit.DIAMONDS, value=1),
        '3C': Card(suit=Suit.CLUBS, value=2),
        '4S': Card(suit=Suit.SPADES, value=3),
        '5H': Card(suit=Suit.HEARTS, value=4),
        '6D': Card(suit=Suit.DIAMONDS, value=5),
        '7C': Card(suit=Suit.CLUBS, value=6),
        '8S': Card(suit=Suit.SPADES, value=7),
        '9H': Card(suit=Suit.HEARTS, value=8),
        'TD': Card(suit=Suit.DIAMONDS, value=9),
        'JC': Card(suit=Suit.CLUBS, value=10),
        'QS': Card(suit=Suit.SPADES, value=11),
        'KC': Card(suit=Suit.CLUBS, value=12),
    }

    for string, card in examples.items():
        assert Card.from_string(string) == card
        assert card.__repr__() == string

    

    for bad_string in ('AAH',  '9CC', '5', 'H'):
        with pytest.raises(ValueError):
            Card.from_string(bad_string)

    for bad_string in ('1D', '11', 'H6'):
        with pytest.raises(KeyError):
            Card.from_string(bad_string)


def test_make_standard_deck():

    standard_deck = make_standard_deck()

    assert len(standard_deck) == 52
    assert len(set(standard_deck)) == len(standard_deck)

    unshuffled_deck = make_standard_deck(shuffle=False)

    assert(standard_deck != unshuffled_deck)

def test_flushes():

    # check we find the flush
    example_hand = Cards.from_string('AH 2H 3H 4H')
    assert example_hand.contains_flush(4)
    assert len(example_hand.get_flushes(4,4)) == 1
    assert example_hand.get_flushes(4,4)[0] == example_hand

    
    # check we don't count the sub-flushes
    assert len(example_hand.get_flushes(3, 4)) == 1

    # check we find flushes smaller than max length
    example_hand = Cards.from_string('7D 8H JD 9D')
    assert not example_hand.contains_flush(4)
    assert len(example_hand.get_flushes(3,4)) == 1
    assert len(example_hand.get_flushes(2,4)) == 1

def test_straights():

    # check we find the flush
    example_hand = Cards.from_string('AH 2H 3H 4H')
    assert example_hand.contains_straight(4)
    assert len(example_hand.get_straights(4,4)) == 1
    assert example_hand.get_straights(4,4)[0] == example_hand

    
    # check we don't count the sub-flushes
    assert len(example_hand.get_straights(2, 4)) == 1

    # check we find straights smaller than max length
    example_hand = Cards.from_string('7D 8H JC 9D')
    assert not example_hand.contains_straight(4)
    assert len(example_hand.get_straights(3,4)) == 1
    assert len(example_hand.get_straights(2,4)) == 1

    # check we can get multiple straights with the same cards
    example_hand = Cards.from_string('5S 5D 6H 7C')
    assert example_hand.contains_straight(3) is True
    assert len(example_hand.get_straights(3,4)) == 2

    # check we find out of order straights
    example_hand = Cards.from_string('JH TS QD')
    assert example_hand.contains_straight(3)
    assert len(example_hand.get_straights(3, 3)) == 1

    # check if we can get multiple straights
    example_hand = Cards.from_string('AD 2S 3H JH TS QD')
    assert example_hand.contains_straight(3)
    assert len(example_hand.get_straights(3, 3)) == 2