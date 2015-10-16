from queue import Queue

# Author: Matt Ankerson
# Date: 29 August 2015


class Tree():
    # 'Abstract' base class representing a tree.

    # --------------------------------------------------------------
    # Nested position class
    class Position():
        '''An abstraction representing the location of a single element.'''

        def element(self):
            '''Return the element stored at this position.'''
            raise NotImplementedError('Must be implemented by subclass.')

        def __eq__(self, other):
            '''Return true if the other position represents the same location'''
            raise NotImplementedError('Must be implemented by subclass.')

        def __ne__(self, other):
            '''Return true if other does not represent the same location.'''
            raise NotImplementedError('Must be implemented by subclass.')

    def __init__(self):
        pass

    def root(self):
        # Return the root node of this tree.
        raise NotImplementedError('Must be implemented by subclass.')

    def is_root(self, p):
        # Return true if 'p' repreesents the root of the tree.
        return self.root() == p

    def parent(self, p):
        # Return the parent of the given node.
        raise NotImplementedError('Must be implemented by subclass.')

    def num_children(self, p):
        # Return the number of children that node has.
        raise NotImplementedError('Must be implemented by subclass.')

    def children(self, p):
        # Generate an iteration of nodes representing node's children
        raise NotImplementedError('Must be implemented by subclass.')

    def is_leaf(self, p):
        # Return true if the given node does not have any children
        return self.num_children(p) == 0

    def __len__(self):
        # Return total number of elements in tree
        raise NotImplementedError('Must be implemented by subclass.')

    def is_empty(self):
        # Return true if the tree is empty.
        return len(self) == 0

    def depth(self, p):
        # Return the number of levels separating the root from the given node.
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height_at_node(self, p):
        # Return the height of the tree rooted at node.
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height_at_node(c) for c in self.children(p))

    def height(self, p=None):
        # Return the height of the subtree rooted at the given node.
        if p is None:
            p = self.root()
        return self._height_at_index(p)

    def nodes(self):
        # Generate an iteration of all nodes in the tree.
        return self.preorder()

    def _subtree_preorder(self, p):
        # Generate a preorder iteration of positions rooted at the given node.
        yield p      # visit this node first.
        for child in self.children(p):
            for other in self._subtree_preorder(child):
                yield other

    def preorder(self):
        # Generate a preorder iteration of the nodes in the tree.
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):    # start recursion
                yield p

    def _subtree_postorder(self, p):
        # Generate a postorder iteration of all nodes rooted at the given node.
        for child in self.children(p):
            for other in self._subtree_postorder(child):
                yield other
        yield p      # visit node after all it's subtrees.

    def postorder(self):
        # Generate a postorder iteration of all nodes in the tree.
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):   # start recursion.
                yield p

    def breadthfirst(self):
        # Generate a breadth first iteration of all nodes in the tree.
        if not self.is_empty():
            fringe = Queue()    # Known nodes not yet yielded.
            fringe.enqueue(self.root())     # start with the root.
            while not fringe.is_empty():
                node = fringe.dequeue()     # Remove node from start of queue
                yield node                  # Return this node
                for child in self.children(node):
                    fringe.enqueue(child)   # Add children to the back of queue

    def __iter__(self):
        # Generate an iteration of all the elements in the tree.
        for node in self.nodes():
            yield node['element']
