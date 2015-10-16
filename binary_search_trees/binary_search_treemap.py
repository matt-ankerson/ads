from linked_binary_tree import LinkedBinaryTree
from map_base import MapBase


class TreeMap(LinkedBinaryTree, MapBase):
    '''Sorted map implementation using a binary search tree.'''

    # Override position class:
    class Position(LinkedBinaryTree.Position):

        def key(self):
            '''Return key of map's kv pair'''
            return self.element()._key

        def value(self):
            '''Return value of map's kv pair'''
            return self.element()._value

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
