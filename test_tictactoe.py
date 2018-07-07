import unittest
from tictactoe import *

class TestTictatoe(unittest.TestCase):

    def test_next_player(self):
        board = Board()
        self.assertEqual(board.next_player(1), 2)
        self.assertEqual(board.next_player(2), 1)

    def test_gets_next_state_for_p1(self):
        board = Board()
        expected = [['_', '_', '_'], ['_', 1, '_'], ['_', '_', '_']]
        self.assertEqual(board.next_state(1, board.start(), (1, 1)), expected)

    def test_gets_next_state_for_p2(self):
        board = Board()
        start = [['_', '_', '_'], [2, '_', '_'], ['_', '_', '_']]
        expected = [['_', '_', '_'], [2, 1, '_'], ['_', '_', '_']]
        self.assertEqual(board.next_state(1, start, (1, 1)), expected)

    def test_finds_legal_plays_at_start(self):
        board = Board()
        legal_moves = [(x, y) for x in range(3) for y in range(3)]
        self.assertEqual(board.legal_actions([board.start()]), legal_moves)

    def test_finds_legal_moves_in_middle(self):
        board = Board()
        start = [[2, 1, 2], ['_', 1, '_'], [1, 2, 2]]
        legal_moves = [(1, 0), (1, 2)]
        self.assertEqual(board.legal_actions([start]), legal_moves)

    def test_finished(self):
        board = Board()
        start = [[2, 1, 2], ['_', 1, '_'], [1, 1, 2]]
        self.assertTrue(board.finished(start))

    def test_not_finished(self):
        board = Board()
        start = [[2, 1, 2], ['_', 1, '_'], [1, 2, 2]]
        self.assertFalse(board.finished(start))

    def test_finds_winner(self):
        board = Board()
        start = [[2, 1, 2], ['_', 1, '_'], [1, 1, 2]]
        self.assertEqual(board.winner(start), 1)

    def test_finds_draw(self):
        board = Board()
        start = [[2, 1, 2], [2, 1, 1], [1, 2, 2]]
        self.assertEqual(board.winner(start), 0)

    def test_not_finished_returns_negative(self):
        board = Board()
        start = [[2, 1, 2], ['_', 1, '_'], [1, 2, 2]]
        self.assertEqual(board.winner(start), -1)

if __name__ == '__main__':
    unittest.main()
