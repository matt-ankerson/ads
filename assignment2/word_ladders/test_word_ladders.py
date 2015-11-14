import unittest
import word_ladders


class TestWordLadderSolver(unittest.TestCase):

    def setUp(self):
        self.solver = word_ladders.WordLadderSolver()

    def test_solve_1(self):
        start = 'hello'
        end = 'pupal'
        expected = ['pupal', 'pupas', 'pumas', 'pumps', 'pulps', 'pulls',
                    'hulls', 'hullo', 'hello']
        actual = self.solver.solve(start, end)
        self.assertItemsEqual(expected, actual)

    def test_solve_2(self):
        start = 'baldy'
        end = 'wonky'
        expected = ['wonky', 'honky', 'hanky', 'handy', 'bandy', 'baldy']
        actual = self.solver.solve(start, end)
        self.assertItemsEqual(expected, actual)

    def test_solve_3(self):
        start = 'baldy'
        end = 'ninja'
        expected = 'No path found.'
        actual = self.solver.solve(start, end)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
