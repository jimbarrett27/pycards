from pycards.cards import Cards, Card
from pycards.games.cribbage import Cribbage, CribbagePlayer
from pycards.players import Players
from pycards.util import get_repo_root
import csv


def make_basic_cribbage_game(n_players: int):

    players = Players([
        CribbagePlayer(is_dealer=True, name='Alice', seat_position=1),
        CribbagePlayer(is_dealer=False, name="Bob", seat_position=2),
        CribbagePlayer(is_dealer=False, name="Charlie", seat_position=3),
        CribbagePlayer(is_dealer= False, name="Dave", seat_position=4),
    ][:n_players])

    return Cribbage(players)


def test_score_cribbage_hands():

    repo_root = get_repo_root()
    example_hands_file = repo_root / 'tests/data/cribbage_hands.csv'

    cribbage = make_basic_cribbage_game(1)

    with example_hands_file.open() as f:
        reader = csv.reader(f)
        f.readline()
        for cards, turn_up, is_crib, score in reader:

            hand = Cards.from_string(cards)
            cribbage.turn_up_card = Card.from_string(turn_up)

            is_crib = is_crib == '1'

            print(hand, turn_up)

            assert cribbage._score_hand(hand, is_crib) == int(score)
