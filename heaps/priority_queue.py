import heapq

# Author: Matt Ankerson
# Date: 13 September 2015

# This class wraps Python's heapq module and provides a priority queue.

class PriorityQueue(object):

    class _Item(object):
        '''Lightweight class to represent an item in the Priority Queue.'''
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __lt__(self, other):
            return self._key < other._key   # compare keys for equality.

    def __init__(self):
        self.heap = []

    def _create_item(self, k, v):
        '''Create and return a new item.'''
        return self._Item(k, v)

    def is_empty(self):
        return len(self.heap) == 0

    def push(self, priority, value):
        '''Push a new kv pair into the heap. Return the new item'''
        new_item = self._create_item(priority, value)
        heapq.heappush(self.heap, new_item)
        return new_item

    def peek(self):
        '''Return but dont remove the next item.'''
        if self.is_empty():
            return None
        else:
            return self.heap[0]

    def pop(self):
        '''Remove and return the next item'''
        if self.is_empty():
            return None
        else:
            return heapq.heappop(self.heap)

    def elements(self):
        '''Return a list of all elements in order.'''
        if self.is_empty():
            return None
        else:
            return heapq.nsmallest(len(self.heap), self.heap)
