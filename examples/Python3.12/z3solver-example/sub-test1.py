# sub-test1.py — Logical constraints and SAT/UNSAT solving
from z3 import Int, Bool, Solver, And, Or, Not, Implies, sat, unsat


def main():
    print("=== sub-test1: logical constraints and SAT solving ===\n")

    # ------------------------------------------------------------------ #
    # Test 1a: Sudoku row-uniqueness constraint (3 cells, simplified)     #
    # ------------------------------------------------------------------ #
    print("Test 1a: Row-uniqueness — three cells must hold distinct values 1..3")

    c1, c2, c3 = Int("c1"), Int("c2"), Int("c3")
    s = Solver()

    # Domain: each cell ∈ {1, 2, 3}
    for c in (c1, c2, c3):
        s.add(c >= 1, c <= 3)

    # All-different
    s.add(c1 != c2, c1 != c3, c2 != c3)

    result = s.check()
    print(f"Result:    {result}")
    assert result == sat
    m = s.model()
    vals = sorted([m[c1].as_long(), m[c2].as_long(), m[c3].as_long()])
    print(f"Values:    c1={m[c1]}, c2={m[c2]}, c3={m[c3]}")
    assert vals == [1, 2, 3]
    print(f"  All-different, domain [1..3] satisfied: {vals == [1, 2, 3]}")

    # ------------------------------------------------------------------ #
    # Test 1b: Implication chain                                           #
    # ------------------------------------------------------------------ #
    print("\nTest 1b: Implication chain — p→q, q→r, p=True ⊢ r=True")

    p, q, r = Bool("p"), Bool("q"), Bool("r")
    s2 = Solver()
    s2.add(Implies(p, q))
    s2.add(Implies(q, r))
    s2.add(p)           # p is true
    s2.add(Not(r))      # assume r is false — should be UNSAT

    result2 = s2.check()
    print(f"Result (with ¬r forced):  {result2}")
    assert result2 == unsat
    print(f"  Correctly UNSAT (p→q→r but ¬r contradicts p=True): {result2 == unsat}")

    # ------------------------------------------------------------------ #
    # Test 1c: XOR semantics via And/Or                                    #
    # ------------------------------------------------------------------ #
    print("\nTest 1c: Exclusive-or — exactly one of (a, b) is true")

    a, b = Bool("a"), Bool("b")
    s3 = Solver()
    xor_ab = And(Or(a, b), Not(And(a, b)))  # a XOR b
    s3.add(xor_ab)

    result3 = s3.check()
    assert result3 == sat
    m3 = s3.model()
    av = bool(m3[a])
    bv = bool(m3[b])
    print(f"Result:  {result3}")
    print(f"  a={av}, b={bv}")
    print(f"  Exactly one True: {av != bv}")
    assert av != bv

    # ------------------------------------------------------------------ #
    # Test 1d: Integer modular constraint                                  #
    # ------------------------------------------------------------------ #
    print("\nTest 1d: Find n in [0..30] divisible by both 3 and 5")

    n = Int("n")
    s4 = Solver()
    s4.add(n >= 0, n <= 30)
    s4.add(n % 3 == 0)
    s4.add(n % 5 == 0)

    result4 = s4.check()
    assert result4 == sat
    m4 = s4.model()
    nv = m4[n].as_long()
    print(f"Result:  {result4}")
    print(f"  n={nv}")
    print(f"  n % 3 == 0: {nv % 3 == 0}")
    print(f"  n % 5 == 0: {nv % 5 == 0}")
    assert nv % 3 == 0 and nv % 5 == 0

    print("\nsub-test1 completed successfully!")


if __name__ == "__main__":
    main()
