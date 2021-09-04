from pycards.cards import Cards, Card, Suit
from pycards.games.cribbage import Cribbage, CribbagePlayer
from pycards.players import Players

def make_basic_cribbage_game(n_players: int):

    players = Players([
        CribbagePlayer(is_dealer=True, name='Alice', seat_position=1),
        CribbagePlayer(is_dealer=False, name="Bob", seat_position=2),
        CribbagePlayer(is_dealer=False, name="Charlie", seat_position=3),
        CribbagePlayer(is_dealer= False, name="Dave", seat_position=4),
    ][:n_players])

    return Cribbage(players)


