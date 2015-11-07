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


class PostfixCalc(object):

    def __init__(self):
        self.stack = Stack()

    # parse a postfix expression and return the result
    def compute_expression(self, ex):
        operators = {'*': lambda x, y: x * y, '+': lambda x, y: x + y,
                     '-': lambda x, y: x - y, '/': lambda x, y: x / y}
        self.stack = Stack()
        # iterate the components of the expression
        for ex_item in ex.split():
            if ex_item.isdigit():
                # push number operand to stack
                self.stack.push(float(ex_item))
            else:
                # this is an operator, perform the calculation
                operand_2 = self.stack.pop()
                operand_1 = self.stack.pop()
                result = operators[ex_item](operand_1, operand_2)
                # push the result to the stack
                self.stack.push(result)
        # this should be the result of the expression.
        return self.stack.pop()
