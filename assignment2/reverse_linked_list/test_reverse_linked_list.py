import unittest
import reverse_linked_list
import copy


class TestLinkedList(unittest.TestCase):

    def setUp(self):
        self.linked_list = reverse_linked_list.LinkedList()
        for x in xrange(20):
            self.linked_list.append(x)

    def test_reverse_ne(self):
        normal_list = copy.deepcopy(self.linked_list)
        # Reverse the list
        self.linked_list.reverse()
        self.assertNotEqual(str(self.linked_list), str(normal_list))

    def test_reverse_eq(self):
        normal_list = copy.deepcopy(self.linked_list)
        # Reverse the list twice
        self.linked_list.reverse()
        self.linked_list.reverse()
        self.assertEqual(str(self.linked_list), str(normal_list))


if __name__ == '__main__':
    unittest.main()
