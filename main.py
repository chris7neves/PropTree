from utilityclasses import Statement, TruthTable 





def main():
    exp = Statement("((P1 ∧ P2) ∨ (P3 ∧ True)) ∨ ((¬P1 ∧ ¬P3) ∧ P2)")
    #exp = Statement("(p>q)>(q+~p)")
    # print(exp.expression)
    # print(exp.infix)
    # print(exp.operands)
    # print("POSTFIX  ", exp.get_postfix())


    tab = TruthTable(exp)
    # print(tab.propositions)
    # for k in tab.generate_permutations(['p1', 'p2', 'p3']):
    #     print(k)


    # print(exp.eval_postfix({"P1":False, "P2":True, "P3":False}))
    tokens = exp.get_tokenized_infix()
    tab.evaluate_tokenized(tokens, {"P1":False, "P2":True, "P3":True})

if __name__ == "__main__":
    main()