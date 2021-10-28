#############################################################
# Propositional logic evaluator and truth table generator
# COMP 5361 ASSIGNMENT 2
# Due: Oct 27, 2021
# Author: Christopher Almeida Neves, 27521979
#############################################################

import sys
import json

#-------------------------------------------------------------------
# MAIN CLASSES
#-------------------------------------------------------------------

class Statement:
    """
    Class to represent a propositional sentence and its operations.
    """

    class Stack:
        """
        Inner class used in order to perform the shunting yard algorithm for infix to postfix conversion.
        Used to perform postfix to infix conversion as well. Follows the LIFO order.
        """

        def __init__(self):
            self.size = 0
            self.data = []

        def push(self, elem):
            """
            Add an element to the stack.
            """
            self.data.append(elem)
            self.size += 1

        def pop(self):
            """
            Remove the element at the top of the stack (the element added in last).
            """
            self.size -= 1
            return self.data.pop(-1)
        
        def see_contents(self):
            """
            Print the contents of the stack.
            """
            print(self.data)

        def peek(self):
            """
            Peek at the element at the top of the stack.
            """
            if self.size > 0:
                return self.data[-1]
            else:
                return None
        
        def is_empty(self):
            """
            Returns true if the stack is empty, false if not.
            """

            if self.data:
                return False
            return True

    class Queue(Stack):
        """
        Queue inner class used in the shunting yard algorithm for infix to postfix conversion. Implements the FIFO ordering. 
        Inherits common methods from the Stack.
        """

        def __init__(self):
            super().__init__()

        def pop(self):
            """
            Return the first element added to the queue.
            """
            self.size -= 1
            return self.data.pop(0)
        
        def peek(self):
            """
            Look at the first element in the queue.
            """
            return self.data[0]

    def __init__(self, expression):
        """Constructor for the Statement class.
        
        Attributes:
            op_dict: dictionary containing the operators and their precedence.
            expression: string entered by user. The propositional sentence.
            infix: the cleaned expression. A string. 
            operands: the operands in the expression. Extracted by extract_infix()
            propositions: only the propositional variables in the expression (operands without True, False)
            postfix: list containing each term in the postfix expression. eg: p1p2+ => ['p1', 'p2', '+']
        """

        self.op_dict = {">":4, "&":2, "!":1, "+":3}
        self.expression = expression
        
        self.infix = self._clean(self.expression)
        self.operands = self._extract_operands(self.infix)
        self.propositions = self.operands
        self.propositions = [x for x in self.propositions if x != 'f' and x != 't']
        self.postfix = self.infix_to_postfix(self.infix)

    def _clean(self, expression):
        """
        Cleans the propositional sentence entered by the user. Removes whitespace, 
        replaces operators with the equivalencies used by the program and converts 
        False and True to a more digestible format.
        """

        equivalencies = {"¬":"!", "∧":"&", "∨":"+", "→":">", "~":"!"}

        for k, v in equivalencies.items():
            expression = expression.replace(k, v)
        
        expression = expression.replace("True", 't').replace("true", 't')
        expression = expression.replace("False", 'f').replace("false", 'f')
        expression = expression.replace(" ", '')
        
        return expression

    def _is_op(self, text):
        """
        Checks to see if text is an operator.
        """
        
        if text in self.op_dict.keys():
            return True
        return False
    
    def _extract_operands(self, expression):
        """
        Parses the expression and extracts the operands.

        returns: a set of all the operands in the expression with no duplicates.
        """

        for k in self.op_dict.keys():
            expression = expression.replace(k, ',')
        
        expression = expression.replace(' ', '')
        expression = expression.replace('(', '')
        expression = expression.replace(')', '')

        return set([x for x in expression.split(',') if x])

    def infix_to_postfix(self, expression):
        """
        Implementation of the shunting yard algorithm. Converts the infix expression to postfix.
        """

        operators, output = self.Stack(), self.Queue()
        sub_expressions = []

        # Add a space after operands to enable end of operand tokenizing
        for op in self.operands:
            expression = expression.replace(op, op + " ")

        curr_operand = []

        for c in expression:

            if self._is_op(c):
                if operators.peek() == '!':
                    while(operators.peek() == '!'): # While loop just to allow me to deal with multiple chained not operators
                        output.push(operators.pop())
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

        return output.data

    def get_postfix(self):
        """
        Returns the postfix version of the expression.
        """
        return ''.join(self.postfix)

    def _eval_logic(self, op, prop1, prop2=None) -> bool:
        """
        Evaluates a unary or binary logical expression give the operator and operands. 
        
        returns: True, False
        """

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
        Evaluates the postfix expression using the values provided in "values".
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
                stack.push(self._eval_logic(c, p))

            elif self._is_op(c):
                p2 = stack.pop()
                p1 = stack.pop()
                stack.push(self._eval_logic(c, p1, p2))

            elif isinstance(c, bool):
                stack.push(c)
            else:
                print("Unexpected object in postfix expression: '{}'".format(c))
                sys.exit(1)
        
        return stack.pop()

    def package_exp(self, op, p1, p2=None):
        """
        Helper function to package a unary or binary operation between brackets for sub expression parsing and display.
        """
        if op != "!":
            return "({}{}{})".format(p1, op, p2)
        else:
            return "({}{})".format(op, p1)

    def get_tokenized_infix(self):
        """
        Parses the postfix expression and generates all of the infix sub expressions to be used by the table.
        """

        postfix = self.postfix
        stack = self.Stack()
        infix = []

        for c in postfix:
            if c == '!':
                p = stack.pop()
                packaged = self.package_exp(c, p)
                stack.push(packaged)
                infix.append(packaged)

            elif self._is_op(c):
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
    """
    Class to represent a truth table and expression category as well as the methods needed to build it. 
    Takes in a Statement object in the constructor. 
    """

    def __init__(self, statement):
        """
        Constructor for the Statement object.

        Attributes:
            statement: the Statement object containing the propositional statement and methods to evaluate it
            propositions: the propositions within the statement
            table: the 2D array containing the table that is to be printed to console.
        """
        self.statement = statement
        self.propositions = statement.operands
        self.propositions = [x for x in self.propositions if x != 'f' and x != 't']

        self.table = self.generate_table(self.statement.postfix)

    def evaluate_tokenized(self, tokenized, values):
        """
        Evaluates each of the tokenized sub expressions generated by the Statment class.

        Arguments:
            tokenized: the tokenized sub expressions generated by Statement.get_tokenized_infix()
            values: the dictionary of propositions and their truth values used to evaluate the expression.
        """

        evaluated = []

        for token in tokenized:
            temp = Statement(token)
            evaluated.append([token, temp.eval_postfix(values)])

        return evaluated

    def generate_permutations(self, vars, values=[True, False]) -> list:
        """
        Generates all possible permutations of the propositions in the expression using the principles of binary addition.
        """
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

        return [list(x) for x in zip(*cols)]

    def generate_table(self, postfix) -> list:
        """
        Generates the 2D array representation of the Truth table for the expression provided.

        Arguments: postfix expression in list form
        """

        # Get permutations
        permutations = self.generate_permutations(self.propositions)
        table = permutations

        # Get tokenized statement
        tokens = self.statement.get_tokenized_infix()

        # Iterate through permutations, create values dict from the permutations, evaluate sub expression, append to list that is a copy of permutations
        for i, row in enumerate(permutations):
            values = {k: v for (k, v) in row}
            # Evalutate sub expressions
            results = self.evaluate_tokenized(tokens, values)
            table[i].extend(results)
     
        return table

    def print_table(self, table=None) -> None:
        """
        Helper function to print the table in a formatted fashion.
        """
        
        equivalencies = {"!":"¬", "&":"∧", "+":"∨", ">":"→", "!":"~", "f":"False", "t":"True"}

        if table is None:
            table = self.table

        # Get whitespace numbers and print headers
        whitespaces = []
        for col in table[0]:
            header = col[0]
            for k, v in equivalencies.items():
                header = header.replace(k, v)
            print(" {:8} ".format(header), end='|')
            whitespaces.append(len(header))
        print('')

        whitespaces = [8 if x<8 else x for x in whitespaces]

        for w in whitespaces:
            print("-"*(w+2), end='|')

        for row in table:
            print('')
            for w, col in zip(whitespaces, row):
                print(" {:8} ".format(str(col[1])), end='')
                print(" "*(w-8), end='|')

        print('')
        for w in whitespaces:
            print("-"*(w+2), end='-')
    
    def determine_type(self, table=None):
        """
        Determines whether the expression is a contingency, contradiction or tautology based on the last column of the truth table.
        """

        if table is None:
            table = self.table

        result = [row[-1][1] for row in table]

        if len(set(result)) == 1 and result[0]:
            t = "TAUTOLOGY" 
        elif len(set(result)) == 1 and not result[0]:
            t = "CONTRADICTION"
        elif len(set(result)) == 2:
            t = "CONTINGENCY"

        return t

