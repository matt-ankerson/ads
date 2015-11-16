
class Heap(object):

    class _Item(object):

        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            return self._key < other._key

    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self) == 0

    def _parent(self, j):
        return (j - 1) // 2

    def _left(self, j):
        return 2 * j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _right(self, j):
        return 2 * j + 2

    def _swap(self, i, j):
        '''Swap the elements at index i and j.'''
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)

    def add(self, key, value):
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data) - 1)

    def min(self):
        if self.is_empty():
            raise ValueError('Heap is empty.')
        item = self._data[0]
        return (item._key, item._value)

    def remove_min(self):
        if self.is_empty():
            raise ValueError('Heap is empty.')
        self._swap(0, len(self._data) - 1)  # put min key item at end.
        item = self._data.pop()             # and remove it from the list.
        self._downheap(0)
        return (item._key, item._value)

if __name__ == '__main__':
    heap = Heap()
    heap.add(1, 'A')
    heap.add(2, 'B')
    heap.add(3, 'C')
    print heap.min()
