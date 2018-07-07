import copy

class Board():
    def start(self):
        return [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]

    def next_player(self, player):
        return 1 if player == 2 else 2

    def hashable(self, state):
        return str(state)

    def next_state(self, player, state, action):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        (x, y) = action
        state_cp = copy.deepcopy(state)
        state_cp[x][y] = player
        return state_cp

    def legal_actions(self, state_history):
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
            return 0 #draw
        return -1 #not finished yet

    def finished(self, state):
        if self.check_win_for(1, state) or self.check_win_for(2, state):
            return True
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