#-------------------------------------------------------------------
# UTILITY FUNCTIONS
#-------------------------------------------------------------------

def read_prop_json(path):
    """
    Helper function to load the statement and values from a .json file.
    """

    with open(path, 'r', encoding='utf-8') as fin:
        prop = json.load(fin)

    if "values" in prop.keys():
        prop["values"] = {k: bool(v) for k, v in prop["values"].items()}

    return prop["sentence"], prop.get("values")

#-------------------------------------------------------------------
# DRIVERS FOR QUESTIONS 1 AND 2
#-------------------------------------------------------------------

def question1():
    """
    Driver for question 1
    """

    print("""

    ---------------------------------------------------------------------------------------

    QUESTION 1

    For the first part of this program, you will supply a propositional sentence and truth assignments for the variables in 
    that sentence either through json format, or by manual input.

    The program will evaluate the input and return either True or False, depending on how the sentence evaluates.

    The following symbols may be used for operators:
    OR: ∨, +
    AND: ∧, &
    Implication: →, >
    NOT: !, ¬
    
    """)

    input_choice = input("Enter 1 for json, 2 for manual input: ")
    if input_choice == "1":
        json_path = input("Enter the path to your json file (example json file can be found in readme):  ")
        statement, values = read_prop_json(json_path)
        exp1 = Statement(statement)

    elif input_choice == "2":
        statement = input("Enter your propositional statement:  ")
        
        values = {}
        exp1 = Statement(statement)
        for op in exp1.propositions:

            val = input("Enter {} value (1 for true 0 for false): ".format(op))
            while val not in ['1', '0']:
                val = input("Enter {} value (1 for true 0 for false): ".format(op))

            val = int(val)
            values[op] = bool(val)

    else: 
        print("Wrong input choice. Ending program.")
        sys.exit(1)

    print(f"""
    \n
    You entered: {exp1.expression}
    With truth values: {values}

    This evaluates to: {exp1.eval_postfix(values)}
    
    Program completed.

    """)

    return 

