class LinkedList(object):

    class _Node(object):

        __slots__ = '_element', '_next'

        def __init__(self, element, next):
            self._element = element
            self._next = next

    def __init__(self):
        '''Create an empty list.'''
        self._head = None
        self._tail = None
        self._size = 0  # number of elements

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def _insert(self, node, e):
        '''Create and insert a new node after an existing one.'''
        new_node = self._Node(e, node._next)
        node._next = new_node
        if self._tail == node:
            self._tail = new_node
        self._size += 1

    def _insert_end(self, e):
        '''Insert at the end of the list'''
        if self._tail is None:
            new_node = self._Node(e, None)
            self._head._next = self._tail = new_node
            self._size += 1
        else:
            self._insert(self._tail, e)

    def _insert_beginning(self, e):
        '''Insert into an initially empty list.'''
        new_node = self._Node(e, self._head)
        self._head = new_node
        self._size += 1

    def _remove_after(self, node):
        old_element = node._next._element
        node._next = node._next._next
        if node._next is None:
            self._tail = node
        self._size -= 1
        return old_element

    def _remove_beginning(self):
        old_element = self._head._element
        self._head = self._head._next
        if self._head is None:
            self._tail = None
        self._size -= 1
        return old_element

    def _get_node_before_tail(self):
        cursor = self._head
        while cursor._next is not self._tail:
            cursor = cursor._next
        return cursor

    def append(self, e):
        if self.is_empty():
            self._insert_beginning(e)
        else:
            self._insert_end(e)

    def pop(self):
        if self.__len__() == 1:
            return self._remove_beginning()
        else:
            return self._remove_after(self._get_node_before_tail())

    def __iter__(self):
        if self._head is None:
            raise ValueError('List is empty.')
        cursor = self._head
        while cursor is not None:
            yield cursor._element
            cursor = cursor._next

if __name__ == '__main__':
    s = LinkedList()
