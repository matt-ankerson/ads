import unittest
import quicksort


class TestQuickSort(unittest.TestCase):

    def setUp(self):
        self.sorter = quicksort.Sorter()
        self.sample_1 = [5, 3, 7, 6, 2, 9, 8, 0, 8, 1, 2]
        self.sample_2 = [9, 8, 7, 6, 5, 4, 3, 3, 2, 1, 0]

    def test_quick_sort_1(self):
        expected = [0, 1, 2, 2, 3, 5, 6, 7, 8, 8, 9]
        self.sorter.quick_sort(self.sample_1)
        self.assertItemsEqual(expected, self.sample_1)

    def test_quick_sort_2(self):
        expected = [0, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9]
        self.sorter.quick_sort(self.sample_2)
        self.assertItemsEqual(expected, self.sample_2)

if __name__ == '__main__':
    unittest.main()
