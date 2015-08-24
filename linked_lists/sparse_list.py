from doubly_linked_list import DoublyLinkedList

# Author: Matt Ankerson
# Date: 24 August

# This class is meant to optimally and efficently represent a sparse list
# (wherein most of the values are zero). We care about the indicies of each element,
# and we care especially about non-zero values.

class CondensedList(DoublyLinkedList):
    '''Use a doubly linked list to represent a sparse list of values'''
    
    def __init__(self):
        DoublyLinkedList.__init__(self)     # create the empty list
        
    def __getitem__(self, k):
        '''Return element at index k. Worst case O(n) time.'''
        if not 0 <= k < self._size:
            raise IndexError('Invalid index')
        item = 0
        current = self._header._next
        while not current == self._trailer:
            if current._index == k:
                item = current._element
                break
            current = current._next
        return item
        
    def __iter__(self):
        '''Generate a forward iteration for the elements in the list.'''
        current = self._header._next
        yield self.__getitem__(0)     # yield the very first item
        while not current == self._trailer:
            for k in range(current._prev._index + 1, current._index):
                yield 0
            yield current._element
            current = current._next           
        
    def _add_zero_value(self):
        '''Increment size, to account for the additional value'''
        self._size += 1
            
    def append(self, e):
        '''Add element e to the end of the list'''
        if e == 0:      # check for zeroness
            self._add_zero_value()
        else:
            # append element to list, include index of 'self._size'
            self._insert_between(e, self._trailer._prev, self._trailer, self._size)
            
    def pop(self):
        '''Remove and return the last element of the list.'''
        # Assess the index value of the last Node. If it's less than one less the size
        # of the list: return 0, and decrement the size of the list.
        if self._trailer._prev._index < (self._size - 1):
            self._size -= 1
            return 0
        else:
            return self._delete(self._trailer._prev)
            
if __name__ == "__main__":
    L = CondensedList()
    L.append(0)
    L.append(1)
    L.append(0)
    L.append(2)
    L.append(0)
    L.append(3)
    L.append(0)
    L.append(4)
    print('Length: ' + str(len(L)))
    
    for item in L:
        print item
          