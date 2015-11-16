
class HeapSorter(object):

    def __init__(self):
        pass

    def _parent(self, j):
        return (j - 1) / 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    def _has_left(self, j, lst):
        return self._left(j) < len(lst)

    def _has_right(self, j, lst):
        return self._right(j) < len(lst)

    def _swap(self, i, j, lst):
        '''Swap the elements at index i and j.'''
        lst[i], lst[j] = lst[j], lst[i]

    def _upheap(self, j, lst):
        parent = self._parent(j)
        if j > 0 and lst[j] > lst[parent]:
            self._swap(j, parent, lst)
            self._upheap(j, lst)

    def _downheap(self, j, lst):
        if self._has_left(j, lst):
            left = self._left(j)
            large_child = left
            if self._has_right(j, lst):
                right = self._right(j)
                if lst[right] > lst[left]:
                    large_child = right
            if lst[large_child] > lst[j]:
                self._swap(j, large_child, lst)
                self._downheap(j, lst)

    def sort(self, s):
        '''Heapsort the sequence in place.'''
        # phase 1: convert the sequence to a heap.
        # Move the boundary from left to right, one step at a time.
        for i in range(1, len(s) + 1):
            self._upheap(i - 1, s)

        # phase 2: move the boundary from right to left, one step at a time.
        for i in range(len(s), -1, -1):
            self._swap(0, i - 1, s)
            self._downheap(0, s)

if __name__ == '__main__':
    s = [6, 7, 5, 9, 2, 4]
    print s
    heapsorter = HeapSorter()
    heapsorter.sort(s)
    print s
