import copy

class Board():
    def start(self):
        return [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        ct = 0
        for a in state:
            for c in a:
                ct += 1 if c == '_' else 0
        return 1 if ct % 2 == 1 else 2

    def hashable(self, state):
        return str(state)

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        (x, y) = play
        state_cp = copy.deepcopy(state)
        state_cp[x][y] = self.current_player(state)
        return state_cp

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        legal = []
        state = state_history[-1]
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == '_':
                    legal.append((i, j))
        return legal

    def winner(self, state):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        if self.check_win_for(1, state):
            return 1
        if self.check_win_for(2, state):
            return 2
        if self.finished(state):
            return -1
        return 0

    def finished(self, state):
        for x in range(3):
            for y in range(3):
                if state[x][y] == '_':
                    return False
        return True

    def check_win_for(self, player, state):
        for y in range(3):
            count = 0
            for x in range(3):
                if state[x][y] == player:
                    count += 1
            if count == 3:
                return True

        for x in range(3):
            count = 0
            for y in range(3):
                if state[x][y] == player:
                    count += 1
            if count == 3:
                return True
        # check two diagonal strips
        count = 0
        for d in range(3):
            if state[d][d] == player:
                count += 1
        if count == 3:
            return True
        count = 0
        for d in range(3):
            if state[d][3-d-1] == player:
                count += 1
        if count == 3:
            return True
        return False
