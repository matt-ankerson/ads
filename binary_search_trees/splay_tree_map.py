from binary_search_treemap import TreeMap


class SplayTreeMap(TreeMap):
    '''Sorted map implementation using a splay tree'''

    def __init__(self):
        super(SplayTreeMap, self).__init__()

    def _splay(self, p):
        while p != self.root():
            parent = self.parent(p)
            grand = self.parent(parent)
            if grand is None:
                # zig case
                self._rotate(p)
            elif (parent == self.left(grand)) == (p == self.left(parent)):
                # zig zag case
                self._rotate(parent)    # move parent up
                self._rotate(p)         # then move p up
            else:
                # zig zag case
                self._rotate(p)         # move p up
                self._rotate(p)         # move p up again

    # Override balancing hooks:
    def _rebalance_insert(self, p):
        self._splay(p)

    def _rebalance_delete(self, p):
        self._splay(p)

    def _rebalance_access(self, p):
        self._splay(p)
