import unittest
import word_ladders


class TestWordLadderSolver(unittest.TestCase):

    def setUp(self):
        self.solver = word_ladders.WordLadderSolver()

    def test_solve(self):
        start = 'fool'
        end = 'wise'
        expected = ['fool', 'pool', 'poll', 'pill', 'will', 'wile', 'wise']
        # actual = self.solver.solve(start, end)
        # self.assertItemsEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
