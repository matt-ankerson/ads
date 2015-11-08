from collections import MutableMapping


class MapBase(MutableMapping):
    '''Abstract base class that includes a nonpublic item class.'''

    class _Item():
        '''Lightweight composite to store key-value pairs.'''
        __slots__ = '_key', '_value'

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self._key == other._key)

        def __lt__(self, other):
            return self._key < other._key
