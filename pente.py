import numpy as np
import copy

class Pente():
    def __init__(self, n=9):
        self.n = 9

    def start(self):
        board = np.zeros((9, 9))
        return board

    def next_player(self, player):
        return 1 if player == 2 else 2

    def hashable(self, state):
        return str(state)

    def next_state(self, player, state, action):
        return add_stone(state, player, action)

    def legal_actions(self, state):
        valids = []
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    valids.append((i, j))
        return valids

    def finished(self, state):
        return five(state) != -1

    def winner(self, state):
        return five(state)

    def pretty_print(self, state):
        out = ""
        for i in range(self.n):
            out += f"{state[i]}\n"
        print(out)

def five(board, seed=None):
    deltas = [(0, 1), (1, 0), (1, 1)]
    for i in range(len(board)):
        for j in range(len(board[0])):
            for delta in deltas:
                if check_towards(i, j, board, delta, 1) > 0:
                    return 1
                if check_towards(i, j, board, delta, 2) > 0:
                    return 2
    return -1

def check_towards(i, j, board, delta, player):
    (dx, dy) = delta
    if is_valid(board, (i + 4 * dx, j + 4 * dy)):
        for k in range(1, 5):
            if board[i + k*dx][j + k*dy] != player:
                return 0
        return 1
    return 0

def removals(board, stone, pos, diff):
    one = sum(pos, diff)
    two = sum(one, diff)
    three = sum(two, diff)
    if not is_valid(board, three):
        return []
    if stone_at(board, one) == opponent(stone) and stone_at(board, two) == opponent(stone) and stone_at(board, three) == stone:
        return [one, two]
    return []

def add_stone(board, stone, pos):
    # (board, p1_captured, p2_captured) = game_state
    out = copy.deepcopy(board)
    # print("raw_pos: {0}".format(pos))
    # pos = (int(pos / 9), int(pos) % 9)
    # print("pos: {0}".format(pos))
    out[pos[0]][pos[1]] = stone
    to_remove = removals(board, stone, pos, (-1, 0)) + \
        removals(board, stone, pos, (1, 0)) + \
        removals(board, stone, pos, (0, -1)) + \
        removals(board, stone, pos, (0, 1)) + \
        removals(board, stone, pos, (1, 1)) + \
        removals(board, stone, pos, (1, -1)) + \
        removals(board, stone, pos, (-1, 1)) + \
        removals(board, stone, pos, (-1, -1))
    for p in to_remove:
        out[p[0]][p[1]] = 0
        # if stone == 1:
        #     p1_captured += 1
        # else:
        #     p2_captured += 1
    # print("updated: {0}".format(out))
    return out #(out, p1_captured, p2_captured)

def opponent(stone):
    if stone == 1:
        return 2
    return 1

def stone_at(board, pos):
    return board[pos[0]][pos[1]]

def sum(pos, dpos):
    return (pos[0] + dpos[0], pos[1] + dpos[1])

def is_valid(board, pos):
    return pos[0] >= 0 and pos[0] < len(board) and pos[1] >= 0 and pos[1] < len(board[0])

def valid_move(board, pos):
    return is_valid(board, pos) and stone_at(board, pos) == 0
