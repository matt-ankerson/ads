import random

# Author: Matt Ankerson
# Date: 22 September 2015

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
        self.height = 1
        # Store the respective height as the value for our sentinel nodes. (for debugging purposes)
        self.start = self._Item(' ', self.height, None, None, None, None)
        self.end = self._Item('~~~~~', self.height, None, None, None, None)
        self.start.next = self.end
        self.end.prev = self.start  # start with a single level.
        self.n_items = 0
        
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
        p = self.start                  # Begin at start position.
        while p.below is not None:      # While there's an element below:
            p = p.below                 # Drop down.
            while k >= p.next.key:      # While the next key is less than k:
                p = p.next              # Scan forward.
        return p                        # Return resulting position.
        
    def skip_search_ge(self, k):
        '''Return the position p in the bottom list. with the smallest key greater than
            or equal to k.'''
        p = self.end                    # Begin at the top of the leftmost tower.
        while p.below is not None:      # While there's an element below:
            p = p.below                 # Drop down.
            while p.prev.key >= k:      # While the previous key is less than k:
                p = p.prev              # Scan backward.
        return p                        # Return resulting position.
        
    def insert_after_above(self, prev, below, k, v):
        '''Insert an item storing (k, v), after item prev (on the same level as prev), and above item below,
            returning the new item.'''
        new_item = None
        # _Item(key, value, prev, next, above, below)
        if prev is None:    # This is a new left tower level
            new_item = self._Item(k, v, None, self.end, None, below)    
            below.above = new_item
        elif below is None: # This is on the bottom level
            new_item = self._Item(k, v, prev, prev.next, None, None)
            prev.next.prev = new_item
            prev.next = new_item 
        else:               # There are elements both adjacent and below.
            new_item = self._Item(k, v, prev, prev.next, None, below)
            prev.next.prev = new_item
            prev.next = new_item                # Stitch up references on this layer and the below.
            below.above = new_item
        return new_item
    
    def __getitem__(self, k):
        '''Return the value associated with this key.'''
        p = self.skip_search(k)
        if k != p.key:
            raise KeyError('Supplied key is not valid.')
        return p.value
        
    def _coin_flip(self):
        '''Toss a coin and return result.'''
        if random.randrange(2) == 0:
            return 'heads'
        else:
            return 'tails'
        
    def __setitem__(self, k, v):
        '''Set the value associated with this key, or create a new item associated with this key.'''
        p = self.skip_search(k)             # p is the bottom level item with the largest key less than or equal to k.
        q = None                            # q will represent top item in the new item's tower.
        i = 0
        while True:
            i += 1
            if i >= self.height:
                self.height += 1            # Add a new level to the skip list.
                self.end = self.start.next
                self.start = self.insert_after_above(None, self.start, ' ', self.height)        # Grow leftmost tower.
                self.insert_after_above(self.start, self.end, '~~~~~', self.height)             # Grow rightmost tower.
            q = self.insert_after_above(p, q, k, v)     # Increase height of new item's tower.
            while p.above is None:
                p = p.prev                      # Scan backward.
            p = p.above                         # Jump up to a higher level.
            if self._coin_flip() == 'tails':    # Repeat until we get a tails.
                break
        self.n_items += 1
        return q
        
    def __len__(self):
        return self.n_items
        
    def __iter__(self):
        '''Yield a forward iteration of all k/v pairs.'''
        p = self.start
        while p.below is not None:          # Drop down the leftmost tower to the bottom.
            p = p.below
        while p.next.next is not None:
            p = p.next
            yield p.key, p.value
        
    def __contains__(self, k):
        '''Return true if the list contains an item with key k.'''
        p = self.skip_search(k)
        if k == p.key:
            return True
        else:
            return False
        
    def remove(self, k):
        '''Remove the item associated with key k and return its value v.'''
        p = self.skip_search(k)
        if p.key != k:
            raise KeyError('Supplied key is invalid.')
        v = p.value
        while p.above is not None:    # Remove p and all positions above.
            p.prev.next = p.next
            p.next.prev = p.prev    # cut out position p.
            p = p.above
        return v
    
    def find_min(self):
        '''Return the item with minimum key, or None if list is empty.'''
        p = self.start
        while p.below is not None:          # Drop down the leftmost tower to the bottom.
            p = p.below
        if p.next.next is None:
            raise ValueError('Skip list is empty.')
        p = p.next                          # Move forward to the smallest actual value.
        return p.key, p.value
        
    def find_max(self):
        '''Return the item with maximum key, or None if list is empty.'''
        p = self.end
        while p.below is not None:          # Drop down the rightmost tower to the bottom.
            p = p.below
        if p.prev.prev is None:
            raise ValueError('Skip list is empty.')
        p = p.prev
        return p.key, p.value
        
    def find_lt(self, k):
        '''Return the item with the greatest key less than k.'''
        p = self.skip_search(k)
        if k == p.key:
            raise KeyError('No key exists less than supplied key.')
        return p.key, p.value
        
    def find_le(self, k):
        '''Return the item with the greatest key less than or equal to k.'''
        p = self.skip_search(k)
        return p.key, p.value
        
    def find_gt(self, k):
        '''Return the item with the smallest key greater than k.'''
        p = self.skip_search_ge(k)
        if k == p.key:
            raise KeyError('No key exists greater than the supplied key.')
        return p.key, p.value
        
    def find_ge(self, k):
        '''Return the item with the smallest key greater than or equal to k.'''
        p = self.skip_search_ge(k)
        return p.key, p.value
        
    def find_range(self, start, stop):
        '''Iterate all items with keys with start <= key < stop. If min or max is None, 
            iteration begins and ends at the start and end of the list respectively.'''
        start_pos = self.skip_search(start)
        end_pos = self.skip_search(stop)
        cursor = start_pos
        while cursor.next is not end_pos.next:
            yield cursor.key, cursor.value
            cursor = cursor.next
        
if __name__ == '__main__':
    map = SkipList()
    map['1'] = 'quack'
    map['3'] = 'gobble'
    map['2'] = 'baa'
    map['4'] = 'foo'
    map['8'] = 'bar'
    map['9'] = 'baz'
    print('Contents:')
    for k, v in map:
        print k, v
    print('Min: ' + str(map.find_min()))
    print('Max: ' + str(map.find_max()))
    print('Range 2 - 8:')
    for k, v in map.find_range('2', '8'):
        print k, v