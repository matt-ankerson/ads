import unittest
import inverted_file


class TestInvertedFile(unittest.TestCase):

    def setUp(self):
        self.inverted_file = inverted_file.InvertedFile()
        self.document = ['the', 'quick', 'brown', 'fox', 'jumped', 'over',
                         'the', 'lazy', 'dog']

    def test_construct_wordmap(self):
        expected = '{ brown: [2], dog: [8], fox: [3], jumped: [4], ' + \
            'lazy: [7], over: [5], quick: [1], the: [0, 6] }'
        self.inverted_file.construct_wordmap(self.document)
        actual = str(self.inverted_file)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
