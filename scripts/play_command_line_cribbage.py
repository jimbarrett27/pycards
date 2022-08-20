from pycards.games.cribbage.cribbage import Cribbage
from pycards.games.cribbage.players import CommandLinePlayer, RandomCribbagePlayer
from pycards.players import Players


cribbage_game = Cribbage(Players([CommandLinePlayer(is_dealer=True, name='Jimmy', seat_position=0), RandomCribbagePlayer(is_dealer=False, name='Rando', seat_position=0)]))

winner = cribbage_game.play()

print(winner.name)