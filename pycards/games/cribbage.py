"""
Rules for the game of Cribbage
"""

from copy import deepcopy
from itertools import combinations

import numpy as np

from pycards.cards import Card, Cards
from pycards.players import Player, Players


def _cribbage_card_value(card: Card):

    if card.value < 9:
        return card.value + 1

    return 10


class CribbagePlayer(Player):
    """
    Child class of PLayer to add cribbage specific functionality
    """

    def can_peg(self, pegged_cards: Cards):
        """
        If the player can go in the pegging phase
        """

        if len(self.hand) == 0:
            return False

        min_value = min(map(_cribbage_card_value, self.hand))
        current_pegging_score = sum(map(_cribbage_card_value, pegged_cards))

        if current_pegging_score + min_value > 31:
            return False

        return True

    def give_cards_to_crib(self, n_required):
        """
        Choose which cards to give to the crib
        """

        if n_required not in {1, 2}:
            raise ValueError("Requested weird number of cards for crib")

        cards_to_play = Cards(
            np.random.choice(self.hand, size=n_required, replace=False)
        )
        return self.hand.play_cards(cards_to_play)

    def play_pegging_card(self, pegged_cards: Cards):  # pylint: disable=unused-argument
        """
        Choose a card from the players hand to play during the
        pegging phase.

        Requires the current pegging score.
        """

        min_card_value = min(map(_cribbage_card_value, self.hand))

        for card in self.hand:
            if _cribbage_card_value(card) == min_card_value:
                return self.hand.play_card(card)

        raise ValueError("No valid pegging card")


class Cribbage:
    """
    Rules and tracking variables for a game of cribbage
    """

    def __init__(self, players: Players, winning_points: int = 121):

        self.players = players
        self.winning_points = winning_points

        self.deal_pile = Cards.standard_deck()
        self.discard_pile = Cards.empty()
        self.crib = Cards.empty()
        self.turn_up_card = None

        self._decide_dealer()

    @property
    def n_players(self):
        """
        number of players in the game
        """
        return self.players.n_players

    @property
    def cards_per_player(self) -> int:
        """
        The number of cards each player should start a round'
        with, depending on the number of players
        """

        if self.n_players == 2:
            return 6
        if self.n_players in {3, 4}:
            return 5

        raise ValueError("Invalid number of players")

    def _decide_dealer(self) -> Player:

        self.players.dealer = np.random.choice(self.players)

    def _find_winner(self) -> Player:

        for player in self.players:
            if player.score >= self.winning_points:
                return player

        return None

    def _fix_deal_pile(self, n_required_cards):
        """
        If there aren't the required number of cards in the deal pile
        then shuffle the discard pile and append them
        """
        if n_required_cards > len(self.deal_pile):
            self.discard_pile.shuffle()
            self.deal_pile += self.discard_pile

    def _deal_cards_to_players(self):

        n_required_cards = self.n_players * self.cards_per_player
        self._fix_deal_pile(n_required_cards)

        for player in self.players:
            for _ in range(self.cards_per_player):
                dealt_card = self.deal_pile.deal_card()
                player.hand += dealt_card

    def _score_hand(self, hand: Cards, is_crib: bool = False):

        hand_score = 0

        effective_hand = deepcopy(hand)
        effective_hand += self.turn_up_card

        # look for 15s
        for n_cards in [2, 3, 4, 5]:
            for cards in combinations(effective_hand, n_cards):
                if sum(_cribbage_card_value(card) for card in cards) == 15:
                    hand_score += 2

        # look for pairs
        for card1, card2 in combinations(effective_hand, 2):
            if card1.value == card2.value:
                hand_score += 2

        # look for flushes
        if effective_hand.contains_flush(5):
            hand_score += 5
        # can only get flushes of 4 in certain situations
        elif hand.contains_flush(4) and not is_crib:
            hand_score += 4

        # look for runs
        runs = effective_hand.get_straights(3, 5)
        hand_score += sum(map(len, runs))

        # look for knobs
        for card in hand:
            if card.value == 10 and card.suit == self.turn_up_card.suit:
                hand_score += 1

        return hand_score

    def _receive_crib_cards_from_players(self):

        for player in self.players:
            if self.n_players == 2:
                self.crib += player.give_cards_to_crib(n_required=2)
            elif self.n_players in {3, 4}:
                self.crib += player.give_cards_to_crib(n_required=1)

        if self.n_players == 3:
            n_required_cards = 1
            self._fix_deal_pile(n_required_cards)
            self.crib += self.deal_pile.deal_card()

    def _choose_turn_up(self):
        self._fix_deal_pile(n_required_cards=1)
        self.turn_up_card = self.deal_pile.play_random_card()

        if self.turn_up_card.value == 10:
            self.players.dealer.score += 2

        return self._find_winner()

    def _play_pegging_phase(self):

        player_order_gen = self.players.get_player_order_generator()

        while any(len(player.hand) for player in self.players):

            pegged_cards = Cards.empty()
            while any(player.can_peg(pegged_cards) for player in self.players):

                player = next(player_order_gen)

                if player.can_peg(pegged_cards):
                    pegged_cards += player.play_pegging_card(pegged_cards)

                if self._find_winner():
                    return True

        return False

    def _score_hands(self):

        for player in self.players:
            player.score += self._score_hand(player.hand)

    def _discard_hands_and_crib(self):

        for player in self.players:
            self.discard_pile += player.hand.play_all()

        self.discard_pile += self.crib.play_all()
        self.discard_pile += self.turn_up_card

    def play(self):
        """
        The main game loop
        """

        while True:

            self._deal_cards_to_players()

            self._receive_crib_cards_from_players()

            for scoring_phase in (
                self._choose_turn_up,
                self._play_pegging_phase,
                self._score_hands,
            ):
                scoring_phase()

                winner_or_none = self._find_winner()
                if winner_or_none is not None:
                    return winner_or_none

            self._discard_hands_and_crib()
