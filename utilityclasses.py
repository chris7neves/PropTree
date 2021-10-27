import sys

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
        self.expression = expression
        
        self.infix = self.clean(self.expression)
        self.operands = self.extract_operands(self.infix)
        self.postfix, self.sub_expressions = self.infix_to_postfix(self.infix)

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

        operators, output = self.Stack(), self.Queue()
        sub_expressions = []

        # Add a space after operands to enable end of operand tokenizing
        for op in self.operands:
            expression = expression.replace(op, op + " ")

        curr_operand = []

        for c in expression:

            if self.is_op(c):
                if operators.peek() == '!':
                    while(operators.peek() == '!'): # While loop just to allow me to deal with multiple chained not operators
                        output.push(operators.pop())
                #     operators.push(c)
                # else:
                operators.push(c)

            elif c == '(':
                operators.push(c)
            elif c == ')':
                while(operators.peek() != '('):
                    output.push(operators.pop())
                operators.pop() # Get rid of the (

            elif c == ' ': # Finished operand parsing, can add to output
                operand = ''.join(curr_operand)

                if operand not in self.operands:
                    print("Invalid string entered: {}".format(operand))
                    print("Stopping program execution.")
                    sys.exit()

                output.push(operand)
                curr_operand = []
            else: # Operand
                curr_operand.append(c)
        
        # Pop out all remaining operators from the operator stack
        while not operators.is_empty():
            output.push(operators.pop())

        return output.data, sub_expressions

    def get_postfix(self):
        return ''.join(self.postfix)

    def eval_logic(self, op, prop1, prop2=None) -> bool:

        if op == '!':
            return (not prop1)
        elif op == '&':
            return (prop1 and prop2)
        elif op == '+':
            return (prop1 or prop2)
        elif op == '>':
            return (not prop1 or prop2)
        else:
            print("Unrecognized operator: '{}'".format(op))
            sys.exit(1)

    def eval_postfix(self, values, expression=None):
        """
        Evaluates the postfix expression stored in the stack
        Values stores the truth values for each of the propositions
        """

        assert isinstance(values, dict)

        if expression is None:
            expression = self.postfix

        postfix = [values[x] if x in values.keys() else x for x in expression]
        postfix = [True if x == 't' else False if x == 'f' else x for x in postfix]

        stack = self.Stack()

        for c in postfix:
            if c == '!':
                p = stack.pop()
                stack.push(self.eval_logic(c, p))

            elif self.is_op(c):
                p2 = stack.pop()
                p1 = stack.pop()
                stack.push(self.eval_logic(c, p1, p2))

            elif isinstance(c, bool):
                stack.push(c)
            else:
                print("Unexpected object in postfix expression: '{}'".format(c))
                sys.exit(1)
        
        return stack.pop()

    def package_exp(self, op, p1, p2=None):
        if op != "!":
            return "({}{}{})".format(p1, op, p2)
        else:
            return "({}{})".format(op, p1)

    def get_tokenized_infix(self):

        postfix = self.postfix
        stack = self.Stack()
        infix = []

        for c in postfix:
            if c == '!':
                p = stack.pop()
                packaged = self.package_exp(c, p)
                stack.push(packaged)
                infix.append(packaged)

            elif self.is_op(c):
                p2 = stack.pop()
                p1 = stack.pop()
                packaged = self.package_exp(c, p1, p2)
                stack.push(packaged)
                infix.append(packaged)

            elif isinstance(c, bool):
                stack.push(c)
            
            elif c in self.operands:
                stack.push(c)

            else:
                print("Unexpected object in postfix expression: '{}'".format(c))
                sys.exit(1)

        return infix

class TruthTable:

    def __init__(self, statement):
        self.statement = statement
        self.propositions = statement.operands
        self.propositions = [x for x in self.propositions if x != 'f' and x != 't']

        self.table = self.generate_table(self.statement.postfix)

    def evaluate_tokenized(self, tokenized, values):
        """
        Values is the corresponding truth values for each proposition
        """

        evaluated = {}

        for token in tokenized:
            temp = Statement(token)
            evaluated[token] = temp.eval_postfix(values)

        return evaluated

    def generate_permutations(self, vars, values=[True, False]):
        cols = []
        iter_every = 1

        for var in vars:
            index = 1
            res = []
            for i in range(1, (2**len(vars))+1):
                if (i % iter_every == 0): index = 1 - index
                res.append([var, values[index]])
            iter_every = iter_every*2
            cols.append(res)
        
        cols = zip(*cols)
        return list(cols)

    def generate_table(self, postfix):
        """
        postfix needs to be in list form
        """

        # Get permutations
        permutations = self.generate_permutations(self.propositions)
        table = permutations

        # Get tokenized statement
        tokens = self.statement.get_tokenized_infix()

        # Iterate through permutations, create values dict from the permutations, evaluate sub expression, append to list that is a copy of permutations
        
        for row in permutations:
            values = {k: v for (k, v) in row}

            # Evalutate sub expressions
            results = []




        # Format the rows and columns, ready to be ingested by the print_table function
        

        return 

    def print_table(self):
        return 





