class Stack:
    # LIFO stack implementation using Python's list as storage.
    # LIFO = Last in first out.
    def __init__(self):
        # create an empty stack.
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def push(self, e):
        # new item stored at the end of the list
        self._data.append(e)

    def top(self):
        if self.is_empty():
            raise ValueError('Stack is empty')
        return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise ValueError('Stack is empty')
        return self._data.pop()


class Sorter(object):

    class _Context(object):

        __slots__ = '_l', '_r'

        def __init__(self, left, right):
            self._l = left
            self._r = right

    def __init__(self):
        pass

    def quick_sort_inplace(self, s, a, b):
        '''Sort the list from s[a] to s[b] inclusive'''
        # seed the stack with provided left and right indices
        stack = Stack()
        stack.push(self._Context(a, b))
        while len(stack) > 0:
            cur = stack.pop()       # pop current context
            if cur._l >= cur._r:
                pass              # range is trivially sorted
            else:
                pivot = s[cur._r]       # last element of range is pivot
                left = cur._l               # will scan rightward
                right = cur._r - 1          # will scan leftward
                while left <= right:
                    # scan until reacjing value >= pivot (or right marker)
                    while left <= right and s[left] < pivot:
                        left += 1
                    # scan until reaching value <= pivot (or left marker)
                    while left <= right and pivot < s[right]:
                        right -= 1
                    if left <= right:       # scans did not strictly cross
                        s[left], s[right] = s[right], s[left]   # swap values
                        left, right = left + 1, right - 1       # shrink range
                # put pivot into its final place, currently marked by left index
                s[left], s[cur._r] = s[cur._r], s[left]
                # push each portion to the stack
                # push the larger sub-problem before the smaller.
                if len(s[cur._l:left - 1]) >= len(s[left + 1:cur._r]):
                    stack.push(self._Context(cur._l, left - 1))
                    stack.push(self._Context(left + 1, cur._r))
                else:
                    stack.push(self._Context(left + 1, cur._r))
                    stack.push(self._Context(cur._l, left - 1))

    def quick_sort(self, s):
        self.quick_sort_inplace(s, 0, len(s) - 1)

if __name__ == '__main__':
    pass
