from pycards.cards import Cards, Card, Suit
from pycards.games.cribbage import Cribbage, CribbagePlayer
from pycards.players import Players

def make_basic_cribbage_game(n_players: int):

    players = Players([
        CribbagePlayer(is_dealer=True, name='Alice'),
        CribbagePlayer(is_dealer=False, name="Bob"),
        CribbagePlayer(is_dealer=False, name="Charlie"),
        CribbagePlayer(is_dealer= False, name="Dave"),
    ][:n_players])

    return Cribbage(players)

def test_score_hand():

    game = make_basic_cribbage_game(2)

    hand = Cards([
        Card.from_strings('Five', 'Hearts'),
        Card.from_strings('Five', 'Diamonds'),
        Card.from_strings('Five', 'Spades'),
        Card.from_strings('Jack', 'Clubs')
    ])
    game.turn_up_card = Card.from_strings('Five', 'Clubs')

    assert game._score_hand(hand) == 29

    hand = Cards([
        Card.from_strings('Ace', 'Hearts'),
        Card.from_strings('Two', 'Diamonds'),
        Card.from_strings('Three', 'Spades'),
        Card.from_strings('Four', 'Clubs')
    ])
    game.turn_up_card = Card.from_strings('Five', 'Clubs')

    assert game._score_hand(hand) == 7

    hand = Cards([
        Card.from_strings('Ace', 'Hearts'),
        Card.from_strings('Two', 'Hearts'),
        Card.from_strings('Three', 'Hearts'),
        Card.from_strings('Four', 'Hearts')
    ])
    game.turn_up_card = Card.from_strings('Five', 'Hearts')

    assert game._score_hand(hand) == 12