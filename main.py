import sys
import json
from utilityclasses import Statement, TruthTable 

def read_prop_json(path):

    with open(path, 'r', encoding='utf-8') as fin:
        prop = json.load(fin)

    if "values" in prop.keys():
        prop["values"] = {k: bool(v) for k, v in prop["values"].items()}

    return prop["sentence"], prop.get("values")

def question1():
    ############################################################
    #                       Question 1                         #
    ############################################################

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