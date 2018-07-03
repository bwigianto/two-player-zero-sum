from math import log, sqrt
from random import choice
import copy
import datetime
from tictactoe import *

class MonteCarlo():
    def __init__(self, board):
        self.wins = {}
        self.plays = {}
        self.board = board
        self.states = [board.start()]
        self.max_iters = 100
        self.C = 1.4
        self.max_depth = 9

    def get_play(self):
        state = self.states[-1]
        player = self.board.current_player(state)
        legal = self.board.legal_plays(self.states[:])

        # Bail out early if there is no real choice to be made.
        if not legal:
            return
        if len(legal) == 1:
            return legal[0]

        for games in range(self.max_iters):
            self.run_simulation()

        moves_states = [(p, self.board.next_state(state, p)) for p in legal]

        # Pick the move with the highest percentage of wins.
        percent_wins, move = max(
            (self.wins.get((player, self.board.hashable(S)), 0) /
             self.plays.get((player, self.board.hashable(S)), 1),
             p)
            for p, S in moves_states
        )

        # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get((player, self.board.hashable(S)), 0) /
              self.plays.get((player, self.board.hashable(S)), 1),
              self.wins.get((player, self.board.hashable(S)), 0),
              self.plays.get((player, self.board.hashable(S)), 0), p)
             for p, S in moves_states),
            reverse=True
        ):
            print( "{3}: {0:.2f}% ({1} / {2})".format(*x))

        print( "Maximum depth searched:", self.max_depth)

        return move

    def run_simulation(self):
        # A bit of an optimization here, so we have a local
        # variable lookup instead of an attribute access each loop.
        plays, wins = self.plays, self.wins

        visited_states = set()
        states_copy = copy.deepcopy(self.states)
        state = states_copy[-1]
        player = self.board.current_player(state)

        expand = True
        for t in range(1, self.max_depth + 1):
            legal = self.board.legal_plays(states_copy)
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]
            if all(plays.get((player, self.board.hashable(S))) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[(player, self.board.hashable(S))] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(player, self.board.hashable(S))] / plays[(player, self.board.hashable(S))]) +
                     self.C * sqrt(log_total / plays[(player, self.board.hashable(S))]), p, S)
                    for p, S in moves_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                move, state = choice(moves_states)

            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, self.board.hashable(state)) not in plays:
                expand = False
                plays[(player, self.board.hashable(state))] = 0
                wins[(player, self.board.hashable(state))] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player, self.board.hashable(state)))

            player = self.board.current_player(state)
            if self.board.finished(state):
                winner = self.board.winner(state)
                break

        for player, state in visited_states:
            if (player, self.board.hashable(state)) not in plays:
                continue
            plays[(player, self.board.hashable(state))] += 1
            if player == winner:
                wins[(player, self.board.hashable(state))] += 1

MonteCarlo(Board()).get_play()
