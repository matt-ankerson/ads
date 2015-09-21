import random
import sys

# Author: Matt Ankerson
# Date: 20 September 2015

# This class represents a skip list. The purpose of this skip list is to
# provide an ordered dictionary / map ADT.

class SkipList(object):
    '''Collection of doubly linked lists aligned at towers, which are also
        doubly linked lists.'''    
    class _Item(object):
        '''Use composition to represent an item in the skip list.'''       
        __slots__ = 'key', 'value', 'next', 'prev', 'below', 'above'
        
        def __init__(self, key, value, prev, next, above, below):
            self.key = key
            self.value = value
            self.prev = prev
            self.next = next
            self.above = above
            self.below = below
            
        def __gt__(self, other):
            return self.key > other.key
        
        def __ge__(self, other):
            return self.key >= other.key
            
        def __lt__(self, other):
            return self.key < other.key
            
        def __le__(self, other):
            return self.key <= other.key
            
    class Position(object):
        '''An abstraction representing the location of a single element.'''
        
        def __init__(self, container, item):
            self._container = container
            self._item = item
            
        def item(self):
            '''Return the kv pair held by this position.'''
            return self._item
            
        def __eq__(self, other):
            return type(other) is type(self) and other._item is self._item
            
        def __ne__(self, other):
            return not (self == other)
    
    def __init__(self):
        self.start = self._Item(-sys.maxint, None, None, None, None, None)
        self.end = self._Item(sys.maxint, None, None, None, None, None)
        self.start.next = self.end
        self.end.prev = self.start  # start with a single level.
        self.n_items = 0
        self.height = 1
        
    def _make_position(self, item):
        '''Create and return a new position.'''
        #if item.value == -sys.maxint or item.value == sys.maxint:
        #    return None
        #else:
        return self.Position(self, item)
            
    def _validate_position(self, p):
        '''Return positions item, or raise appropriate error if invalid.'''
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper position type.')
        if p._container is not self:
            raise ValueError('p does not belong to this container.')
        return p._item
        
    def start_pos(self):
        '''Return a position for the start of the skip list.'''
        return self._make_position(self.start)
        
    def above(self, p):
        '''Return the position above this position.'''
        item = self._validate_position(p)
        return self._make_position(item.above)
        
    def below(self, p):
        '''Return the position below this position.'''
        item = self._validate_position(p)
        return self._make_position(item.below)
        
    def next(self, p):
        '''Return the next forward position of this position.'''
        item = self._validate_position(p)
        return self._make_position(item.next)
        
    def prev(self, p):
        '''Return the previous position to this position.'''
        item = self._validate_position(p)
        return self._make_position(item.prev)
        
    def skip_search(self, k):
        '''Return the position p in the bottom list S-0, with the largest key
            such that key(p) <= k'''
        p = self.start_pos()               # Begin at start position.
        while self.below(p) is not None:   # While there's an element below:
            p = self.below(p)           # Drop down.
            while k >= self.next(p)._item.key:     # While the next key is less than k:
                p = self.next(p)        # Scan forward.
        return p                        # Return resulting position.
        
    def insert_after_above(self, p, q, k, v):
        '''Insert an item storing (k, v), after item p (on the same level as p), and above item q,
            returning the new item r.'''
        r = None
        # _Item(key, value, prev, next, above, below)
        if p is None:
            r = self._Item(k, v, None, None, None, q)
            q.above = r
        elif q is None:
            r = self._Item(k, v, p, p.next, None, None)
            p.next.prev = r
            p.next = r 
        else:
            r = self._Item(k, v, p, p.next, None, q)
            p.next.prev = r
            p.next = r                # Stitch up references on this layer.
            q.above = r
        return r
    
    def __getitem__(self, k):
        '''Return the value associated with this key.'''
        pass
        
    def _coin_flip(self):
        '''Toss a coin and return result.'''
        if random.randrange(2) == 0:
            return 'heads'
        else:
            return 'tails'
        
    def __setitem__(self, k, v):
        '''Set the value associated with this key, or create a new item associated with this key.'''
        p = self.skip_search(k)             # p is the bottom level position with the largest key less than or equal to k.
        q = None                            # q will represent top item in the new item's tower.
        i = -1
        while self._coin_flip() == 'heads':     # Toss a coin
            i += 1
            if i >= self.height:
                self.height += 1            # Add a new level to the skip list.
                t = self.next(self.start_pos()) # Get rightmost top position.
                self.start = self.insert_after_above(None, self.start_pos(), -sys.maxint, None)            # Grow leftmost tower.
                self.insert_after_above(self.start, t._item, sys.maxint, None)                         # Grow rightmost tower.
            while self.above(p) is None:
                p = self.prev(p)            # Scan backward.
            p = self.above(p)               # Jump up to a higher level.
            q = self.insert_after_above(p._item, q._item, k, v)     # Increase height of new item's tower.
        self.n_items += 1
        return q
        
    def __len__(self):
        return self.n_items
        
    def __iter__(self):
        '''Yield a forward iteration of all elements.'''
        pass
        
    def __reversed__(self):
        '''Yield a reverse iteration of all elements.'''
        pass
        
    def __contains__(self, k):
        '''Return true if the list contains an item with key k.'''
        pass
        
    def remove(self, k):
        '''Remove the item associated with key k and return its value v.'''
        p = self.skip_search(k)
        if p._item.key != k:
            raise KeyError('Supplied key is invalid.')
        v = p._item.value
        while self.above(p) is not None:    # Remove p and all positions above.
            p._item.prev.next = p._item.next
            p._item.next.prev = p._item.prev    # cut out position p.
            p = self.above(p)
        return v
    
    def find_min(self):
        '''Return the item with minimum key, or None if list is empty.'''
        pass
        
    def find_max(self):
        '''Return the item with maximum key, or None if list is empty.'''
        pass
        
    def find_lt(self, k):
        '''Return the item with the greatest key less than k.'''
        pass
        
    def find_le(self, k):
        '''Return the item with the greatest key less than or equal to k.'''
        pass
        
    def find_gt(self, k):
        '''Return the item with the smallest key greater than k.'''
        pass
        
    def find_ge(self, k):
        '''Return the item with the smallest key greater than or equal to k.'''
        pass
        
    def find_range(self, start, stop):
        '''Iterate all items with keys with start <= key < stop. If min or max is None, 
            iteration begins and ends at the start and end of the list respectively.'''
        pass