import sys
#https://www.includehelp.com/c/evaluation-of-postfix-expressions-using-stack-with-c-program.aspx#:~:text=Evaluation%20rule%20of%20a%20Postfix,the%20end%20of%20the%20expression.
class Statement:

    class Stack:

        def __init__(self):
            self.size = 0
            self.data = []

        def push(self, elem):
            self.data.append(elem)
            self.size += 1

        def pop(self):
            self.size -= 1
            return self.data.pop(-1)
        
        def see_contents(self):
            print(self.data)

        def peek(self):
            if self.size > 0:
                return self.data[-1]
            else:
                return None
        
        def is_empty(self):
            if self.data:
                return False
            return True

    class Queue(Stack):

        def __init__(self):
            super().__init__()

        def pop(self):
            self.size -= 1
            return self.data.pop(0)
        
        def peek(self):
            return self.data[0]

    def __init__(self, expression):

        self.op_dict = {">":4, "&":2, "!":1, "+":3}
        self.operators, self.output = self.Stack(), self.Queue()
        self.expression = expression
        
        self.infix = self.clean(self.expression)
        self.operands = self.extract_operands(self.infix)
        self.postfix = self.infix_to_postfix(self.infix)
        


    def clean(self, expression):

        equivalencies = {"¬":"!", "∧":"&", "∨":"+", "→":">", "~":"!"}

        for k, v in equivalencies.items():
            expression = expression.replace(k, v)
        
        expression = expression.replace("True", 't').replace("true", 't')
        expression = expression.replace("False", 'f').replace("false", 'f')
        expression = expression.replace(" ", '')
        
        return expression

    def is_op(self, text):
        """
        Checks to see if text is an operator.
        """
        
        if text in self.op_dict.keys():
            return True
        return False
    
    def extract_operands(self, expression):

        for k in self.op_dict.keys():
            expression = expression.replace(k, ',')
        
        expression = expression.replace(' ', '')
        expression = expression.replace('(', '')
        expression = expression.replace(')', '')

        return set([x for x in expression.split(',') if x])


    def infix_to_postfix(self, expression):

        # Add a space after operands to enable end of operand tokenizing
        for op in self.operands:
            expression = expression.replace(op, op + " ")
        
        print(expression)

        curr_operand = []
        for c in expression:

            if self.is_op(c):
                if self.operators.peek() == '!':
                    while(self.operators.peek() == '!'): # While loop just to allow me to deal with multiple chained not operators
                        self.output.push(self.operators.pop())
                else:
                    self.operators.push(c)

            elif c == '(':
                self.operators.push(c)
            elif c == ')':
                while(self.operators.peek() != '('):
                    self.output.push(self.operators.pop())
                self.operators.pop() # Get rid of the (

            elif c == ' ': # Finished operand parsing, can add to output
                operand = ''.join(curr_operand)

                if operand not in self.operands:
                    print("Invalid string entered: {}".format(operand))
                    print("Stopping program execution.")
                    sys.exit()

                self.output.push(operand)
                curr_operand = []
            else: # Operand
                curr_operand.append(c)
        
        # Pop out all remaining operators from the operator stack
        while not self.operators.is_empty():
            self.output.push(self.operators.pop())

        return self.output.data

    def get_postfix(self):
        return ''.join(self.postfix)

    def eval_postfix(self):
        """
        Evaluates the postfix expression stored in the stack
        """
    
