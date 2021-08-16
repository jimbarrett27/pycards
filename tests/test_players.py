from pycards.players import Player, Players
import random

def _make_n_players(n: int):
    """
    Helper function to make n random players
    for testing, with exactly one dealer
    """

    dealer_ind = random.choice(range(n))

    return Players([
        Player(
            is_dealer=(i==dealer_ind),
            name='',
            seat_position=i
        ) for i in range(n)
    ])

def test_get_dealer():

    for i in range(2,5):
        players = _make_n_players(i)
        assert players.dealer.is_dealer

def test_permute_dealer():
    """
    Test that the dealer role is correctly
    permuted around the players
    """

    for n_players in range(2, 5):

        players = _make_n_players(n_players)

        # make sure there is only one dealer at the start
        assert sum(player.is_dealer for player in players) == 1

        initial_dealer = players.dealer
        players._permute_dealer()

        # check the dealer changed, and there's still only 1
        assert not initial_dealer.is_dealer
        assert players.dealer != initial_dealer
        assert sum(player.is_dealer for player in players) == 1

        # check that the dealer loops round, and there is
        # only ever one
        for _ in range(n_players - 1):
            players._permute_dealer()
            assert sum(player.is_dealer for player in players) == 1
        
        assert initial_dealer.is_dealer
        for player in players:
            if player != initial_dealer:
                assert not player.is_dealer


