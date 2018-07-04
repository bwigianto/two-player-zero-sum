from math import log, sqrt
from random import choice
import copy
import datetime

class MonteCarlo():
    def __init__(self, board, max_iters, explore_coefficient, max_depth):
        self.wins = {}
        self.plays = {}
        self.board = board
        self.states = [board.start()]
        self.max_iters = max_iters
        self.C = explore_coefficient
        self.max_depth = max_depth

    def update(self, a):
        self.states.append(self.board.next_state(self.states[-1], a))

    def state(self):
        return self.states[-1]

    def pretty_print(self):
        state = self.state()
        print(f"{state[0]}\n{state[1]}\n{state[2]}")

    def finished(self):
        return self.board.finished(self.state())

    def win_rate(self, a, s, player):
        return self.wins.get((player, self.board.hashable(s)), 0) / self.plays.get((player, self.board.hashable(s)), 1)

    def mcts_argmax(self, state, player, legal_actions):
        next_actions_and_states = self.next_actions_and_states(state, legal_actions)
        _, a_max = max((self.win_rate(a, s, player), a) for a, s in next_actions_and_states)
        # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get((player, self.board.hashable(s)), 0) /
              self.plays.get((player, self.board.hashable(s)), 1),
              self.wins.get((player, self.board.hashable(s)), 0),
              self.plays.get((player, self.board.hashable(s)), 0), p)
             for p, s in next_actions_and_states),
            reverse=True
        ):
            print( "{3}: {0:.2f}% ({1} / {2})".format(*x))
        return a_max

    def pick_action(self):
        state = self.states[-1]
        player = self.board.current_player(state)
        legal_actions = self.board.legal_plays(self.states[:])
        # Bail out early if there is no real choice to be made.
        if len(legal_actions) == 1:
            return legal_actions[0]

        for _ in range(self.max_iters):
            self.run_simulation(player, state)

        return self.mcts_argmax(state, player, legal_actions)

    def next_actions_and_states(self, state, legal_actions):
        return [(a, self.board.next_state(state, a)) for a in legal_actions]

    def has_all_stats(self, player, next_actions_and_states):
         return all(self.plays.get((player, self.board.hashable(s))) for _, s in next_actions_and_states)

    def run_simulation(self, player, state):
        # A bit of an optimization here, so we have a local
        # variable lookup instead of an attribute access each loop.
        plays, wins = self.plays, self.wins
        visited = set()
        states = copy.deepcopy(self.states)

        expand = True
        for t in range(self.max_depth):
            legal_actions = self.board.legal_plays(states)
            next_actions_and_states = self.next_actions_and_states(state, legal_actions)
            if self.has_all_stats(player, next_actions_and_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[(player, self.board.hashable(s))] for _, s in next_actions_and_states))
                value, action, state = max(
                    ((wins[(player, self.board.hashable(s))] / plays[(player, self.board.hashable(s))]) +
                     self.C * sqrt(log_total / plays[(player, self.board.hashable(s))]), a, s)
                    for a, s in next_actions_and_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                action, state = choice(next_actions_and_states)

            states.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, self.board.hashable(state)) not in plays:
                expand = False
                plays[(player, self.board.hashable(state))] = 0
                wins[(player, self.board.hashable(state))] = 0
                if t + 1 > self.max_depth:
                    self.max_depth = t + 1

            visited.add((player, self.board.hashable(state)))

            player = self.board.current_player(state)
            if self.board.finished(state):
                winner = self.board.winner(state)
                break

        for player, state in visited:
            if (player, self.board.hashable(state)) not in plays:
                continue
            plays[(player, self.board.hashable(state))] += 1
            if player == winner:
                wins[(player, self.board.hashable(state))] += 1
            elif winner != -1:
                wins[(player, self.board.hashable(state))] -= 1
