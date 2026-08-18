# sub-test2.py — Optimization problems
from z3 import Int, Real, Optimize, And, sat


def main():
    print("=== sub-test2: optimization problems ===\n")

    # ------------------------------------------------------------------ #
    # Test 2a: Resource allocation — maximize profit                       #
    # ------------------------------------------------------------------ #
    print("Test 2a: Resource allocation — maximize profit")
    print("  Products A and B, limited labor (40h) and material (60 units)")
    print("  A: 2h labor, 3 material, profit $5")
    print("  B: 4h labor, 2 material, profit $7")

    a, b = Int("a"), Int("b")        # units of product A and B
    opt = Optimize()

    opt.add(a >= 0, b >= 0)
    opt.add(2 * a + 4 * b <= 40)     # labor constraint
    opt.add(3 * a + 2 * b <= 60)     # material constraint

    profit_expr = 5 * a + 7 * b
    opt.maximize(profit_expr)

    result = opt.check()
    print(f"Result:  {result}")
    assert result == sat
    mo = opt.model()
    av, bv = mo[a].as_long(), mo[b].as_long()
    profit = 5 * av + 7 * bv
    print(f"  A={av}, B={bv}, Profit=${profit}")
    assert 2 * av + 4 * bv <= 40
    assert 3 * av + 2 * bv <= 60
    assert profit > 0
    print(f"  Labor constraint satisfied:    {2*av + 4*bv} <= 40")
    print(f"  Material constraint satisfied: {3*av + 2*bv} <= 60")
    print(f"  Profit: ${profit}")

    # ------------------------------------------------------------------ #
    # Test 2b: Budget minimization                                         #
    # ------------------------------------------------------------------ #
    print("\nTest 2b: Budget minimization — buy at least 10 items, two suppliers")
    print("  Supplier X: $3/item, max 8 items")
    print("  Supplier Y: $5/item, unlimited")

    x, y = Int("x"), Int("y")
    opt2 = Optimize()

    opt2.add(x >= 0, x <= 8)
    opt2.add(y >= 0)
    opt2.add(x + y >= 10)

    budget = 3 * x + 5 * y
    opt2.minimize(budget)

    result2 = opt2.check()
    assert result2 == sat
    mo2 = opt2.model()
    xv, yv = mo2[x].as_long(), mo2[y].as_long()
    cost = 3 * xv + 5 * yv
    print(f"Result:  {result2}")
    print(f"  Supplier X: {xv} items, Supplier Y: {yv} items")
    print(f"  Total items: {xv + yv}")
    print(f"  Total cost: ${cost}")
    assert xv + yv >= 10
    assert xv <= 8
    assert cost == 34   # optimal: 8 from X ($24) + 2 from Y ($10)
    print(f"  Minimum cost achieved ($34): {cost == 34}")

    # ------------------------------------------------------------------ #
    # Test 2c: Multi-objective with soft constraints                       #
    # ------------------------------------------------------------------ #
    print("\nTest 2c: Soft constraints — prefer x close to 5, hard: x in [0..10]")

    xc = Int("xc")
    opt3 = Optimize()
    opt3.add(xc >= 0, xc <= 10)     # hard constraint

    # Soft: penalize distance from 5
    diff = Int("diff")
    opt3.add(diff >= xc - 5, diff >= 5 - xc)  # diff = |xc - 5|
    opt3.minimize(diff)

    result3 = opt3.check()
    assert result3 == sat
    mo3 = opt3.model()
    xcv = mo3[xc].as_long()
    dv = mo3[diff].as_long()
    print(f"Result:  {result3}")
    print(f"  xc={xcv}, |xc-5|={dv}")
    assert dv == 0 and xcv == 5
    print(f"  Optimal value is 5 (distance=0): {xcv == 5}")

    print("\nsub-test2 completed successfully!")


if __name__ == "__main__":
    main()
