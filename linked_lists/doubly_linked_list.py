# Author: Matt Ankerson
# Date: 24 August 2015

class DoublyLinkedList(object):
    '''A base class providing a doubly linked list representation.'''
    
    class _Node(object):
        '''Lightweight inner class to store a doubly linked node.'''
        __slots__ = '_element', '_prev', '_next', '_index'    # streamline memory usage
        
        def __init__(self, element, prev, next, index=None):
            self._element = element     # the user's element
            self._index = index
            self._prev = prev           # the previous node reference
            self._next = next           # the next node reference
        
    def __init__(self):
        '''Create an empty list'''
        self._header = self._Node(None, None, None, 0)      # header has 0 index
        self._trailer = self._Node(None, None, None)     # trailer has no index
        self._header._next = self._trailer      # header is before the trailer.
        self._trailer._prev = self._header      # trailer os after the header.
        self._size = 0                          # number of elements.
        
    def __len__(self):
        return self._size
        
    def is_empty(self):
        return self._size == 0
        
    def _insert_between(self, e, predecessor, successor, index=None):
        '''Add element e between two specified elements and return the new node.'''
        newest = self._Node(e, predecessor, successor, index)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest
        
    def _delete_node(self, node):
        '''Delete nonsentinel node from the list and return it's element.'''
        predecessor = node._prev    # get the previous node
        successor = node._next      # get the next node
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element     # record the deleted element
        node._prev = node._next = node._element = None  # deprecate node
        return element