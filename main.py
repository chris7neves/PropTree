from utilityclasses import Statement 





def main():
    exp = Statement("((P1 ∧ P2) ∨ (P3 ∧ True)) ∨ ((¬P1 ∧ ¬P3) ∧ P2)")
    #exp = Statement("(p>q)>(q+~p)")
    print(exp.expression)
    print(exp.infix)
    print(exp.operands)
    print("POSTFIX  ", exp.get_postfix())







if __name__ == "__main__":
    main()