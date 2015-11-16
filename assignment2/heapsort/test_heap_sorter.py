import unittest
from heap_sorter import HeapSorter


class TestHeapSorter(unittest.TestCase):

    def setUp(self):
        self.hs = HeapSorter()

    def test_sort(self):
        s = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.hs.sort(s)
        self.assertItemsEqual(expected, s)

if __name__ == '__main__':
    unittest.main()
