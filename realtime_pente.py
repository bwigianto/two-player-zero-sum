from mcts import *
from pente import *
import sys

def get_action():
    parts = input("your move: ").split(' ')
    x = int(parts[0])
    y = int(parts[1])
    return (x, y)

mcts = MonteCarlo(board=Pente(),
    max_iters=100,
    explore_coefficient=1.4,
    max_depth=9)
while not mcts.finished():
    mcts.pretty_print()
    mcts.update(1, get_action())
    mcts.pretty_print()

    print("thinking...")

    if mcts.finished():
        print("You won!")
        sys.exit(0)
    #response
    mcts.update(2, mcts.pick_action(2))
mcts.pretty_print()
print("You lost...")
