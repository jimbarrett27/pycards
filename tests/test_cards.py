from pycards.cards import make_standard_deck

def test_make_standard_deck():

    standard_deck = make_standard_deck()

    assert len(standard_deck) == 52
    assert len(set(standard_deck)) == len(standard_deck)

    unshuffled_deck = make_standard_deck(shuffle=False)

    assert(standard_deck != unshuffled_deck)