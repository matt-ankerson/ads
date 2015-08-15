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
            raise Empty('Stack is empty')
        return self._data[-1]
        
    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')
        return self._data.pop()
        
# Function to parse a mathematical expression with only single digits
def compute_expression(ex):
    operators = {'*': lambda x, y: x * y, '+': lambda x, y: x + y,\
    '-': lambda x, y: x - y, '/': lambda x, y: x / y}
    stack = Stack()
    for c in ex:
        if c == '(':
            pass
        elif c == ')':  # this means we need to perform the computation now
            operand_2 = stack.pop()
            operator = stack.pop()
            operand_1 = stack.pop()
            stack.push(operator(operand_1, operand_2))
        elif c.isdigit():
            stack.push(float(c))
        elif c == ' ':
            pass
        else:   # c is an operator
            stack.push(operators[c])
    # return the result of the expression
    return stack.pop()
 
           
result = compute_expression('(((3 + 3)/2) - (6 * (8 - 2)))')
print(result)