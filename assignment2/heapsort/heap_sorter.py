
class HeapSorter(object):

    def __init__(self):
        pass

    def _parent(self, j):
        return (j - 1) / 2

    def _left(self, j):
        return 2 * j + 1

    def _right(self, j):
        return 2 * j + 2

    def _swap(self, i, j, lst):
        '''Swap the elements at index i and j.'''
        lst[i], lst[j] = lst[j], lst[i]

    def _downheap(self, first, last, s):
        largest = self._left(first)     # assume left child is largest.
        while largest <= last:
            # if right child exists and is larger:
            if largest < last and s[largest] < s[largest + 1]:
                largest = self._right(first)
            # if child is larger than parent:
            if s[largest] > s[first]:
                self._swap(largest, first, s)
                # move down
                first = largest
                largest = self._left(first)
            else:
                return

    def sort(self, s):
        '''Heapsort the sequence in place.'''
        # phase 1: Convert the sequence to a heap.
        n = len(s) - 1
        least_parent = self._parent(len(s))
        for i in range(least_parent, -1, -1):
            self._downheap(i, n, s)
        # phase 2: Convert the heap back to a sequence.
        # Move the boundary from right to left, one step at a time.
        for i in range(n, 0, -1):
            if s[0] > s[i]:
                self._swap(0, i, s)
                self._downheap(0, i - 1, s)

if __name__ == '__main__':
    s = [6, 7, 5, 9, 2, 4]
    print s
    heapsorter = HeapSorter()
    heapsorter.sort(s)
    print s
