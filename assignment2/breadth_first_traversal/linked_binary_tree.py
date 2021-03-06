from binary_tree_base import BinaryTree


class LinkedBinaryTree(BinaryTree):
    '''Linked representation of a binary tree structure.'''

    class _Node(object):
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        '''Abstraction representing the location of a single element.'''

        def __init__(self, container, node):
            '''Constructor should not be invoked by user.'''
            super(LinkedBinaryTree.Position, self).__init__()
            self._container = container
            self._node = node

        def element(self):
            '''Return the element stored at this position.'''
            return self._node._element

        def __eq__(self, other):
            '''Return true if the other position represents the same
            position.'''
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other):
            '''Inverse of __eq__'''
            return type(other) is not type(self) or \
                other._node is not self._node

    def _validate(self, p):
        '''Return associated node, if position is valid.'''
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type.')
        if p._container is not self:
            raise ValueError('p does not belong to this container.')
        if p._node._parent is p._node:  # convention for deprecated nodes.
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        '''Return position instance for given node.'''
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        '''Create an initially empty binary tree'''
        super(LinkedBinaryTree, self).__init__()
        self._root = None
        self._size = 0

    # ---------------------------------------
    # Public accessors
    def __len__(self):
        '''Return the total number of elements in the tree.'''
        return self._size

    def root(self):
        '''Return the root position of the tree.'''
        return self._make_position(self._root)

    def parent(self, p):
        '''Return the position of p's parent.'''
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        '''Return the position of p's left child.'''
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        '''Return the position of p's right child.'''
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        '''Return the number of children that p has.'''
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    def _add_root(self, e):
        '''Place element e at root of empty tree and return new position.'''
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        '''Create a new left child for Position p, storing element e.
        Return the new position.'''
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists.')
        self._size += 1
        node._left = self._Node(e, node)
        return self._make_position(node._left)

    def _add_right(self, p, e):
        '''Create a new right child for position p, storing element e.
        Return the new position.'''
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child already exists.')
        self._size += 1
        node._right = self._Node(e, node)
        return self._make_position(node._right)

    def _replace(self, p, e):
        '''Replace the element at position p with element e,
        return old element'''
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        '''Delete node at position p, and replace it with its child (if any).
        Return the element that had been stored at positon p.'''
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children.')
        child = node._left if node._left else node._right   # might be None
        if child is not None:
            child._parent = node._parent    # child's grandparent becomes parent
        if node is self._root:
            self._root = child              # child becomes root
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node     # convention for deprecated node.
        return node._element

    def _attach(self, p, t1, t2):
        '''Attach trees t1 and t2 as left and right subtrees of external p.'''
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError('position must be a leaf.')
        if not type(self) is type(t1) is type(t1):
            raise TypeError('Tree types must match.')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():   # attach t1 as left subtree
            t1._root._parent = node
            node._left = t1._root
            t1._root = None     # set t1 instance to empty
            t1._size = 0
        if not t2.is_empty():   # attach t2 as right subtree
            t2._root._parent = node
            node._right = t2._root
            t2._root = None     # set t2 instance to empty
            t2._size = 0
