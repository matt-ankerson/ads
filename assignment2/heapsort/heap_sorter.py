
class HeapSorter(object):

    def __init__(self, unsorted_sequence):
        self._data = unsorted_sequence
        self._boundary = 0

    def __len__(self):
        return len(self._data[: self._boundary])

    def is_empty(self):
        return len(self) == 0

    def _parent(self, j):
        return (j - 1) // 2

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

    def _increase_heap(self, i):
        # shift the boundary rightward.
        # upheap if necessary.
        self._upheap(len(self) - 1)
        self._boundary = i

    def max(self):
        if self.is_empty():
            raise ValueError('Heap is empty.')
        item = self._data[0]
        return (item._key, item._value)

    def _decrease_heap(self, i):
        # shift the boundary leftward.
        self._boundary = i
        self._swap(0, len(self))    # put max key item at end.
        self._downheap(0)

    def sort(self):
        '''Heapsort the given sequence in place.'''
        # phase 1: move the boundary from left to right, one step at a time.
        for i in range(0, len(self._data) + 1):
            self._increase_heap(i)

        print 'heap: ' + str(self.get_heap())
        print 'sequence: ' + str(self.get_sequence())
        print 'boundary: ' + str(self._boundary)

        # phase 2: move the boundary from right to left, one step at a time.
        for i in range(len(self._data) - 1, -1, -1):
            self._decrease_heap(i)

if __name__ == '__main__':
    s = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    heapsorter = HeapSorter(s)
    print 'Unsorted:'
    heapsorter.sort()
    print 'Sorted:'
    print 'heap: ' + str(heapsorter.get_heap())
    print 'sequence: ' + str(heapsorter.get_sequence())
