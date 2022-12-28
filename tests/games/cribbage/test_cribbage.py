# pylint: disable=missing-function-docstring,protected-access

import csv

from pycards.cards import Card, Cards
from pycards.games.cribbage.cribbage import Cribbage
from pycards.games.cribbage.players import RandomCribbagePlayer
from pycards.players import Players
from pycards.util import get_repo_root


def make_basic_cribbage_game(n_players: int):

    players = Players(
        [
            RandomCribbagePlayer(is_dealer=True, name="Alice", seat_position=1),
            RandomCribbagePlayer(is_dealer=False, name="Bob", seat_position=2),
            RandomCribbagePlayer(is_dealer=False, name="Charlie", seat_position=3),
            RandomCribbagePlayer(is_dealer=False, name="Dave", seat_position=4),
        ][:n_players]
    )

    return Cribbage(players)


def test_score_cribbage_hands():

    repo_root = get_repo_root()
    example_hands_file = repo_root / "tests/data/cribbage_hands.csv"

    cribbage = make_basic_cribbage_game(1)

    with example_hands_file.open() as f:
        reader = csv.reader(f)
        f.readline()
        for cards, turn_up, is_crib, score in reader:

            hand = Cards.from_string(cards)
            print(hand)
            cribbage.turn_up_card = Card.from_string(turn_up)

            is_crib = is_crib == "1"

            assert cribbage._score_hand(hand, is_crib) == int(score)


def test_cribbage_game_completes():
    """
    Plays random moves until the cribbage game completes,
    to make sure it does
    """

    for n_players in [2, 3, 4]:

        game = make_basic_cribbage_game(n_players=n_players)
        winner = game.play()

        assert winner.score >= 121


def test_deal_cards_to_players():

    game = make_basic_cribbage_game(n_players=2)

    for _ in range(100):

        game._deal_cards_to_players()

        assert len(game.deal_pile) == len(set(game.deal_pile))
        assert len(game.discard_pile) == len(set(game.discard_pile))

        all_cards = (
            game.deal_pile
            + game.discard_pile
            + game.players[0].hand
            + game.players[1].hand
        )
        assert len(all_cards) == len(set(all_cards))
        assert set(all_cards) == set(Cards.standard_deck())

        for player in game.players:
            assert len(player.hand) == game.cards_per_player
            assert len(player.hand) == len(set(player.hand))

        game._discard_hands_and_crib()

def test_score_pegging_sequence():

    repo_root = get_repo_root()
    example_hands_file = repo_root / "tests/data/cribbage_pegging_sequences.csv"

    with example_hands_file.open() as f:
        reader = csv.reader(f)
        f.readline()

        for cards_str, last_card, score_sequence in reader:

            cards = Cards.from_string(cards_str)
            last_card = last_card == '1'
            correct_score_sequence = list(map(int,score_sequence.split(',')))

            score_sequence = []
            for i in range(len(cards)):
                # only pass in last card when its actuall the last card
                last_card_played = last_card and i == len(cards) - 1
                score_sequence.append(Cribbage.score_pegging_contribution(cards[:i+1], last_card_played))

            print(cards)
            assert score_sequence == correct_score_sequence