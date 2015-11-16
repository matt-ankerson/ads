
class HeapSorter(object):

    def __init__(self, unsorted_sequence=None):
        self._data = unsorted_sequence
        self._boundary = 0

    def __len__(self):
        return len(self._data[: self._boundary])

    def is_empty(self):
        return len(self) == 0

    def _parent(self, j):
        return (j - 1) / 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    def _has_left(self, j):
        return self._left(j) < len(self)

    def _has_right(self, j):
        return self._right(j) < len(self)

    def _swap(self, i, j):
        '''Swap the elements at index i and j.'''
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] > self._data[parent]:
            self._swap(j, parent)
            self._upheap(j)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            large_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] > self._data[left]:
                    large_child = right
            if self._data[large_child] > self._data[j]:
                self._swap(j, large_child)
                self._downheap(j)

    def get_heap(self):
        items = []
        for item in self._data[: self._boundary]:
            items.append(item)
        return items

    def get_sequence(self):
        items = []
        for item in self._data[self._boundary:]:
            items.append(item)
        return items

    def sort(self, s):
        '''Heapsort the sequence in place.'''
        self._data = s
        # phase 1: move the boundary from left to right, one step at a time.
        for i in range(1, len(self._data)):
            self._upheap(i - 1)
            self._boundary = i

        print 'heap: ' + str(self.get_heap())

        # phase 2: move the boundary from right to left, one step at a time.
        for i in range(len(self._data) - 1, -1, -1):
            self._boundary = i
            self._swap(0, len(self) - 1)
            self._downheap(0)

        print 'sequence: ' + str(self.get_sequence())

if __name__ == '__main__':
    s = [6, 7, 5, 9, 2, 4]
    heapsorter = HeapSorter()
    heapsorter.sort(s)
