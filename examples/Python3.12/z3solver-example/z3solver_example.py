# z3solver_example.py
from z3 import (
    Int, Bool, Real, Solver, Optimize,
    And, Or, Not, Implies, If,
    sat, unsat, unknown,
    Sum, IntVal
)


def section(title):
    print(f"\n=== {title} ===\n")


def main():
    print("=== z3solver_example: SMT solving fundamentals ===\n")

    # ------------------------------------------------------------------ #
    # 1. Basic SAT: Boolean satisfiability                                 #
    # ------------------------------------------------------------------ #
    section("1. Boolean satisfiability")

    p, q, r = Bool("p"), Bool("q"), Bool("r")
    s = Solver()
    s.add(Or(p, q))
    s.add(Or(Not(p), r))
    s.add(Not(q))

    result = s.check()
    print("Formula:  (p ∨ q) ∧ (¬p ∨ r) ∧ ¬q")
    print(f"Result:   {result}")
    assert result == sat
    m = s.model()
    print(f"Model:    p={m[p]}, q={m[q]}, r={m[r]}")
    print(f"  SAT result matched expected: {result == sat}")

    # ------------------------------------------------------------------ #
    # 2. Integer arithmetic constraints                                    #
    # ------------------------------------------------------------------ #
    section("2. Integer arithmetic constraints")

    x, y = Int("x"), Int("y")
    s2 = Solver()
    s2.add(x + y == 10)
    s2.add(x - y == 4)
    s2.add(x > 0, y > 0)

    result2 = s2.check()
    print("Constraints:  x + y = 10, x - y = 4, x > 0, y > 0")
    print(f"Result:       {result2}")
    assert result2 == sat
    m2 = s2.model()
    xv, yv = m2[x].as_long(), m2[y].as_long()
    print(f"Solution:     x={xv}, y={yv}")
    assert xv + yv == 10 and xv - yv == 4
    print(f"  x + y == 10: {xv + yv == 10}")
    print(f"  x - y == 4 : {xv - yv == 4}")

    # ------------------------------------------------------------------ #
    # 3. Unsatisfiability detection                                        #
    # ------------------------------------------------------------------ #
    section("3. Unsatisfiability detection")

    a = Int("a")
    s3 = Solver()
    s3.add(a > 5)
    s3.add(a < 3)

    result3 = s3.check()
    print("Constraints:  a > 5  AND  a < 3  (impossible)")
    print(f"Result:       {result3}")
    assert result3 == unsat
    print(f"  Correctly detected UNSAT: {result3 == unsat}")

    # ------------------------------------------------------------------ #
    # 4. Optimization: minimize/maximize an objective                      #
    # ------------------------------------------------------------------ #
    section("4. Linear optimization")

    cost, units = Int("cost"), Int("units")
    opt = Optimize()
    opt.add(units >= 1, units <= 20)
    opt.add(cost == units * 15)
    opt.minimize(cost)

    opt_result = opt.check()
    print("Minimize:  cost = units * 15,  1 ≤ units ≤ 20")
    print(f"Result:    {opt_result}")
    assert opt_result == sat
    mo = opt.model()
    uv, cv = mo[units].as_long(), mo[cost].as_long()
    print(f"Optimal:   units={uv}, cost={cv}")
    assert uv == 1 and cv == 15
    print(f"  Minimum cost achieved: {cv == 15}")

    # ------------------------------------------------------------------ #
    # 5. If-Then-Else (ITE) expressions                                    #
    # ------------------------------------------------------------------ #
    section("5. If-Then-Else expressions")

    n = Int("n")
    abs_n = If(n >= 0, n, -n)
    s5 = Solver()
    s5.add(n == -7)

    result5 = s5.check()
    assert result5 == sat
    m5 = s5.model()
    nv = m5[n].as_long()
    # Evaluate abs via Python since z3 ITE is a formula handle
    abs_val = nv if nv >= 0 else -nv
    print(f"n = {nv},  |n| = {abs_val}")
    assert abs_val == 7
    print(f"  |n| == 7: {abs_val == 7}")

    print("\n=== z3solver_example completed successfully ===")


if __name__ == "__main__":
    main()
