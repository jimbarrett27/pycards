import pytest
from pycards.cards import make_standard_deck, Card, Suit

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