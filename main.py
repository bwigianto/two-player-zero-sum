from mcts import *
from tictactoe import *

mcts = MonteCarlo(Board())
while not mcts.finished():
    mcts.pretty_print()
    parts = input("your move: ").split(' ')
    x = int(parts[0])
    y = int(parts[1])
    mcts.update((x, y))
    mcts.pretty_print()
    #response
    a = mcts.pick_action()
    mcts.update(a)
