import unittest
import binary_treemap


class TestLinkedBinaryTree(unittest.TestCase):

    def setUp(self):
        self.tree = binary_treemap.TreeMap()
        input_keys = [5, 1, 3, 8, 4, 2, 7, 9, 6]
        for key in input_keys:
            self.tree[key] = key

    def test_breadthfirst(self):
        expected_keys = [5, 1, 8, 3, 7, 9, 2, 4, 6]
        actual_keys = []
        for node in self.tree.breadthfirst():
            actual_keys.append(node.key())
        self.assertItemsEqual(expected_keys, actual_keys)

if __name__ == '__main__':
    unittest.main()
