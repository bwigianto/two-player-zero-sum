from mcts import *
from tictactoe import *
import sys

mcts = MonteCarlo(board=Board(),
    max_iters=100,
    explore_coefficient=1.4,
    max_depth=9)
while not mcts.finished():
    mcts.pretty_print()
    parts = input("your move: ").split(' ')
    x = int(parts[0])
    y = int(parts[1])
    mcts.update((x, y))
    mcts.pretty_print()

    print("thinking...")

    if mcts.finished():
        print("You won!")
        sys.exit(0)
    #response
    a = mcts.pick_action()
    mcts.update(a)
mcts.pretty_print()
print("You lost...")