def question2():
    """
    Driver for question 2
    """

    print("""

    ---------------------------------------------------------------------------------------

    QUESTION 2

    For question 2, you can supply a propositional sentence to the program and a truth tab;e will be generated. 
    The sentence will also be evaluated to either a CONTINGENCY, TAUTOLOGY or CONTRADICTION depending on its generated
    truth values.

    The propositional sentence can either be input using a json file, or can be manually entered. The format for the json file
    can be found in the project readme.

    The following symbols may be used for operators:
    OR: ∨, +
    AND: ∧, &
    Implication: →, >
    NOT: !, ¬
    
    """)

    input_choice = input("Enter 1 for json, 2 for manual input: ")
    if input_choice == "1":
        json_path = input("Enter the path to your json file (example json file can be found in readme):  ")
        statement, _ = read_prop_json(json_path)
        exp1 = Statement(statement)

    elif input_choice == "2":
        statement = input("Enter your propositional statement:  ")
        exp1 = Statement(statement)

    else: 
        print("Wrong input choice. Ending program.")
        sys.exit(1)

    tab = TruthTable(exp1)

    print(f"""
    \n\n\n
    You entered: {exp1.expression}

    
    TRUTH TABLE:
    """)

    tab.print_table()

    print(f"\n\nThe category of this expression: {tab.determine_type()}\n\n\n Program Completed.")

    return 

#-------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------

def main():

    choice = input("\nEnter 1 for question 1 or 2 for question 2: ")
    while choice not in ['1', '2']:
        choice = input("\nEnter 1 for question 1 or 2 for question 2: ")

    if choice == '1':
        question1()
    elif choice == '2':
        question2()

if __name__ == "__main__":
    main()