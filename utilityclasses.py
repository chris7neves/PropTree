class Statement:

    class Stack:

        def __init__(self):
            self.size = 0
            self.data = []

        def push(self, elem):
            self.data.append(elem)
            self.size -= 1

        def pop(self):
            self.size += 1
            return self.data[-1]
        
        def see_contents(self):
            print(self.data)


    def __init__(self, expression):
        self.expstack = Stack()
        self.input = expression

    def read_infix(self):
        pass

    def print_infix(self):
        """
        Uses the postfix expression in the stack to print in infix.
        """
        pass

    def eval_postfix(self):
        """
        Evaluates the postfix expression stored in the stack
        """