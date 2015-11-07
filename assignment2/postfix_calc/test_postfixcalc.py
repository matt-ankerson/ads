import unittest
import postfix_calculator


class TestPostFixCalc(unittest.TestCase):

    def setUp(self):
        self.calc = postfix_calculator.PostfixCalc()

    def test_compute_expression_1(self):
        expression = '1 2 +'
        expected = 3
        actual = self.calc.compute_expression(expression)
        self.assertEqual(expected, actual)

    def test_compute_expression_2(self):
        expression = '3 7 + 4 *'
        expected = 40
        actual = self.calc.compute_expression(expression)
        self.assertEqual(expected, actual)

    def test_compute_expression_3(self):
        expression = '15 2 * 3 /'
        expected = 10
        actual = self.calc.compute_expression(expression)
        self.assertEqual(expected, actual)

    def test_compute_expression_4(self):
        expression = '2 7 6 + -'
        expected = -11
        actual = self.calc.compute_expression(expression)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
