class Queue:
    # LILO queue implementation using Python's list as storage
    # LILO = Last in last out.
    DEFAULT_CAP = 10
    
    def __init__(self):
        # create an empty queue
        self._data = [None] * Queue.DEFAULT_CAP
        self._size = 0
        self._front = 0
        
    def __len__(self):
        return self._size
        
    def is_empty(self):
        return self._size == 0
        
    def first(self):
        # return but don't remove the first element of the queue
        if self.is_empty():
            raise Empty('The queue is empty')
        return self._data[self._front]
    
    def dequeue(self):
        # remove and return the first element of the queue. (FIFO)
        if self.is_empty():
            raise Empty('The queue is empty')
        answer = self._data[self._front]
        self._data[self._front] = None
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        return answer
        
    def enqueue(self, e):
        # add an element to the back of the queue
        if self._size == len(self._data):
            self._resize(2 * len(self._data))   # double the array size
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = e
        self._size += 1
        
    def _resize(self, cap):
        # resize to a new capacity
        old = self._data                # keep track of the old list
        self._data = [None] * cap       # allocate list with new capacity
        walk = self._front
        for k in range(self._size):     # only consider existing elements
            self._data[k] = old[walk]   # intentionally shift indices
            walk = (1 + walk) % len(old)# use old size as modulus
        self._front = 0                 # front has been realigned