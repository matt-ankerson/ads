class Stack:
    # LIFO stack implementation using Python's list as storage.   
    def __init__(self):
        # create an empty stack.
        self._data = []
        
    def __len__(self):
        return len(self._data)
        
    def is_empty(self):
        return len(self._data) == 0
        
    def push(self, e):
        # new item stored at the end of the list
        self._data.append(o)
        
    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data[-1]
        
    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()
        
# Function to parse a mathematical expression
