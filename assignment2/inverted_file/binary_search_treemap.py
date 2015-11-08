from linked_binary_tree import LinkedBinaryTree
from map_base import MapBase


class TreeMap(LinkedBinaryTree, MapBase):
    '''Sorted map implementation using a binary search tree.'''

    # Override position class:
    class Position(LinkedBinaryTree.Position):

        def __init__(self, container, node):
            super(TreeMap.Position, self).__init__(container, node)

        def key(self):
            '''Return key of map's kv pair'''
            return self.element()._key

        def value(self):
            '''Return value of map's kv pair'''
            return self.element()._value

    def __init__(self):
        super(TreeMap, self).__init__()

    def _subtree_search(self, p, k):
        '''Return position of p's subtree having key k, or last node searched'''
        if k == p.key():        # found match
            return p
        elif k < p.key():       # search left subtree
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else:                   # search right subtree
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p                # unsuccessful search

    def _subtree_first_position(self, p):
        '''Return position of first item in subtree rooted at p'''
        walk = p
        while self.left(walk) is not None:     # keep walking left.
            walk = self.left(walk)
        return walk

    def _subtree_last_position(self, p):
        '''Return position of last item in subtree rooted at p.'''
        walk = p
        while self.right(walk) is not None:     # keep walking right.
            walk = self.right(walk)
        return walk

    def first(self):
        '''Return the first position in the tree.'''
        return self._subtree_first_position(
            self.root() if len(self) > 0 else None)

    def last(self):
        '''Return the last position in the tree'''
        return self._subtree_last_position(
            self.root() if len(self) > 0 else None)

    def before(self, p):
        '''Return the position just before p in natural order.'''
        self._validate(p)
        if self.left(p):
            return self._subtree_last_position(self.left(p))
        else:
            # walk upward
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above

    def after(self, p):
        '''Return the position just after p in natural order.'''
        self._validate(p)
        if self.right(p):
            return self._subtree_first_position(self.right(p))
        else:
            # walk upward
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k):
        '''Return position wiht key k or else neighbor.'''
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)     # Hook for balanced tree subclass
            return p

    def find_min(self):
        '''Return kv pair with minimum key.'''
        if self.is_empty():
            return None
        else:
            p = self.first()
            return (p.key(), p.value())

    def find_ge(self, k):
        '''Return kv pair with least key greater than or equal to k.'''
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if p.key() < k:
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_range(self, start, stop):
        '''Iterate all kv pairs such that start <= key < stop'''
        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                p = self.find_position(start)
                if p.key() < start:
                    p = self.after(p)
            while p is not None and (stop is None or p.key() < stop):
                yield (p.key(), p.value())
                p = self.after(p)

    def __getitem__(self, k):
        '''Return value associated with k'''
        if self.is_empty():
            raise KeyError('Map Empty Key Error: ' + repr(k))
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)     # hook for balanced tree subclass
            if k != p.key():
                raise KeyError('Key Error: ' + repr(k))
            return p.value()

    def __setitem__(self, k, v):
        '''Assign value v to key k, overwrite any existing value'''
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v))
        else:
            p = self._subtree_search(self.root(), k)
            if p.key() == k:
                p.element()._value = v
                # self.rebalance_access(p)  # hook for balanced tree subclass
                return
            else:
                item = self._Item(k, v)
                if p.key() < k:
                    leaf = self._add_right(p, item)
                else:
                    leaf = self._add_left(p, item)
        self._rebalance_insert(leaf)    # hook for balanced tree subclass

    def __iter__(self):
        p = self.first()
        while p is not None:
            yield p
            p = self.after(p)

    def delete(self, p):
        '''Remove the item at given position.'''
        self._validate(p)
        if self.left(p) and self.right(p):  # p has two children
            replacement = self._subtree_last_position(self.left(p))
            self._replace(p, replacement.element())
            p = replacement
        # No p has at most one child
        parent = self.parent(p)
        self._delete(p)
        self._rebalance_delete(parent)    # if root deleted, parent is None

    def __delitem__(self, k):
        '''Remove item associated with key k.'''
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if k == p.key():
                self.delete(p)      # rely on positional version.
                return
            self._rebalance_access(p)   # hooke for balanced tree subclass
        raise KeyError('Key Error: ' + repr(k))

    def _rebalance_insert(self, p):
        pass

    def _rebalance_delete(self, p):
        pass

    def _rebalance_access(self, p):
        pass

    def _relink(self, parent, child, make_left_child):
        '''Relink parent node with child node.'''
        if make_left_child:     # make it a left child
            parent._left = child
        else:
            parent._right = child
        if child is not None:
            child._parent = parent

    def _rotate(self, p):
        '''Rotate position p above its parent.'''
        x = p._node
        y = x._parent
        z = y._parent
        if z is None:
            self._root = x      # x becomes root
            x._parent = None
        else:
            self._relink(z, x, y == z._left)    # x becomes immediate child of z
        # Now rotate x and y
        if x == y._left:
            self._relink(y, x._right, True)     # x.right becomes left childto y
            self._relink(x, y, False)           # y becomes right child of x
        else:
            self._relink(y, x._left, False)     # x._left is now right childto y
            self._relink(x, y, True)            # y becomes let child of x

    def _restructure(self, x):
        '''Perform trinode restructure of x with parent/grandparent'''
        y = self.parent(x)
        z = self.parent(y)
        if (x == self.right(y)) == (y == self.right(z)):    # matching alignment
            self._rotate(y)     # single rotation of y
            return y
        else:
            self._rotate(x)      # double rotation of x
            self._rotate(x)
            return x

if __name__ == '__main__':
    treemap = TreeMap()
    treemap[1] = 'horse'
    treemap[2] = 'bacon'
    treemap[4] = 'monkey'
    treemap[7] = 'jumbo'
    for value in treemap:
        print value
