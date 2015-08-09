import ctypes   # provides native C types

class DynamicArray:
    # A dynamic array class similar to the Python list
    
    def __init__(self):
        # Create an empty array
        self._n = 0     # number of elements
        self._capacity = 1
        self._A = self._make_array(self._capacity)
        
    def __len__(self):
        # return the number of elements stored in the array
        return self._n
        
    def get_capacity(self):
        return self._capacity
    
    def __getitem__(self, k):
        # return element at index k
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k]
        
    def append(self, obj):
        # Add obj to the end of array
        if self._n == self._capacity:           # not eneough cells
            self._resize(2 * self._capacity)    # so double capacity
        self._A[self._n] = obj
        self._n += 1
        
    def _resize(self, c):
        # resize internal array to capacity c
        B = self._make_array(c)         # make new big array
        for k in range(self._n):        # for each existing value
            B[k] = self._A[k]           # copy into the bigger array
        self._A = B                     # use the big array
        self._capacity = c
        
    def _make_array(self, c):
        # return new array with capacity c
        return (c * ctypes.py_object)()
        
    def pop(self):
        # remove the last element from the list and return it.
        # shrink the capacity as necessary
        obj = self._A[self._n - 1]          # get the last element
        self._A[self._n - 1] = None         # remove the last element
        if (self._n * 4) <= self._capacity:    # if n is less than a quarter of c
            self._resize(self._capacity / 2)   # shrink in half
        self._n -= 1                          # decrement n
        return obj                      # return the object that was removed.
        
class OrderedDynamicArray(DynamicArray):
    # maintain a sorted dynamic array
    
    def __init__(self):
        DynamicArray.__init__(self)
    
    def _bsearch_for_index(self, data, target, low, high):
        # return index for insersion point
        if low > high:
            return low          # return low as the index
        else:
            mid = (low + high) // 2
            if target == data[mid]:
                return mid      # return mid point as the index
            elif target < data[mid]:
                # recur on the portion left of the middle
                return self._bsearch_for_index(data, target, low, mid - 1)
            else:
                # recur on the portion right of the middle
                return self._bsearch_for_index(data, target, mid + 1, high)
        
    def insert(self, value):
        # add item to the list, maintaining sorted order.
        if self._n > 0:
            if self._n == self._capacity:           # if no room left
                self._resize(2 * self._capacity)    # double capacity
            # find insersion point
            ins_index = self._bsearch_for_index(self._A, value, 0, self._n-1)
            # shift values rightward to make space
            for j in range(self._n, ins_index, -1):
                self._A[j] = self._A[j - 1]
            self._A[ins_index] = value
            self._n += 1
        else:
            self.append(value)
                
        
if __name__ == "__main__":
    B  = OrderedDynamicArray()
    B.insert(5)
    B.insert(4)
    B.insert(3)
    B.insert(2)
    B.insert(1)
    B.insert(2)
    B.insert(7)
    B.insert(5)
    B.insert(4)
    B.insert(3)
    B.insert(22)
    B.insert(1)
    B.insert(2)
    B.insert(7)    
    for number in B:
        print(number)